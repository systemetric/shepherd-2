"""Functions used by endpoints for sheep"""
import json
import os
import re
from pathlib import Path

from app.config import config


def get_files() -> dict:
    """This read the editable files from the file system and returns them as json
    The blockly blocks are saved in a `blocks.json` and are converted into a
    standardized dictionary.
    """
    project_paths = [f for f in os.listdir(config.usr_src_path)
                     if os.path.isfile(os.path.join(config.usr_src_path, f))
                     and (f.endswith('.py') or f.endswith(".xml") or f == "blocks.json")
                     and f != 'main.py']

    def read_project(project_path: Path) -> dict:
        with open(config.usr_src_path / project_path, 'r') as project_file:
            content = project_file.read()
        return {
            'filename': project_path,
            'content': content
        }

    blocks = {}
    if config.blocks_path.exists():
        with open(config.blocks_path, 'r') as blocks_file:
            try:
                blocks = json.load(blocks_file)
            except ValueError:
                pass

    if "requires" not in blocks:
        blocks["requires"] = []
    if "header" not in blocks:
        blocks["header"] = ""
    if "footer" not in blocks:
        blocks["footer"] = ""
    if "blocks" not in blocks:
        blocks["blocks"] = []

    return {
        'main': config.usr_src_main_path.absolute(),
        'blocks': blocks,
        'projects': [read_project(p) for p in project_paths]
    }


def save_file(filename, body):
    """Write a file with `filename` and `body` to the filesystem"""
    dots = len(re.findall("\\.", filename))
    if dots == 1:
        with open(os.path.join(config.usr_src_path, filename), 'w') as f:
            f.write(body.decode('utf-8'))
    else:
        pass
        logging.warning("A file was attempted to be saved with too many dots: "
                     f"{filename}")


def delete_file(filename):
    """Remove a file with `filename`"""
    if filename == "blocks.json":
        return ""
    dots = len(re.findall("\\.", filename))
    if dots == 1:
        os.unlink(os.path.join(config.usr_src_path, filename))
    else:
        pass
        logging.warning("A file was attempted to be saved with too many dots: "
                     f"{filename}")
