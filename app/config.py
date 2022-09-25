import os

import logging
from pathlib import Path
import tempfile


class Settings:

    log_file_path: Path = Path("logs.txt")
    round_path: Path = Path("usercode/round").absolute()
    round_entry_point = Path("main.py")
    round_entry_path: Path = (round_path / round_entry_point).absolute()

    static_path: Path = Path("static/").absolute()
    editor_path: Path = Path("static/editor/").absolute()
    docs_path: Path = Path("static/docs/").absolute()

    round_len: float = 180.0  # seconds
    reap_grace_time: float = 5.0  # seconds
    arena_usb_path: Path = Path("/media/ArenaUSB")

    robot_path: Path = Path("/home/pi/robot")
    robot_env: dict = dict(os.environ)
    on_brain: bool = False

    robot_usb_path: Path = Path("/media/RobotUSB")
    teamname_file: Path = Path("/home/pi/teamname.txt")
    zone: bool = False

    """
    Pick a start image in order of preference :
        1) Camera Image (Deleted on Start)
        2) Corner Image (USB)
        3) Team Image (Uploaded)
        4) Generic Corner Image (Arena USB Exists)
        5) Teddy Image
    """
    camera_image_files: list[Path] = [
        Path("static/image.jpg"),
        Path("static/temp.jpg"),
        arena_usb_path / "Corner.jpg",
        Path('usercode/editable/team_logo.jpg'),
        Path("static/game/teddy.jpg")
    ]

    # tempfile.mktemp is deprecated, but there's no possibility of a race --
    usr_fifo_path = tempfile.mktemp(prefix="shepherd-fifo-")

    def __init__(self):
        self._on_brain()
        self._init_usercode_folder()
        self._zone_from_USB()
        self._get_team_image()

        # os.mkfifo raises if its path already exists.
        os.mkfifo(self.usr_fifo_path)

    def _on_brain(self):
        """Detects if we are on a brain and alters the config accordingly
        Looks to see if the robot_usb path exists, if it does then we are
        probably on a configured brain rather than a dev PC
        """
        if self.robot_usb_path.exists():
            logging.warning("Detected RobotUSB path assuming on brain")
            self.log_file_path = self.robot_usb_path / self.log_file_path
            config.robot_env["PYTHONPATH"] = config.robot_path
            self._get_team_specifics()

    def _init_usercode_folder(self):
        """Ensure that the saved usercode has a main.py and blocks.json"""
        self.usr_src_path = Path("usercode/editable").absolute()
        if not self.usr_src_path.exists():
            os.mkdir(self.usr_src_path)

        self.usr_src_main_path = self.usr_src_path / Path('main.py')
        with open(self.usr_src_main_path, 'w') as main_file:
            main_file.write('# DO NOT DELETE\n')
        self.blocks_path = self.usr_src_path / Path('blocks.json')

        if self.round_path.exists() is False:
            os.mkdir(self.round_path)

    def _zone_from_USB(self):
        """Set the zone based on the ARENAUSB, defaulting to zone 0"""
        self.zone = "0"
        for i in range(1, 4):
            if (self.arena_usb_path / f"zone{i}.txt").exists():
                self.zone = str(i)
                return

    def _get_team_image(self):
        """Find information set on each brain about the team

        Only makes sense to run this if we are on a brain
        Teamname is set per brain before shipping and allows unique graphics
        for ID'ing teams in the arena.
        """
        teamname_jpg = 'none'
        if self.teamname_file.exists():
            teamname_jpg = self.teamname_file.read_text().strip() + '.jpg'
        
        self.camera_image_files[1] = Path(teamname_jpg) 

config = Settings()
