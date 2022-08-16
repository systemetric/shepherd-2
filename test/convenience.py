"""A set of functions to make writing the tests a bit easier"""
import time
import pprint

from fastapi.testclient import TestClient


def wait_until(expr, interval=0.1, timeout=5):
    start = time.time()
    while not expr:
        if time.time() - start > timeout:
            raise TimeoutError(
                f"wait_until timeout occurred after {timeout}s: {lhs} != {rhs}")
        time.sleep(interval)


def start_python(client: TestClient, python_file: str):
    files = {"archive": ("robot.zip", open(python_file, "rb"))}
    response = client.post("/upload", files=files)
    pprint.pprint(response.content)
    print(python_file)
    assert response.status_code == 201
    time.sleep(1)  # TODO: https://github.com/systemetric/shepherd-2/issues/18
    response = client.get("/start")


def run_python(client: TestClient, python_file: str):
    start_python(client, python_file)
    wait_until(lambda: client.get("/state").json() == "Stopped", timeout=2)
    return client.get("/logs").json()
