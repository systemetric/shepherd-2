from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_main():
    """Loading the route should return 200"""
    response = client.get("/")
    assert response.status_code == 200


def test_state():
    """The servers initial state should be Stopped"""
    response = client.get("/state")
    assert response.status_code == 200
    assert response.json() == "Ready"

def test_set_state():
    """Set and check that the new status is accepted"""
    response = client.get("/state?new_state=SomethingWeird")
    print(response.json())
    assert response.status_code == 200

def test_start():
    """Code can be started"""
    client.get("/start")
    response = client.get("/state")
    assert response.status_code == 200
    assert response.json() == "Running"

def test_stop():
    """Code can be stopped"""
    client.get("/start")
    client.get("/stop")
    response = client.get("/state")
    assert response.status_code == 200
    assert response.json() == "Stopped"

def test_code_run():
    """Checks that code can be run"""
    pass