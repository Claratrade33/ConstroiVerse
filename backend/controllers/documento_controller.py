from flask import Blueprint, jsonify, request
from database import db

documentos_controller = Blueprint('documentos_controller', __name__)
documentos_collection = db['documentos']

# Listar documentos
@documentos_controller.route('/documentos', methods=['GET'])
def listar_documentos():
    documentos = list(documentos_collection.find({}, {'_id': 0}))
    return jsonify(documentos)

# Adicionar documento
@documentos_controller.route('/documentos', methods=['POST'])
def adicionar_documento():
    dados = request.get_json()
    if 'nome' not in dados or 'obra' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome, obra'}), 400

    documentos_collection.insert_one(dados)
    return jsonify({'mensagem': 'Documento salvo com sucesso'})