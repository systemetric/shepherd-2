import os

from pathlib import Path


class Settings:

    output_file_path: Path = Path("logs.txt").absolute()
    usercode_path: Path = Path("usercode/").absolute()
    usercode_entry_point = Path("main.py")
    usercode_entry_path: Path = (usercode_path / usercode_entry_point).absolute()

    editor_path: Path = Path("static/editor/").absolute()
    docs_path: Path = Path("static/docs/").absolute()

    round_len: float = 180.0  # seconds
    reap_grace_time: float = 5.0  # seconds
    arenaUSB_path: Path = Path("/media/ArenaUSB")

    robot_path: Path = Path("/home/pi/robot").absolute()
    robot_env: dict = dict(os.environ)
    on_brain: bool = False

    game_control_path: Path = Path('/media/ArenaUSB')
    teamname_file: Path = Path('/home/pi/teamname.txt')

    def __init__(self):
        pass

    def _get_team_specifics(self):
        """Find infomation set on each brain about the team"""
        # Teamname should be set on a per brain basis before shipping
        # Its purpose is to allow the setting of specific graphics for help identifing teams in the arena.
        # Graphics are loaded from the ArenaUSB stick if available, or standard graphics from the stick are used.
        # this used to be in rc.local, but the looks of shame and dissapointment
        # got the better of me

        if teamname_file.exists():
            teamname_jpg = teamname_file.read_text().replace('\n', '') + '.jpg'
        else:
            teamname_jpg = 'none'

        # Pick a start imapge in order of preference :
        #     1) We have a team corner image on the USB
        #     2) The team have uploaded their own image to the robot
        #     3) We have a generic corner image on the USB
        #     4) The game image
        start_graphic = game_control_path / teamname_jpg
        if not start_graphic.exists():
            # attempt to find the team specific corner graphic from the ArenaUSB
            start_graphic = Path('robotsrc/team_logo.jpg')
        if not start_graphic.exists():
            # attempt to find the default corner graphic from ArenaUSB
            start_graphic = game_control_path / 'Corner.jpg'
        if not start_graphic.exists():
            # finally look for a game specific logo
            start_graphic = Path('/home/pi/game_logo.jpg')

        if config.start_graphic.exists():
            static_graphic = Path('shepherd/static/image.jpg')
            static_graphic.write_bytes(start_graphic.read_bytes())



config = Settings()

if config.on_brain is True:
    config.robot_env["PYTHONPATH"] = config.robot_path
