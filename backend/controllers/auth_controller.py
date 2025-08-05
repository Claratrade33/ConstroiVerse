from datetime import datetime, timedelta, UTC
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from backend.database import db
from backend.config import SECRET_KEY


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

PROFILES = {
    "arquiteto",
    "engenheiro",
    "loja",
    "fabricante",
    "representante",
    "corretor",
    "mestre",
    "pedreiro",
    "eletricista",
    "encanador",
    "cliente",
    "construtora",
}


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    main_profile = data.get("main_profile")
    if not email or not password or not main_profile:
        return {"erro": "Dados incompletos"}, 400
    if main_profile not in PROFILES:
        return {"erro": "Perfil inválido"}, 400
    if db.users.find_one({"email": email}):
        return {"erro": "Email já cadastrado"}, 409
    hashed_pw = generate_password_hash(password)
    db.users.insert_one({
        "email": email,
        "password": hashed_pw,
        "main_profile": main_profile,
    })
    return {"mensagem": "Usuário cadastrado"}, 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return {"erro": "Dados incompletos"}, 400
    user = db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return {"erro": "Credenciais inválidas"}, 401
    payload = {
        "sub": str(user["_id"]),
        "main_profile": user["main_profile"],
        "exp": datetime.now(UTC) + timedelta(hours=12),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"token": token, "main_profile": user["main_profile"]}
