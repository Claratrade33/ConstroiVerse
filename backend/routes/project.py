from flask import Blueprint, request, jsonify
from backend.utils.auth import jwt_required
from backend.database import get_db
from backend.models.obra import Obra
from backend.models.orcamento import Orcamento

project_bp = Blueprint("projects", __name__, url_prefix="/api/v1/projects")

@project_bp.post("")
@jwt_required
def create_project():
    db = next(get_db())
    data = request.get_json() or {}
    if not data.get("titulo"):
        return jsonify({"error": "titulo é obrigatório"}), 400
    obra = Obra(titulo=data["titulo"], endereco=data.get("endereco"), owner_id=request.user.id)
    db.add(obra); db.flush()
    return jsonify({"id": obra.id, "titulo": obra.titulo, "endereco": obra.endereco, "status": obra.status}), 201

@project_bp.get("")
@jwt_required
def list_projects():
    db = next(get_db())
    obras = db.query(Obra).filter_by(owner_id=request.user.id).order_by(Obra.id.desc()).all()
    return jsonify([{"id": o.id, "titulo": o.titulo, "status": o.status} for o in obras])

@project_bp.get("/<int:obra_id>")
@jwt_required
def get_project(obra_id: int):
    db = next(get_db())
    o = db.query(Obra).filter_by(id=obra_id, owner_id=request.user.id).first()
    if not o:
        return jsonify({"error": "Obra não encontrada"}), 404
    return jsonify({"id": o.id, "titulo": o.titulo, "endereco": o.endereco, "status": o.status})

@project_bp.patch("/<int:obra_id>")
@jwt_required
def update_project(obra_id: int):
    db = next(get_db())
    o = db.query(Obra).filter_by(id=obra_id, owner_id=request.user.id).first()
    if not o:
        return jsonify({"error": "Obra não encontrada"}), 404
    data = request.get_json() or {}
    for field in ["titulo", "endereco", "status"]:
        if field in data and data[field] is not None:
            setattr(o, field, data[field])
    return jsonify({"id": o.id, "titulo": o.titulo, "endereco": o.endereco, "status": o.status})

@project_bp.delete("/<int:obra_id>")
@jwt_required
def delete_project(obra_id: int):
    db = next(get_db())
    o = db.query(Obra).filter_by(id=obra_id, owner_id=request.user.id).first()
    if not o:
        return jsonify({"error": "Obra não encontrada"}), 404
    db.delete(o)
    return jsonify({"ok": True})

# Orcamentos simples ligados à obra
@project_bp.post("/<int:obra_id>/orcamentos")
@jwt_required
def create_orcamento(obra_id: int):
    db = next(get_db())
    o = db.query(Obra).filter_by(id=obra_id, owner_id=request.user.id).first()
    if not o:
        return jsonify({"error": "Obra não encontrada"}), 404
    data = request.get_json() or {}
    orc = Orcamento(obra_id=o.id, descricao=data.get("descricao"), total=data.get("total", 0), status=data.get("status", "aberto"))
    db.add(orc); db.flush()
    return jsonify({"id": orc.id, "obra_id": o.id, "total": str(orc.total), "status": o.status}), 201

@project_bp.get("/<int:obra_id>/orcamentos")
@jwt_required
def list_orcamentos(obra_id: int):
    db = next(get_db())
    o = db.query(Obra).filter_by(id=obra_id, owner_id=request.user.id).first()
    if not o:
        return jsonify({"error": "Obra não encontrada"}), 404
    itens = db.query(Orcamento).filter_by(obra_id=o.id).all()
    return jsonify([{"id": i.id, "descricao": i.descricao, "total": str(i.total), "status": i.status} for i in itens])