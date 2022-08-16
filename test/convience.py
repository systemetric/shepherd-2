"""A set of functions to make writing the tests a bit easier"""
import time

from fastapi.testclient import TestClient


def wait_until(expr, interval=0.1, timeout=5):
    start = time.time()
    while not expr:
        if time.time() - start > timeout:
            raise TimeoutError(f"wait_until timeout occurred after {timeout}s: {lhs} != {rhs}")
        time.sleep(interval)


def upload_python(client: TestClient, python_file: str):
    files = {"file": open(python_file, "rb")}
    res = client.post("/upload", files=files)
    assert res.status_code == 201
    time.sleep(1) # TODO: https://github.com/systemetric/shepherd-2/issues/18
    res = client.get("/start")
    wait_until(lambda: client.get("/state").json() == "Stopped", timeout=2)
    return client.get("/logs").json()
