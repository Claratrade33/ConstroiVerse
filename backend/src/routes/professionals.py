"""
Rotas para Vitrine de Profissionais - CONVERTIDO PARA FLASK
"""

from flask import Blueprint, jsonify, request, abort
from bson import ObjectId
from datetime import datetime
from models.mongodb_models import PerfilProfissional, AvaliacaoProfissional
from src.database import get_collection

professionals_bp = Blueprint('professionals', __name__)

@professionals_bp.route("/", methods=["GET"])
def list_professionals():
    """
    Listar profissionais com filtros opcionais
    """
    try:
        # Filtros do request.args (Flask)
        profession = request.args.get("profession")
        location = request.args.get("location")
        min_rating = request.args.get("min_rating", type=float)
        skip = request.args.get("skip", type=int, default=0)
        limit = request.args.get("limit", type=int, default=10)
        
        # Lógica de listagem de profissionais (simulada)
        # professionals_collection = get_collection("perfis_profissionais")
        # query = {}
        # if profession:
        #     query["profissao"] = profession
        # if location:
        #     query["localizacao"] = location
        # if min_rating:
        #     query["nota_media"] = {"$gte": min_rating}
            
        # professionals = list(professionals_collection.find(query).skip(skip).limit(limit))
        
        return jsonify([]) # Retorno simulado
    except Exception as e:
        abort(500, description=f"Erro ao listar profissionais: {str(e)}")


@professionals_bp.route("/<professional_id>", methods=["GET"])
def get_professional(professional_id):
    """
    Obter detalhes de um profissional específico
    """
    try:
        if not ObjectId.is_valid(professional_id):
            abort(400, description="ID de profissional inválido")
        
        # Lógica de obtenção de profissional (simulada)
        # professionals_collection = get_collection("perfis_profissionais")
        # professional = professionals_collection.find_one({"_id": ObjectId(professional_id)})
        
        abort(404, description="Profissional não encontrado")
    except Exception as e:
        abort(500, description=f"Erro ao obter profissional: {str(e)}")


@professionals_bp.route("/", methods=["POST"])
def create_professional():
    """
    Criar novo perfil de profissional
    """
    data = request.get_json()
    try:
        # Lógica de criação de profissional (simulada)
        # new_professional = PerfilProfissional(**data)
        # professionals_collection = get_collection("perfis_profissionais")
        # result = professionals_collection.insert_one(new_professional.to_dict())
        
        return jsonify(data), 201 # Retorno simulado
    except Exception as e:
        abort(500, description=f"Erro ao criar profissional: {str(e)}")


@professionals_bp.route("/<professional_id>", methods=["PUT"])
def update_professional(professional_id):
    """
    Atualizar perfil de profissional
    """
    data = request.get_json()
    try:
        if not ObjectId.is_valid(professional_id):
            abort(400, description="ID de profissional inválido")
        
        # Lógica de atualização de profissional (simulada)
        # professionals_collection = get_collection("perfis_profissionais")
        # updated_professional = professionals_collection.find_one_and_update(
        #     {"_id": ObjectId(professional_id)},
        #     {"$set": data},
        #     return_document=True
        # )
        
        # if not updated_professional:
        #     abort(404, description="Profissional não encontrado")
            
        return jsonify(data) # Retorno simulado
    except Exception as e:
        abort(500, description=f"Erro ao atualizar profissional: {str(e)}")


@professionals_bp.route("/<professional_id>", methods=["DELETE"])
def delete_professional(professional_id):
    """
    Deletar perfil de profissional
    """
    try:
        if not ObjectId.is_valid(professional_id):
            abort(400, description="ID de profissional inválido")
        
        # Lógica de deleção de profissional (simulada)
        # professionals_collection = get_collection("perfis_profissionais")
        # result = professionals_collection.delete_one({"_id": ObjectId(professional_id)})
        
        # if result.deleted_count == 0:
        #     abort(404, description="Profissional não encontrado")
            
        return jsonify({"message": "Profissional deletado com sucesso"}), 204
    except Exception as e:
        abort(500, description=f"Erro ao deletar profissional: {str(e)}")


@professionals_bp.route("/<professional_id>/reviews", methods=["POST"])
def add_review(professional_id):
    """
    Adicionar avaliação a um profissional
    """
    data = request.get_json()
    try:
        if not ObjectId.is_valid(professional_id):
            abort(400, description="ID de profissional inválido")
        
        rating = data.get("rating")
        if rating is None or rating < 1 or rating > 5:
            abort(400, description="Avaliação deve estar entre 1 e 5")
            
        # Lógica de adição de avaliação (simulada)
        # reviews_collection = get_collection("avaliacoes_profissionais")
        # new_review = AvaliacaoProfissional(
        #     professional_id=professional_id,
        #     rating=rating,
        #     comment=data.get("comment"),
        #     reviewer_id=data.get("reviewer_id")
        # )
        # reviews_collection.insert_one(new_review.to_dict())
        
        return jsonify({"message": "Avaliação adicionada com sucesso"}), 201
    except Exception as e:
        abort(500, description=f"Erro ao adicionar avaliação: {str(e)}")


@professionals_bp.route("/<professional_id>/reviews", methods=["GET"])
def get_professional_reviews(professional_id):
    """
    Obter avaliações de um profissional
    """
    try:
        if not ObjectId.is_valid(professional_id):
            abort(400, description="ID de profissional inválido")
        
        # Lógica de obtenção de avaliações (simulada)
        # reviews_collection = get_collection("avaliacoes_profissionais")
        # reviews = list(reviews_collection.find({"professional_id": professional_id}))
        
        return jsonify([]) # Retorno simulado
    except Exception as e:
        abort(500, description=f"Erro ao obter avaliações: {str(e)}")
