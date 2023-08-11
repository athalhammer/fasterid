from fastapi.testclient import TestClient
from fasterid import fasterid


client = TestClient(fasterid)

def test_read_main():
    response = client.post("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
