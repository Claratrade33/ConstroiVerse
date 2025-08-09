import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SECRET_KEY", "testing")
os.environ["MONGO_URI"] = ""

from backend.app import create_app
from backend.database import db


@pytest.fixture()
def client():
    app = create_app()
    with app.test_client() as client:
        db.users.delete_many({})
        yield client
        db.users.delete_many({})


def register_user(client):
    return client.post("/auth/register", json={
        "username": "tester",
        "email": "tester@example.com",
        "password": "123456",
        "role": "engenheiro",
    })


def login_user(client):
    return client.post("/auth/login", json={
        "email": "tester@example.com",
        "password": "123456",
    })


def test_register_and_login(client):
    resp = register_user(client)
    assert resp.status_code == 201
    resp = login_user(client)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "token" in data


def test_get_profile(client):
    register_user(client)
    login_resp = login_user(client)
    token = login_resp.get_json()["token"]
    resp = client.get("/users/tester@example.com", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["email"] == "tester@example.com"
