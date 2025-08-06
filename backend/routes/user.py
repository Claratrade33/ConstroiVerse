"""User profile routes: register, view, edit and list users."""

from flask import Blueprint, request, jsonify, g
from backend.database import db
from backend.utils.auth import decode_token, hash_password
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

# Todos os campos obrigatórios para qualquer tipo de usuário
REQUIRED_FIELDS = [
    "role", "nome", "email", "documento", "telefone", "data_nascimento", "endereco",
    "categoria", "descricao", "logo_url", "responsavel", "inscricao_estadual", "nome_fantasia", "created_at"
]

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
    # Atualiza senha se enviada (com hash)
    if "senha" in data:
        data["senha"] = hash_password(data["senha"])
    # Validação de campos obrigatórios
    missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
    if missing:
        return jsonify({"erro": f"Campos obrigatórios faltando: {', '.join(missing)}"}), 400
    data["updated_at"] = datetime.datetime.utcnow().isoformat()
    db.users.update_one({"_id": user.get("_id")}, {"$set": data})
    user.update(data)
    user.pop("password", None)
    return jsonify(user), 200

@user_bp.route("/", methods=["GET"])
@login_required
def list_users():
    role = request.args.get("role")
    filtro = {}
    if role:
        filtro["role"] = role
    users = list(db.users.find(filtro))
    for u in users:
        u.pop("password", None)
    return jsonify(users), 200

@user_bp.route("/<id>", methods=["GET"])
@login_required
def get_user_by_id(id):
    user = db.users.find_one({"_id": id}) or db.users.find_one({"email": id})
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    user.pop("password", None)
    return jsonify(user), 200