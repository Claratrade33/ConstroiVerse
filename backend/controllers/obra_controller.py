from flask import Blueprint, jsonify, request
from config import db

obra_bp = Blueprint('obra_bp', __name__)
obras_collection = db['obras']

@obra_bp.route('/api/obras', methods=['GET'])
def listar_obras():
    obras = list(obras_collection.find({}, {'_id': 0}))
    return jsonify(obras)

@obra_bp.route('/api/obras', methods=['POST'])
def criar_obra():
    dados = request.json
    obras_collection.insert_one(dados)
    return jsonify({"mensagem": "Obra criada com sucesso!"}), 201