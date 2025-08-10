from flask import Blueprint, request, jsonify
from backend.database import get_db
from backend.services import auth as authsvc

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    required = ["name", "email", "password"]
    if any(k not in data or not data[k] for k in required):
        return jsonify({"error": "Dados inválidos"}), 400
    db = next(get_db())
    try:
        u = authsvc.register(db, data["name"], data["email"], data["password"])
        return jsonify({"id": u.id, "name": u.name, "email": u.email}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    required = ["email", "password"]
    if any(k not in data or not data[k] for k in required):
        return jsonify({"error": "Dados inválidos"}), 400
    db = next(get_db())
    try:
        token = authsvc.login(db, data["email"], data["password"])
        return jsonify({"token": token})
    except ValueError as e:
        return jsonify({"error": str(e)}), 401