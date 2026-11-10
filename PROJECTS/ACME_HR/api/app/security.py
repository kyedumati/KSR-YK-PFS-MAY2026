import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException

MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    validate_password(password)
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def validate_password(password: str) -> None:
    if password == "":
        raise HTTPException(status_code=422, detail="Password is required.")
    if len(password.encode()) > MAX_PASSWORD_BYTES:
        raise HTTPException(status_code=422, detail="Password is too long.")

def verify_password(password: str, password_hash: str) -> bool:
    if len(password.encode()) > MAX_PASSWORD_BYTES:
        return False
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def jwt_secret() -> str:
    secret = os.environ.get("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is not set")
    return secret


def token_minutes() -> int:
    return int(os.environ.get("ACCESS_TOKEN_MINUTES", "480"))


def create_access_token(*, employee_id: int, role: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=token_minutes())
    payload = {"sub": str(employee_id), "role": role, "exp": expires}
    return jwt.encode(payload, jwt_secret(), algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, jwt_secret(), algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Sign-in is required.")
