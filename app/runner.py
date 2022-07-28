"""A wrapper on subprocess to control the state of the robot"""
import errno
import io
import subprocess as sp
import threading
import sys
from enum import Enum

from app.config import config


class States(Enum):
    READY = "Ready"
    RUNNING = "Running"
    STOPPED = "Stopped"


class Runner:
    """A state machine which cycles through the different"""
    zone: int
    output_file: io.TextIOWrapper
    current_state: States
    next_state: States
    new_state_event: threading.Event
    state_transition_lock: threading.Lock
    runner: threading.Thread
    user_sp: sp.Popen

    def __init__(self):
        self.zone = 0
        self.output_file = open(config.output_file_path, "w")

        self.user_sp = None
        self.current_state = None
        self.next_state = States.READY

        self.state_transition_lock = threading.Lock()
        self.new_state_event = threading.Event()
        self.new_state_event.set()
        self.runner = threading.Thread(target=self._state_machine, daemon=True)
        self.runner.start()

    def _enter_ready_state(self) -> None:
        self.user_sp = sp.Popen(
            [sys.executable, "-u", config.usercode_entry_point],
            stdout=self.output_file,
            stderr=sp.STDOUT,
            universal_newlines=True,
            env=config.robot_env,
        )

    def _enter_running_state(self) -> None:
        """Send start button press to usercode"""
        pass

    def _enter_stopped_state(self) -> None:
        """Reap the users code"""
        if self.user_sp is None:
            return
        return_code = self.user_sp.poll()
        if return_code is None:
            try:
                try:
                    self.user_sp.terminate()
                    self.user_sp.wait(timeout=config.reap_grace_time)
                except sp.TimeoutExpired:
                    self.user_sp.kill()
            except OSError as e:
                if e.errno != errno.ESRCH:  # No such process, already died
                    raise e
        elif return_code != 0:
            print(f"Usercode exited with {return_code} but was not killed by shepherd")

    def _state_machine(self) -> None:
        """The lifecycle of the usercode
        Don't need a try/finlay as @shutdown handles forcing into STOPPED state
        """
        state_timeout = None

        while True:
            self.new_state_event.wait(timeout=state_timeout)
            with self.state_transition_lock:
                self.new_state_event.clear()
                print(f"Moving state from {self.current_state} to {self.next_state}")
                self.current_state = self.next_state
                match self.next_state:
                    case States.READY:
                        self._enter_ready_state()
                        self.next_state = States.RUNNING
                        state_timeout = None
                    case States.RUNNING:
                        self._enter_running_state()
                        self.next_state = States.STOPPED
                        state_timeout = config.round_len
                    case States.STOPPED:
                        self._enter_stopped_state()
                        self.next_state = States.STOPPED
                        state_timeout = None

    @property
    def state(self) -> States:
        with self.state_transition_lock:
            return self.current_state

    @state.setter
    def state(self, next_state: States) -> None:
        with self.state_transition_lock:
            self.next_state = next_state
            self.new_state_event.set()

    def get_output(self) -> io.TextIOWrapper:
        return open(config.output_file_path, "rt", 1)


runner = Runner()
