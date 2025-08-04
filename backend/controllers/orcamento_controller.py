from flask import Blueprint, request, jsonify
from models.orcamento import Orcamento
from database import db
from services.clarice import gerar_orcamento_ia

orcamento_controller = Blueprint('orcamento_controller', __name__)

@orcamento_controller.route('/orcamento', methods=['POST'])
def criar_orcamento():
    dados = request.json
    try:
        novo_orcamento = Orcamento(**dados)
        db.session.add(novo_orcamento)
        db.session.commit()
        return jsonify({'mensagem': 'Orçamento criado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@orcamento_controller.route('/orcamento/gerar', methods=['POST'])
def gerar_orcamento_automatico():
    dados = request.json
    try:
        resultado = gerar_orcamento_ia(dados)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@orcamento_controller.route('/orcamentos', methods=['GET'])
def listar_orcamentos():
    try:
        orcamentos = Orcamento.query.all()
        return jsonify([o.serialize() for o in orcamentos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500