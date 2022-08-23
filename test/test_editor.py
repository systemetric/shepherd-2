"""Tests for the 'files' endpoint"""
import os
import os.path as path

from pathlib import Path
from pprint import pprint

from app.config import config
from convenience import client


def test_files(client):
    """The `files` endpoint returns the correct data about the files in
    usercode.

    TODO: We should also test weather the blockly works
    https://github.com/systemetric/shepherd-2/issues/24

    A good test would also mock in some files into the usercode/editable folder
    to check that the files can be changed and that those changes are reflected
    by the server
    """
    response = client.get("files/")
    expected_usr_path = Path("usercode/editable").absolute()
    expected_main_path = expected_usr_path / Path("main.py")
    actual_main_path = response.json()["main"]
    assert(actual_main_path == str(expected_main_path))

    pprint(response.json()["projects"][0]["filename"])
    actual_filenames = [project["filename"] for project in response.json()["projects"]]
    expected_filenames = [f for f in os.listdir(expected_usr_path)
                            if path.isfile(path.join(expected_usr_path, f))
                            and (f.endswith('.py') or f.endswith(".xml") or f == "blocks.json")
                            and f != 'main.py']
    assert(actual_filenames == expected_filenames)

    for project in response.json()["projects"]:
        expected_file_name = expected_usr_path / Path(project["filename"])
        with open(expected_file_name) as expected_file:
            expected_file_contents = expected_file.read()
            assert(expected_file_contents == project["content"])


def test_create_and_delete(client):
    """Check that the editor can save and receive files"""
    stimulus_name = "stimulus.py"
    stimulus_contents = "print('hello this is the stimulus program!')"
    stimulus_path = config.usr_src_path / Path(stimulus_name)
    try:
        client.post(f"/files/save/{stimulus_name}", data=stimulus_contents)
        with open(stimulus_path) as stimulus:
            assert(stimulus_contents == stimulus.read())
        client.delete(f"/files/delete/{stimulus_name}")
        assert(stimulus_path.exists() is False)
    finally:
        if stimulus_path.exists():
            os.remove(stimulus_path)
