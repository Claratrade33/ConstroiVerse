from flask import Blueprint, request, jsonify
from models.profissional import Profissional
from database import db

profissional_controller = Blueprint('profissional_controller', __name__)

@profissional_controller.route('/profissionais', methods=['POST'])
def criar_profissional():
    dados = request.json
    try:
        novo = Profissional(**dados)
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Profissional cadastrado!'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@profissional_controller.route('/profissionais', methods=['GET'])
def listar_profissionais():
    try:
        profissionais = Profissional.query.all()
        return jsonify([p.serialize() for p in profissionais]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500