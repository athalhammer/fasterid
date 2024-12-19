#!/usr/bin/env python3

# Copyright (C) 2023  Andreas Thalhammer
# Please get in touch if you plan to use this in a commercial setting.


from fasterid import app
from fastapi.testclient import TestClient
from rdflib import Graph

client = TestClient(app)


def test_basic():
    response = client.post("/")
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert "@id" in response.json().keys()


def test_multiple():
    response = client.post("/", json={"number": 5})
    assert response.status_code == 201
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5


def test_content_negotiation():
    response = client.post("/", headers={"accept": "application/ld+json"})
    assert response.status_code == 201
    assert response.headers["content-type"] == "application/ld+json"


def test_json_ld():
    response = client.post(
        "/", json={"number": 5}, headers={"accept": "application/ld+json"}
    )
    assert response.status_code == 201
    g = Graph().parse(data=response.content, format="json-ld")
    assert len(g) == 5
