from flask import Blueprint, jsonify, request
from src.database import get_collection
from models.mongodb_models import Usuario
from bson import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    # users_collection = get_collection("usuarios")
    # users = list(users_collection.find({}))
    # for user in users:
    #     user["_id"] = str(user["_id"])
    return jsonify([{"_id": "simulated_id_1", "nome": "Simulated User 1", "email": "user1@sim.com"}, {"_id": "simulated_id_2", "nome": "Simulated User 2", "email": "user2@sim.com"}])


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    # users_collection = get_collection("usuarios")
    # new_user = Usuario(nome=data["nome"], email=data["email"], senha_hash=data["senha_hash"], tipo_usuario=data.get("tipo_usuario", "Cliente"))
    # result = users_collection.insert_one(new_user.to_dict())
    # new_user_dict = new_user.to_dict()
    # new_user_dict["_id"] = str(result.inserted_id)
    data["_id"] = "simulated_new_id"
    return jsonify(data), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # users_collection = get_collection("usuarios")
    # user = users_collection.find_one({"id": user_id})
    # if user:
    #     user["_id"] = str(user["_id"])
    #     return jsonify(user)
    return jsonify({"_id": f"simulated_id_{user_id}", "nome": f"Simulated User {user_id}", "email": f"user{user_id}@sim.com"}), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # users_collection = get_collection("usuarios")
    # data = request.json
    # updated_user = users_collection.find_one_and_update(
    #     {"id": user_id},
    #     {"$set": data},
    #     return_document=True
    # )
    # if updated_user:
    #     updated_user["_id"] = str(updated_user["_id"])
    #     return jsonify(updated_user)
    data["_id"] = f"simulated_id_{user_id}"
    return jsonify(data), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # users_collection = get_collection("usuarios")
    # result = users_collection.delete_one({"id": user_id})
    # if result.deleted_count == 1:
    return jsonify({"message": f"Usuário {user_id} deletado com sucesso (simulado)"}), 204
    # return jsonify({"message": "Usuário não encontrado"}), 404
