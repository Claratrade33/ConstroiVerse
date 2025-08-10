from functools import wraps
from flask import request, jsonify
from backend.services.auth import decode_token
from backend.database import get_db
from backend.models.user import User

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Token ausente"}), 401
        token = auth.split(" ", 1)[1]
        try:
            payload = decode_token(token)
        except Exception:
            return jsonify({"error": "Token inválido"}), 401
        user_id = payload.get("sub")
        db = next(get_db())
        user = db.get(User, user_id)  # SQLAlchemy 2.x
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 401
        request.user = user
        request.db = db
        return fn(*args, **kwargs)
    return wrapper