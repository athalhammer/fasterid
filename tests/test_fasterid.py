from fastapi.testclient import TestClient

from fasterid import fasterid

client = TestClient(fasterid.app)


def test_read_main():
    response = client.post("/")
    assert response.status_code == 201
    assert response.json() == {"id": ["kxfhqi4aow"], "map": {}}
