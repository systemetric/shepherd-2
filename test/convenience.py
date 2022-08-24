"""A set of functions to make writing the tests a bit easier"""
import time
import pytest
import os

from fastapi.testclient import TestClient

from app import shepherd
from app.config import config
import app.run

@pytest.fixture
def client():
    try:
        with TestClient(shepherd) as test_client:
            yield test_client
    finally:
        # Don't want to leave the usercode running
        user_sp = app.run.runner.user_sp
        if user_sp.poll() is None:
            user_sp.kill()
            user_sp.communicate()
        if os.path.exists(config.usr_fifo_path) is True:
            os.remove(config.usr_fifo_path)

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
