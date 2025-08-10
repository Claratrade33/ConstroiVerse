from flask import Blueprint, request, jsonify
from sqlalchemy import asc, desc
from backend.utils.auth import jwt_required
from backend.models.user import User
from backend.database import get_db

user_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

@user_bp.get("/me")
@jwt_required
def me():
    u = request.user
    return jsonify({"id": u.id, "name": u.name, "email": u.email, "role": u.role})

@user_bp.get("")
@jwt_required
def list_users():
    db = next(get_db())
    q = db.query(User)
    sort = request.args.get("sort", "id")
    order = request.args.get("order", "asc")
    if hasattr(User, sort):
        q = q.order_by(asc(getattr(User, sort)) if order == "asc" else desc(getattr(User, sort)))
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 20))
    items = q.offset((page-1)*size).limit(size).all()
    data = [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in items]
    return jsonify({"data": data, "page": page, "size": size})