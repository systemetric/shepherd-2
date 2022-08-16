from multiprocessing.connection import wait
from fastapi.testclient import TestClient

from app import app
from convience import wait_until

import time

client = TestClient(app)

def test_file_upload():
    """Upload a file, and read it back"""
    files = {"file": open("test/sample_test_file.py", "rb")}
    res = client.post("/upload", files=files)
    assert res.status_code == 201
    time.sleep(1)
    res = client.get("/start")
    wait_until(lambda: client.get("/state").json() == "Stopped", timeout=2)
    assert("code running from sample_test_file.py\n" == client.get("/logs").json())
