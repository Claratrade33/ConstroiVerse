from flask import Blueprint, request, jsonify
from backend.config import db

obra_bp = Blueprint('obras', __name__)

# Listar todas as obras
@obra_bp.route('/api/obras', methods=['GET'])
def listar_obras():
    obras = list(db.obras.find({}, {'_id': 0}))
    return jsonify(obras)

# Cadastrar nova obra
@obra_bp.route('/api/obras', methods=['POST'])
def cadastrar_obra():
    data = request.json
    if not data or 'nome' not in data:
        return jsonify({'erro': 'Dados inválidos'}), 400
    db.obras.insert_one(data)
    return jsonify({'mensagem': 'Obra cadastrada com sucesso!'})

# Editar obra (por nome)
@obra_bp.route('/api/obras/<nome>', methods=['PUT'])
def editar_obra(nome):
    data = request.json
    resultado = db.obras.update_one({'nome': nome}, {'$set': data})
    if resultado.matched_count == 0:
        return jsonify({'erro': 'Obra não encontrada'}), 404
    return jsonify({'mensagem': 'Obra atualizada com sucesso!'})

# Remover obra (por nome)
@obra_bp.route('/api/obras/<nome>', methods=['DELETE'])
def remover_obra(nome):
    resultado = db.obras.delete_one({'nome': nome})
    if resultado.deleted_count == 0:
        return jsonify({'erro': 'Obra não encontrada'}), 404
    return jsonify({'mensagem': 'Obra removida com sucesso!'})