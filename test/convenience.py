"""A set of functions to make writing the tests a bit easier"""
import time
import pytest

from fastapi.testclient import TestClient

from app import shepherd

@pytest.fixture
def client():
    with TestClient(shepherd) as test_client:
        yield test_client

def wait_until(expr, interval=0.1, timeout=5):
    start = time.time()
    while not expr():
        if time.time() - start > timeout:
            raise TimeoutError(
                f"wait_until timeout occurred after {timeout}s: {expr}")
        time.sleep(interval)


def start_python(client: TestClient, python_file: str):
    files = {"uploaded_file": (python_file, open(python_file, "rb"))}
    response = client.post("/upload/upload", files=files)
    assert response.status_code == 201
    time.sleep(1)  # TODO: https://github.com/systemetric/shepherd-2/issues/18
    response = client.post("/run/start")
    # Can't just check for Running as the usercode could crash on entrance
    wait_until(lambda: client.get("run/state").json() in ["Running", "Stopped"], timeout=5, interval=0.01)


def run_python(client: TestClient, python_file: str):
    start_python(client, python_file)
    wait_until(lambda: client.get("run/state").json() == "Stopped", timeout=2)
    return client.get("run/logs").json()
