"""Utility functions for authentication and JWT token handling.

This module provides helpers to hash and verify passwords using the
`werkzeug.security` helpers from Flask, as well as to generate JWT
tokens for authenticated users. Tokens include the user's ID and role
and expire after 24 hours.
"""

import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from backend.config import SECRET_KEY

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)

def generate_token(user_id: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
