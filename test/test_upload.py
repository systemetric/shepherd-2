import shutil
from pathlib import Path
import tempfile
from fastapi.testclient import TestClient

from app import app
from convenience import run_python


client = TestClient(app)

def test_file_upload():
    """Upload a file, and read it back"""
    result = run_python(client, "test/stimulus/hello_world.py")
    assert("hello world 550\n" == result)


def test_zip_upload():
    """Upload a zip with a main.py to check it runs"""
    with tempfile.TemporaryDirectory() as dir:
        archive_name = dir + "/robot"
        shutil.make_archive(
            archive_name,
            "zip",
            Path("test/stimulus/example_zip").absolute()
        )
        print(Path("test/stimulus/example_zip").absolute())
        result = run_python(client, archive_name + ".zip")
    raise Exception(result)
