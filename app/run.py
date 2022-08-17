"""A wrapper on subprocess to control the state of the robot"""
import errno
import io
import subprocess as sp
import threading
import logging
import sys
import time
from enum import Enum

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
        self.runner = threading.Thread(target=self._state_machine, daemon=True)
        self.watchdog = threading.Thread(
            target=self._run_watchdog, daemon=True)
        self.runner.start()
        self.watchdog.start()

    def _enter_init_state(self) -> None:
        """Start the user process running.
        Open output file, in read/write with line buffering of 1,
        clearing previous contents
        """
        self.output_file = open(config.output_file_path, "w+", 1)
        self.user_sp = sp.Popen(
            [sys.executable, "-u", config.round_entry_path],
            stdout=self.output_file,
            stderr=sp.STDOUT,
            universal_newlines=True,
            env=config.robot_env,
        )

    def _enter_running_state(self) -> None:
        """Send start signal to usercode"""
        pass  # TODO:

    def _enter_stopped_state(self) -> None:
        """Reap the users code"""
        if self.user_sp is None:
            return
        return_code = self.user_sp.poll()
        if return_code is None:
            # User code is still running so we need to kill it
            try:
                try:
                    self.user_sp.terminate()
                    self.user_sp.wait(timeout=config.reap_grace_time)
                except sp.TimeoutExpired:
                    self.user_sp.kill()
            except OSError as e:
                # Died between us seeing its alive and killing it
                if e.errno != errno.ESRCH:
                    raise e
        elif return_code != 0:
            logging.info(
                f"Usercode exited with {return_code} but was not killed by shepherd")
        self.output_file.close()

    def _state_machine(self) -> None:
        """The lifecycle of the usercode
        Don't need a try/finally as main.shutdown handles forcing into STOPPED state
        """
        state_timeout = None

        while True:
            self.new_state_event.wait(timeout=state_timeout)
            with self.state_transition_lock:
                self.new_state_event.clear()
                logging.info(
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

    def get_output(self):
        """Open the output file in reading text mode, line buffered"""
        return open(config.output_file_path, "rt", 1).read()

    def _run_watchdog(self) -> None:
        """Watches the usercode to check when it exits so we can move to STOPPED
        Runs in a separate thread.
        """
        while True:
            time.sleep(0.25)
            if self._current_state == States.RUNNING:  # Don't acquire lock unless we might need it
                with self.state_transition_lock:
                    if (self._current_state == States.RUNNING) and (self.user_sp.poll() is not None):
                        logging.info("WATCHDOG: Detected usercode has exited")
                        self._next_state = States.STOPPED
                        self.new_state_event.set()

    def shutdown(self):
        self.state = States.STOPPED
        self.output_file.close()


runner = Runner()
