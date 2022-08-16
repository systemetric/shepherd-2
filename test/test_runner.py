import time
from fastapi.testclient import TestClient
import pytest

from app import app

from convenience import start_python, wait_until

client = TestClient(app)

@pytest.mark.xfail(reason="Ready state not implemented, https://github.com/systemetric/shepherd-2/issues/18")
def test_inital_state():
    """The server is ready to run code within timeout seconds of starting"""
    wait_until(lambda: client.get("/state").json() == "Ready")
    assert client.get("/state").status_code == 200

def test_start():
    """Code can be started"""
    client.get("/start")
    wait_until(lambda: client.get("/state").json() == "Running")
    assert client.get("/state").status_code == 200

def test_stop():
    """Code can be stopped within TIMEOUT seconds of it commanding to be stopped"""
    client.get("/start")
    client.get("/stop")
    wait_until(lambda: client.get("/state").json() == "Stopped")
    assert client.get("/state").status_code == 200

def test_kill_user_code():
    """Usercode can be killed
    Runs a while True loop printing out `running` then ensures that once the
    code is stopped that the output does not continue to grow.
    """
    start_python(client, "test/stimulus/while_true.py")
    client.get("/stop")
    wait_until(lambda: client.get("/state").json() == "Stopped")
    log1 = client.get("/logs").json()
    time.sleep(0.1)
    log2 = client.get("/logs").json()
    assert(log1 == log2)
