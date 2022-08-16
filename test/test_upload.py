from multiprocessing.connection import wait
from fastapi.testclient import TestClient

from app import app
from convenience import run_python


client = TestClient(app)

def test_file_upload():
    """Upload a file, and read it back"""
    result = run_python(client, "test/stimulus/hello_world.py")
    assert("hello world 550\n" == result)
