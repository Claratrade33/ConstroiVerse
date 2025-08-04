from flask import Blueprint, jsonify, request
from config import db

perfil_bp = Blueprint('perfil_bp', __name__)
usuarios_collection = db['usuarios']

@perfil_bp.route('/api/perfis', methods=['GET'])
def listar_perfis():
    usuarios = list(usuarios_collection.find({}, {'_id': 0}))
    return jsonify(usuarios)

@perfil_bp.route('/api/perfis/<string:tipo>', methods=['GET'])
def listar_por_tipo(tipo):
    usuarios = list(usuarios_collection.find({'tipo': tipo}, {'_id': 0}))
    return jsonify(usuarios)