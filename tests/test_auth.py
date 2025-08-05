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


def test_register_and_login(client):
    resp = client.post("/auth/register", json={
        "email": "tester@example.com",
        "password": "123456",
        "main_profile": "engenheiro",
    })
    assert resp.status_code == 201

    resp = client.post("/auth/login", json={
        "email": "tester@example.com",
        "password": "123456",
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "token" in data
    assert data["main_profile"] == "engenheiro"


def test_perfil_endpoint(client):
    client.post("/auth/register", json={
        "email": "tester@example.com",
        "password": "123456",
        "main_profile": "engenheiro",
    })
    resp = client.get("/perfil/tester@example.com")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["painel"] == "/painel_engenheiro"