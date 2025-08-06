"""User profile routes: view and edit your own profile."""

from flask import Blueprint, request, jsonify, g
from backend.database import db
from backend.utils.auth import decode_token
from functools import wraps
import datetime

user_bp = Blueprint("user", __name__, url_prefix="/users")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"erro": "Token não fornecido"}), 401
        token = auth.split(" ")[1]
        payload = decode_token(token)
        if not payload:
            return jsonify({"erro": "Token inválido ou expirado"}), 401
        g.user_payload = payload
        return f(*args, **kwargs)
    return decorated

@user_bp.route("/me", methods=["GET"])
@login_required
def get_my_profile():
    user_id = g.user_payload.get("user_id")
    user = db.users.find_one({"_id": user_id}) or db.users.find_one({"email": user_id})
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    user.pop("password", None)
    return jsonify(user), 200

@user_bp.route("/me", methods=["PUT"])
@login_required
def edit_my_profile():
    user_id = g.user_payload.get("user_id")
    user = db.users.find_one({"_id": user_id}) or db.users.find_one({"email": user_id})
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    data = request.get_json()
    # Campos permitidos para edição
    update = {k: v for k, v in data.items() if k not in ["_id", "email", "password", "role"]}
    update["updated_at"] = datetime.datetime.utcnow().isoformat()
    db.users.update_one({"_id": user.get("_id")}, {"$set": update})
    user.update(update)
    user.pop("password", None)
    return jsonify(user), 200
