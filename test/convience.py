"""A set of functions to make writing the tests a bit easier"""
import time

def wait_until(expr, interval=0.1, timeout=5):
    start = time.time()
    while not expr:
        if time.time() - start > timeout:
            raise TimeoutError(f"wait_until timeout occurred after {timeout}s: {lhs} != {rhs}")
        time.sleep(interval)

def upload_python(client, python):
    files = {"file": open("test/sample_test_file.py", "rb")}
    res = client.post("/upload", files=files)
    assert res.status_code == 201
    time.sleep(1)
    res = client.get("/start")
    wait_until(lambda: client.get("/state").json() == "Stopped", timeout=2)
    return client.get("/logs").json()
