from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_main():
    """Loading the route should return 200"""
    response = client.get("/")
    assert response.status_code == 200