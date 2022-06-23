from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):

    output_file_path: Path = Path("./logs/logs.txt")
    usercode_path: Path = Path("./usercode/")
    sheep_files_path: Path = Path("./files/")
    round_len: int = 180  # seconds

    # The config for each round in the arena
    arenaUSB_path: Path = Path("/media/ArenaUSB")

    robot_lib_path: Path = Path("/home/pi/robot")



settings = Settings()
