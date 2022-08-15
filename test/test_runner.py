from fastapi.testclient import TestClient
import pytest

from app import app

STATE_TRANS_TIMEOUT = 5

client = TestClient(app)

@pytest.mark.timeout(STATE_TRANS_TIMEOUT)
def test_inital_state():
    """The server is ready to run code within STATE_TRANS_TIMEOUT seconds of starting"""
    while (response := client.get("/state")).json() != "Ready":
        pass
    assert response.status_code == 200

@pytest.mark.timeout(STATE_TRANS_TIMEOUT)
def test_start():
    """Code can be started"""
    client.get("/start")
    while (response := client.get("/state")).json() != "Running":
        pass
    assert response.status_code == 200

@pytest.mark.timeout(STATE_TRANS_TIMEOUT)
def test_stop():
    """Code can be stopped within STATE_TRANS_TIMEOUT seconds of it commanding to be stopped"""
    client.get("/start")
    client.get("/stop")
    while (response := client.get("/state")).json() != "Stopped":
        pass
    assert response.status_code == 200
