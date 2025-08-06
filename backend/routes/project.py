"""Routes for managing projects and running intelligent calculations."""

from flask import Blueprint, request, jsonify, g
from backend.database import db
from backend.utils.auth import decode_token
from functools import wraps
import datetime
import uuid

project_bp = Blueprint("project", __name__, url_prefix="/projects")

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

@project_bp.route("/", methods=["POST"])
@login_required
def create_project():
    data = request.get_json()
    required = ["nome", "descricao"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"erro": f"Campos obrigatórios faltando: {', '.join(missing)}"}), 400
    project = {
        "_id": str(uuid.uuid4()),
        "nome": data["nome"],
        "descricao": data["descricao"],
        "user_id": g.user_payload.get("user_id"),
        "arquivos": data.get("arquivos", []),  # lista de nomes ou URLs
        "material_calc": None,  # será preenchido após IA
        "status": "criado",
        "created_at": datetime.datetime.utcnow().isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat(),
        "historico": []
    }
    db.projects.insert_one(project)
    return jsonify(project), 201

@project_bp.route("/", methods=["GET"])
@login_required
def list_projects():
    user_id = g.user_payload.get("user_id")
    projetos = list(db.projects.find({"user_id": user_id}))
    return jsonify(projetos), 200

@project_bp.route("/<id>", methods=["GET"])
@login_required
def get_project(id):
    proj = db.projects.find_one({"_id": id})
    if not proj:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify(proj), 200

@project_bp.route("/<id>/calc_material", methods=["POST"])
@login_required
def calc_material(id):
    # Aqui será plugada a IA de cálculo de materiais
    proj = db.projects.find_one({"_id": id})
    if not proj:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    # Exemplo: calcular quantidade fictícia de materiais
    materiais = {
        "areia": 10,
        "cimento": 20,
        "tijolos": 5000,
        "ferro": 150
    }
    db.projects.update_one({"_id": id}, {"$set": {"material_calc": materiais, "updated_at": datetime.datetime.utcnow().isoformat()}})
    proj.update({"material_calc": materiais})
    return jsonify({"msg": "Cálculo de materiais salvo!", "materiais": materiais}), 200