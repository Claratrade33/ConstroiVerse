from flask import Blueprint, jsonify, request
from database import db

materiais_controller = Blueprint('materiais_controller', __name__)
materiais_collection = db['materiais']

# Listar materiais
@materiais_controller.route('/materiais', methods=['GET'])
def listar_materiais():
    materiais = list(materiais_collection.find({}, {'_id': 0}))
    return jsonify(materiais)

# Adicionar novo material
@materiais_controller.route('/materiais', methods=['POST'])
def adicionar_material():
    dados = request.get_json()
    campos_obrigatorios = ['nome', 'quantidade', 'obra', 'fabricante']
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({'erro': f'Campos obrigatórios: {campos_obrigatorios}'}), 400

    materiais_collection.insert_one(dados)
    return jsonify({'mensagem': 'Material adicionado com sucesso'})