from flask import Blueprint, request, jsonify
from models.representante import Representante
from database import db

representantes_controller = Blueprint('representantes_controller', __name__)

@representantes_controller.route('/representantes', methods=['POST'])
def cadastrar_representante():
    dados = request.json
    try:
        novo = Representante(**dados)
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Representante cadastrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@representantes_controller.route('/representantes', methods=['GET'])
def listar_representantes():
    try:
        reps = Representante.query.all()
        return jsonify([r.serialize() for r in reps]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500