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
        result = run_python(client, archive_name + ".zip")
    assert(result == "zip files work\n")


def test_large_zip_upload():
    """upload a zip file which is larger than any usercode should be"""
    import stimulus.large_zip.main as large_pi
    with tempfile.TemporaryDirectory() as dir:
        archive_name = dir + "/robot"
        shutil.make_archive(
            archive_name,
            "zip",
            Path("test/stimulus/large_zip").absolute()
        )
        result = run_python(client, archive_name + ".zip")
    assert(result == "{}\n".format(large_pi.pi))
