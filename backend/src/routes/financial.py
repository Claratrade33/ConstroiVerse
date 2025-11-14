"""
Rotas para Gestão Financeira - CONVERTIDO PARA FLASK
"""

from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from datetime import datetime
from models.mongodb_models import Transacao
from src.database import get_collection

financial_bp = Blueprint('financial', __name__)


@financial_bp.route("/records", methods=["GET"])
def list_financial_records():
    """
    Listar registros financeiros do usuário com filtros opcionais
    """
    try:
        user_id = request.args.get("user_id")
        
        if not ObjectId.is_valid(user_id):
            abort(400, description="ID de usuário inválido")
            
        # Lógica de listagem de registros (simulada)
        # records_collection = get_collection("transacoes")
        # query = {"user_id": user_id}
        # records = list(records_collection.find(query))
        
        return jsonify([]) # Retorno simulado
    except Exception as e:
        abort(500, description=f"Erro ao listar registros financeiros: {str(e)}")


@financial_bp.route("/records", methods=["POST"])
def create_financial_record():
    """
    Criar novo registro financeiro
    """
    data = request.get_json()
    try:
        record_type = data.get("type")
        amount = data.get("amount")
        
        if record_type not in ["income", "expense"]:
            abort(400, description="Tipo deve ser 'income' ou 'expense'")
        if amount is None or amount <= 0:
            abort(400, description="Valor deve ser maior que zero")
            
        # Lógica de criação de registro (simulada)
        # new_record = Transacao(**data)
        # records_collection = get_collection("transacoes")
        # result = records_collection.insert_one(new_record.to_dict())
        
        return jsonify(data), 201 # Retorno simulado
    except Exception as e:
        abort(500, description=f"Erro ao criar registro financeiro: {str(e)}")


@financial_bp.route("/records/<record_id>", methods=["GET"])
def get_financial_record(record_id):
    """
    Obter detalhes de um registro financeiro específico
    """
    try:
        if not ObjectId.is_valid(record_id):
            abort(400, description="ID de registro inválido")
        
        # Lógica de obtenção de registro (simulada)
        # records_collection = get_collection("transacoes")
        # record = records_collection.find_one({"_id": ObjectId(record_id)})
        
        abort(404, description="Registro financeiro não encontrado")
    except Exception as e:
        abort(500, description=f"Erro ao obter registro financeiro: {str(e)}")


@financial_bp.route("/records/<record_id>", methods=["PUT"])
def update_financial_record(record_id):
    """
    Atualizar registro financeiro
    """
    data = request.get_json()
    try:
        if not ObjectId.is_valid(record_id):
            abort(400, description="ID de registro inválido")
        
        # Lógica de atualização de registro (simulada)
        # records_collection = get_collection("transacoes")
        # updated_record = records_collection.find_one_and_update(
        #     {"_id": ObjectId(record_id)},
        #     {"$set": data},
        #     return_document=True
        # )
        
        # if not updated_record:
        #     abort(404, description="Registro financeiro não encontrado")
            
        return jsonify(data) # Retorno simulado
    except Exception as e:
        abort(500, description=f"Erro ao atualizar registro financeiro: {str(e)}")


@financial_bp.route("/records/<record_id>", methods=["DELETE"])
def delete_financial_record(record_id):
    """
    Deletar registro financeiro
    """
    try:
        if not ObjectId.is_valid(record_id):
            abort(400, description="ID de registro inválido")
        
        # Lógica de deleção de registro (simulada)
        # records_collection = get_collection("transacoes")
        # result = records_collection.delete_one({"_id": ObjectId(record_id)})
        
        # if result.deleted_count == 0:
        #     abort(404, description="Registro financeiro não encontrado")
            
        return jsonify({"message": "Registro financeiro deletado com sucesso"}), 204
    except Exception as e:
        abort(500, description=f"Erro ao deletar registro financeiro: {str(e)}")


@financial_bp.route("/summary/<user_id>", methods=["GET"])
def get_financial_summary(user_id):
    """
    Obter resumo financeiro do usuário (total de entradas e saídas)
    """
    try:
        if not ObjectId.is_valid(user_id):
            abort(400, description="ID de usuário inválido")
            
        # Lógica de resumo financeiro (simulada)
        return jsonify({
            "total_income": 15000.00,
            "total_expense": 8500.00,
            "balance": 6500.00,
            "currency": "BRL"
        })
    except Exception as e:
        abort(500, description=f"Erro ao obter resumo financeiro: {str(e)}")
