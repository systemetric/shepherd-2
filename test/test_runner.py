import time
from fastapi.testclient import TestClient
import pytest

from app import app

from convenience import start_python, wait_until

client = TestClient(app)

@pytest.mark.xfail(reason="Ready state not implemented, https://github.com/systemetric/shepherd-2/issues/18")
def test_inital_state():
    """The server is ready to run code within timeout seconds of starting"""
    wait_until(lambda: client.get("/run/state").json() == "Ready")
    assert client.get("/run/state").status_code == 200

def test_start():
    """Code can be started"""
    client.post("/run/start")
    wait_until(lambda: client.get("/run/state").json() == "Running")
    response = client.get("/run/state")
    assert response.status_code == 200

def test_stop():
    """Code can be stopped within TIMEOUT seconds of it commanding to be stopped"""
    client.post("/run/start")
    client.post("/run/stop")
    wait_until(lambda: client.get("/run/state").json() == "Stopped")
    assert client.get("/run/state").status_code == 200

def test_kill_user_code():
    """Usercode can be killed
    Runs a while True loop printing out `running` then ensures that once the
    code is stopped that the output does not continue to grow.
    """
    start_python(client, "test/stimulus/while_true.py")
    client.post("/run/stop")
    wait_until(lambda: (client.get("/run/state").json() == "Stopped"))
    log1 = client.get("/run/logs").json()
    time.sleep(1)
    log2 = client.get("/run/logs").json()
    assert(log1 == log2)
