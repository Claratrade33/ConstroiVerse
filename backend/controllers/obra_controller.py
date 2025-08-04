# backend/controllers/obra_controller.py

from flask import Blueprint, request, jsonify
from backend.config import db

obra_bp = Blueprint('obras', __name__)

@obra_bp.route('/api/obras', methods=['GET'])
def listar_obras():
    obras = list(db.obras.find({}, {'_id': 0}))
    return jsonify(obras)

# (Adicione aqui outras rotas do controller conforme sua lógica)