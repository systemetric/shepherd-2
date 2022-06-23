"""Controls the running of an stopping of user code.

Most of the interface to this module should be just set/getting the
`RunnerHandler.state`
"""
import io
import subprocess as sp
import sys
from enum import Enum

from app.config import settings


class RunnerState(Enum):
    READY = "Ready"
    STOPPED = "Stopped"
    RUNNING = "Running"


class RunnerHandler:
    zone: int
    user_code: sp.Popen
    output_file: io.TextIOWrapper
    _state: RunnerState

    def __init__(self):
        print("Runner handler created")
        self.zone = 0
        self.user_code = None
        self.output_file = None
        self._state = RunnerState.STOPPED

    def start_user_code(self) -> None:
        self.stop_user_code()
        if self.output_file:
            self.output_file.close()
        self.output_file = open(settings.output_file_path, "wt", 1)
        self.user_code = sp.Popen(
            [sys.executable, "-u", settings.usercode_path + "/main.py"],
            bufsize=1,
            stdout=self.output_file,
            stderr=sp.STDOUT,
            universal_newlines=True,
        )
        self._state = RunnerState.RUNNING

    def stop_user_code(self) -> bool:
        if self.user_code:
            self.user_code.kill()
            self.user_code.wait()
            self._state = RunnerState.STOPPED
            return True
        return False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        match new_state:
            case RunnerState.RUNNING:
                self.start_user_code()
            case RunnerState.STOPPED:
                self.stop_user_code()
            case RunnerState.READY:
                pass
            case _:
                raise Exception("Invalid state")

    def get_output(self) -> io.TextIOWrapper:
        return open(settings.output_file_path, "rt", 1)
