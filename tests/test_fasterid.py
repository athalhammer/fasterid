from fastapi.testclient import TestClient

from fasterid import fasterid
from fasterid.settings import Settings, get_settings

client = TestClient(fasterid.app)

def get_settings_override():
    return Settings (
        sqlalchemy_database_url="sqlite:///./test.sqlite"
    )

fasterid.app.dependency_overrides[get_settings] = get_settings_override

def test_request_id():
    response = client.post("/")
    assert response.status_code == 201
    #assert response.json() == {"id": ["kxfhqi4aow"], "map": {}}

def test_request_prefix_id():
    response = client.post("/", data={"number": 5, "prefix": "https://example.com/"})
    assert response.status_code == 201

def test_request_mapped_id():
    response = client.post("/", data={"number": 1, "key": ["test"]})
    assert response.status_code == 201

def test_request_mapped_prefix_id():
    response = client.post("/", data={"number": 1, "prefix": "https://example.com/", "key": ["test"]})
    assert response.status_code == 201