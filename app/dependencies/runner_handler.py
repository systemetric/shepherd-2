import io
import os
import subprocess as sp
import sys
from enum import Enum

from config import settings


class RunnerState(Enum):
    NOTCREATED = "Not Created"
    NOTRUNNING = "Not Running"
    RUNNING = "Running"


class RunnerHandler:
    zone: int
    started: bool
    user_code: sp.Popen
    output_file: io.TextIOWrapper

    def __init__(self):
        print("Runner handler created")
        self.zone = -1
        self.started = False
        self.user_code = None
        self.output_file = None

    def start_user_code(self) -> None:
        self.stop_user_code()
        if self.output_file:
            self.output_file.close()
        self.started = False

        self.output_file = open(settings.output_file_path, "wt", 1)
        self.user_code = sp.Popen(
            [sys.executable, "-u", settings.usercode_path + "/main.py"],
            bufsize=1,
            stdout=self.output_file,
            stderr=sp.STDOUT,
            universal_newlines=True,
        )

    def stop_user_code(self) -> bool:
        if self.user_code:
            self.user_code.kill()
            self.user_code.wait()
            return True
        return False

    def get_state(self) -> RunnerState:
        if not self.user_code:
            return RunnerState.NOTCREATED
        if self.user_code.poll() is not None:
            return RunnerState.NOTRUNNING
        return RunnerState.RUNNING

    def get_output(self) -> io.TextIOWrapper:
        return open(settings.output_file_path, "rt", 1)
