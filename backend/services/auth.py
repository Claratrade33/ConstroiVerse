import jwt
import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta-constroiverse')

# 🔐 Criptografa senha
def hash_password(senha_plana):
    return bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 🔍 Verifica senha
def verify_password(senha_plana, senha_hash):
    return bcrypt.checkpw(senha_plana.encode('utf-8'), senha_hash.encode('utf-8'))

# 🎫 Gera token JWT
def generate_token(user):
    payload = {
        'id': user.id,
        'email': user.email,
        'perfil': user.perfil,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# ✅ Decodifica e valida token
def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None