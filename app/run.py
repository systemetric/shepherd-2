"""A wrapper on subprocess to control the state of the robot"""
import errno
import io
import os
import subprocess as sp
import threading
import sys
import time
from enum import Enum

from app.logging import logger
from app.config import config


class States(Enum):
    INIT = "Init"
    RUNNING = "Running"
    STOPPED = "Stopped"


class Runner:
    """A state machine which cycles through the different"""
    zone: int
    output_file: io.TextIOWrapper
    new_state_event: threading.Event
    state_transition_lock: threading.Lock
    runner: threading.Thread
    user_sp: sp.Popen
    _current_state: States
    _next_state: States

    def __init__(self):
        self.zone = 0
        self.output_file = None

        self.user_sp = None
        self._current_state = None
        self._next_state = States.INIT

        self.state_transition_lock = threading.Lock()
        self.new_state_event = threading.Event()
        self.new_state_event.set()
        self.watchdog = threading.Thread(
            target=self._run_watchdog, daemon=True)
        self.runner = threading.Thread(target=self._state_machine, daemon=True)
        self.watchdog.start()
        self.runner.start()

    def _enter_init_state(self) -> None:
        """Start the user process running.
        Open output file, in read/write with line buffering of 1,
        clearing previous contents
        """
        # Can't just truncate the file it is possible that we don't close the
        # file which can leave it in a mess to be truncated.
        if config.log_file_path.exists():
            os.remove(config.log_file_path)
        self.output_file = open(config.log_file_path, "w+", 1)
        self.user_sp = sp.Popen(
            [sys.executable, "-u", config.round_entry_path,
             "--startfifo", config.usr_fifo_path],
            stdout=self.output_file,
            stderr=sp.STDOUT,
            universal_newlines=True,
            env=config.robot_env,
            preexec_fn=os.setsid
        )
        logger.info(f"Started usercode PID:{os.getpgid(self.user_sp.pid)}")

    def _enter_running_state(self) -> None:
        """Send start signal to usercode"""
        start_settings = {
                "mode": "comp",
                "zone": int(config.zone),
                "arena": "A",
            }
        # This is the old way of locking shepherd up until user code is ready
        # to run however we should have a ready state so that we can't get here
        # unless the usercode is ready to run
        # TODO: https://github.com/systemetric/shepherd-2/issues/13
        # with os.open(config.usr_fifo_path, os.O_WRONLY ) as usr_fifo:
        #     json.dump(start_settings, usr_fifo)

    def _enter_stopped_state(self) -> None:
        """Reap the users code"""
        if self.user_sp is None:
            logger.debug("Re-entering STOPPED state. Usercode already stopped")
            return
        return_code = self.user_sp.poll()
        if return_code is None:
            self.kill_usercode()
        else:
            logger.debug(
                f"Usercode exited with {return_code} but was not killed by Shepherd")
        self.output_file.close()
        self.user_sp = None

    def _state_machine(self) -> None:
        """The lifecycle of the usercode
        Don't need a try/finally as main.shutdown handles forcing into STOPPED state
        """
        state_timeout = None
        self._next_state = States.INIT
        self._current_state = None

        while True:
            self.new_state_event.wait(timeout=state_timeout)
            with self.state_transition_lock:
                self.new_state_event.clear()
                logger.info(
                    f"Moving state from {self._current_state} to {self._next_state}")
                self._current_state = self._next_state
                match self._next_state:
                    case States.INIT:
                        self._enter_init_state()
                        self._next_state = States.RUNNING
                        state_timeout = None
                    case States.RUNNING:
                        self._enter_running_state()
                        self._next_state = States.STOPPED
                        state_timeout = config.round_len
                    case States.STOPPED:
                        self._enter_stopped_state()
                        self._next_state = States.STOPPED
                        state_timeout = None

    @property
    def state(self) -> States:
        with self.state_transition_lock:
            return self._current_state

    @state.setter
    def state(self, next_state: States) -> None:
        """Moves into a new state
        Waits for the other thread to acquire the lock so is guaranteed to cause
        a transition.
        """
        with self.state_transition_lock:
            self._next_state = next_state
            self.new_state_event.set()
        while self.new_state_event.is_set():  # Only cleared in the state_machine thread
            time.sleep(0.05)                  # Don't use 100% CPU

    def kill_usercode(self):
        """Try and terminate usercode if unable kill it.
        This function deliberately does not acquire any lock on the state machine
        and so the effect of this will only be noticed by the watchdog
        """
        logger.info("Trying to kill usercode")
        if (self.user_sp is not None) and (self.user_sp is not None):
            try:
                try:
                    self.user_sp.terminate()
                    self.user_sp.communicate(timeout=config.reap_grace_time)
                    logger.info("subprocess thinks usercode is dead")
                except sp.TimeoutExpired:
                    logger.warning(
                        f"Usercode could not be terminated within {config.reap_grace_time}s "
                            "sending kill signal"
                    )
                    self.user_sp.kill()
                    self.user_sp.communicate()
            except OSError as e:
                # Usercode was already dead
                if e.errno != errno.ESRCH:
                    raise e


    def get_output(self):
        """Open the output file in reading text mode, line buffered"""
        if not self.output_file.closed:
            self.output_file.flush()
        if config.log_file_path.exists():
            return open(config.log_file_path, "rt", 1).read()
        return ""

    def _run_watchdog(self) -> None:
        """Watches the usercode to check when it exits so we can move to STOPPED
        Runs in a separate thread.
        """
        while True:
            time.sleep(0.25)
            if self._current_state == States.RUNNING:  # Don't acquire lock unless we might need it
                with self.state_transition_lock:
                    if (self._current_state == States.RUNNING) and (self.user_sp.poll() is not None):
                        logger.info("WATCHDOG: Detected usercode has exited")
                        self._next_state = States.STOPPED
                        self.new_state_event.set()



    def shutdown(self):
        self.kill_usercode()
        if self.output_file is not None:
            self.output_file.close()


runner = Runner()
