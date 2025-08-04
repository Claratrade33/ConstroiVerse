from flask import Blueprint, jsonify, request
from config import db

obra_bp = Blueprint('obra_bp', __name__)
obras_collection = db['obras']

# 📌 Listar todas as obras
@obra_bp.route('/api/obras', methods=['GET'])
def listar_obras():
    obras = list(obras_collection.find({}, {'_id': 0}))
    return jsonify(obras)

# 📌 Cadastrar nova obra
@obra_bp.route('/api/obras', methods=['POST'])
def cadastrar_obra():
    dados = request.get_json()
    if 'nome' not in dados or 'responsavel' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome, responsavel'}), 400

    obras_collection.insert_one(dados)
    return jsonify({'mensagem': 'Obra cadastrada com sucesso'})