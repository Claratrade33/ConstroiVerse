"""Authentication routes for user registration and login.

These endpoints allow clients to register new users and authenticate
existing users. Passwords are securely hashed before being stored, and
JWT tokens are returned upon successful registration or login.
"""

from flask import Blueprint, jsonify, request
from backend.database import db
from backend.utils.auth import hash_password, verify_password, generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required = {"username", "email", "password", "role"}
    if not data or not required.issubset(data.keys()):
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400
    if db.users.find_one({"email": data["email"]}):
        return jsonify({"erro": "E-mail já cadastrado"}), 400
    user = {
        "username": data["username"],
        "email": data["email"],
        "password": hash_password(data["password"]),
        "role": data["role"]
    }
    db.users.insert_one(user)
    token = generate_token(str(user.get("_id", user["email"])), user["role"])
    return jsonify({"mensagem": "Usuário registrado", "token": token}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"erro": "Campos obrigatórios ausentes"}), 400
    user = db.users.find_one({"email": data["email"]})
    if not user or not verify_password(data["password"], user["password"]):
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401
    token = generate_token(str(user.get("_id", user["email"])), user["role"])
    return jsonify({"mensagem": "Login efetuado", "token": token}), 200
