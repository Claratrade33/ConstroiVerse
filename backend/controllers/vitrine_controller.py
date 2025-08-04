from flask import Blueprint, jsonify
from database import db

vitrine_controller = Blueprint('vitrine_controller', __name__)
profissionais_collection = db['profissionais']

# Lista todos os profissionais para exibição pública na vitrine
@vitrine_controller.route('/vitrine', methods=['GET'])
def listar_profissionais_vitrine():
    profissionais = list(profissionais_collection.find({}, {'_id': 0}))
    return jsonify(profissionais)