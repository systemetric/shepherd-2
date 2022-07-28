import os

from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):

    output_file_path: Path = Path("logs.txt")
    usercode_path: Path = Path("usercode/")
    usercode_entry_point: Path = Path("usercode/main.py").absolute()
    sheep_files_path: Path = Path("files/")

    round_len: float = 180.0  # seconds
    reap_grace_time: float = 5.0  # seconds
    arenaUSB_path: Path = Path("/media/ArenaUSB")

    robot_path: Path = Path("/home/pi/robot").absolute()
    robot_env: dict = dict(os.environ)
    on_brain: bool = False

config = Settings()
if config.on_brain is True:
    config.robot_env["PYTHONPATH"] = config.robot_path

