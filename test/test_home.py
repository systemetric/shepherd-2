from convenience import client


def test_read_main(client):
    """Loading the route should return 200"""
    response = client.get("/")
    assert response.status_code == 200