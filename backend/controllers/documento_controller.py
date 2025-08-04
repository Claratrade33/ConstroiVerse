from flask import Blueprint, jsonify, request
from database import db

documento_controller = Blueprint('documento_controller', __name__)
documentos_collection = db['documentos']

# Listar todos os documentos
@documento_controller.route('/documentos', methods=['GET'])
def listar_documentos():
    documentos = list(documentos_collection.find({}, {'_id': 0}))
    return jsonify(documentos)

# Adicionar novo documento
@documento_controller.route('/documentos', methods=['POST'])
def adicionar_documento():
    dados = request.get_json()
    if not dados.get('nome') or not dados.get('obra'):
        return jsonify({'erro': 'Nome e obra são obrigatórios'}), 400

    documentos_collection.insert_one(dados)
    return jsonify({'mensagem': 'Documento cadastrado com sucesso'})