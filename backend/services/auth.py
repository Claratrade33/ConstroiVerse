import os, datetime, bcrypt, jwt
from sqlalchemy.orm import Session
from backend.models.user import User

SECRET = os.getenv("SECRET_KEY", "change-me")
EXPIRES = int(os.getenv("JWT_EXPIRES", "3600"))

def hash_password(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def verify_password(pwd: str, hashed: str) -> bool:
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def generate_token(user_id: int) -> str:
    now = datetime.datetime.utcnow()
    payload = {"sub": user_id, "iat": now, "exp": now + datetime.timedelta(seconds=EXPIRES)}
    return jwt.encode(payload, SECRET, algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])

def register(db: Session, name: str, email: str, password: str):
    if db.query(User).filter_by(email=email).first():
        raise ValueError("E-mail já cadastrado")
    u = User(name=name, email=email, password_hash=hash_password(password))
    db.add(u)
    db.flush()
    return u

def login(db: Session, email: str, password: str):
    u = db.query(User).filter_by(email=email).first()
    if not u or not verify_password(password, u.password_hash):
        raise ValueError("Credenciais inválidas")
    return generate_token(u.id)