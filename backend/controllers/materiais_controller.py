from flask import Blueprint, jsonify, request
from database import db

materiais_controller = Blueprint('materiais_controller', __name__)
materiais_collection = db['materiais']

# Listar todos os materiais
@materiais_controller.route('/materiais', methods=['GET'])
def listar_materiais():
    materiais = list(materiais_collection.find({}, {'_id': 0}))
    return jsonify(materiais)

# Adicionar novo material
@materiais_controller.route('/materiais', methods=['POST'])
def adicionar_material():
    dados = request.get_json()
    if 'nome' not in dados or 'categoria' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome, categoria'}), 400

    materiais_collection.insert_one(dados)
    return jsonify({'mensagem': 'Material cadastrado com sucesso'})