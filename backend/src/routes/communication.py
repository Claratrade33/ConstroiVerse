"""
Rotas para Sistema de Comunicação Interna (Chat e E-mail) - CONVERTIDO PARA FLASK
"""

from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from datetime import datetime
from models.mongodb_models import Mensagem
from src.database import get_collection

communication_bp = Blueprint('communication', __name__)

@communication_bp.route("/messages/<user_id>", methods=["GET"])
def list_user_messages(user_id):
    """
    Listar mensagens de um usuário (recebidas e enviadas)
    """
    try:
        if not ObjectId.is_valid(user_id):
            abort(400, description="ID de usuário inválido")
        
        # Lógica de listagem de mensagens (simulada)
        # messages_collection = get_collection("mensagens")
        # messages = list(messages_collection.find({"$or": [{"sender_id": user_id}, {"recipient_id": user_id}]}))
        
        return jsonify([]) # Retorno simulado
    except Exception as e:
        abort(500, description=f"Erro ao listar mensagens: {str(e)}")


@communication_bp.route("/messages", methods=["POST"])
def send_message():
    """
    Enviar nova mensagem (chat ou e-mail)
    """
    data = request.get_json()
    try:
        sender_id = data.get("sender_id")
        recipient_id = data.get("recipient_id")
        message_type = data.get("message_type")
        content = data.get("content")

        if not ObjectId.is_valid(sender_id) or not ObjectId.is_valid(recipient_id):
            abort(400, description="IDs de usuário inválidos")
        
        if message_type not in ["chat", "email"]:
            abort(400, description="Tipo de mensagem deve ser 'chat' ou 'email'")
        
        if not content:
            abort(400, description="Conteúdo da mensagem não pode estar vazio")
        
        # Lógica de envio de mensagem (simulada)
        new_message = Mensagem(
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        # messages_collection = get_collection("mensagens")
        # result = messages_collection.insert_one(new_message.to_dict())
        
        return jsonify(new_message.to_dict()), 201
    except Exception as e:
        abort(500, description=f"Erro ao enviar mensagem: {str(e)}")


@communication_bp.route("/messages/<message_id>", methods=["GET"])
def get_message(message_id):
    """
    Obter detalhes de uma mensagem específica
    """
    try:
        if not ObjectId.is_valid(message_id):
            abort(400, description="ID de mensagem inválido")
        
        # Lógica de obtenção de mensagem (simulada)
        # messages_collection = get_collection("mensagens")
        # message = messages_collection.find_one({"_id": ObjectId(message_id)})
        
        abort(404, description="Mensagem não encontrada")
    except Exception as e:
        abort(500, description=f"Erro ao obter mensagem: {str(e)}")


@communication_bp.route("/messages/<message_id>/read", methods=["PUT"])
def mark_message_as_read(message_id):
    """
    Marcar mensagem como lida
    """
    try:
        if not ObjectId.is_valid(message_id):
            abort(400, description="ID de mensagem inválido")
        
        # Lógica de marcar como lida (simulada)
        return jsonify({"message": "Mensagem marcada como lida"})
    except Exception as e:
        abort(500, description=f"Erro ao marcar mensagem como lida: {str(e)}")


@communication_bp.route("/messages/<message_id>", methods=["DELETE"])
def delete_message(message_id):
    """
    Deletar mensagem
    """
    try:
        if not ObjectId.is_valid(message_id):
            abort(400, description="ID de mensagem inválido")
        
        # Lógica de deleção de mensagem (simulada)
        return jsonify({"message": "Mensagem deletada com sucesso"}), 204
    except Exception as e:
        abort(500, description=f"Erro ao deletar mensagem: {str(e)}")


@communication_bp.route("/conversations/<user_id>", methods=["GET"])
def list_conversations(user_id):
    """
    Listar conversas de um usuário
    """
    try:
        if not ObjectId.is_valid(user_id):
            abort(400, description="ID de usuário inválido")
        
        # Lógica de listagem de conversas (simulada)
        return jsonify([])
    except Exception as e:
        abort(500, description=f"Erro ao listar conversas: {str(e)}")


@communication_bp.route("/conversations/<user_id>/<other_user_id>", methods=["GET"])
def get_conversation(user_id, other_user_id):
    """
    Obter conversa entre dois usuários
    """
    try:
        if not ObjectId.is_valid(user_id) or not ObjectId.is_valid(other_user_id):
            abort(400, description="IDs de usuário inválidos")
        
        # Lógica de obtenção de conversa (simulada)
        return jsonify([])
    except Exception as e:
        abort(500, description=f"Erro ao obter conversa: {str(e)}")
