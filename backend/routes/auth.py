from flask import Blueprint, request, jsonify
from backend.database import get_db
from backend.services import auth as authsvc
from sqlalchemy.orm import Session

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

def _db() -> Session:
    return next(get_db())

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    db = _db()
    u = authsvc.register(db, data["name"], data["email"], data["password"])
    return jsonify({"id": u.id, "name": u.name, "email": u.email}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    db = _db()
    token = authsvc.login(db, data["email"], data["password"])
    return jsonify({"token": token})