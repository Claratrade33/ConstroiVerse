from flask import Blueprint, jsonify, request
from database import db

fabricantes_controller = Blueprint('fabricantes_controller', __name__)
fabricantes_collection = db['fabricantes']

# Listar fabricantes
@fabricantes_controller.route('/fabricantes', methods=['GET'])
def listar_fabricantes():
    fabricantes = list(fabricantes_collection.find({}, {'_id': 0}))
    return jsonify(fabricantes)

# Adicionar fabricante
@fabricantes_controller.route('/fabricantes', methods=['POST'])
def adicionar_fabricante():
    dados = request.get_json()
    if 'nome' not in dados or 'produtos' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome, produtos'}), 400

    fabricantes_collection.insert_one(dados)
    return jsonify({'mensagem': 'Fabricante cadastrado com sucesso'})