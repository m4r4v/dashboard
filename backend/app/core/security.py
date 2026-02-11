from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from argon2.low_level import hash_secret_raw, Type
import secrets
from app.core.config import settings

security = HTTPBearer()


def get_current_root(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Valida el JWT y asegura que el usuario tenga el rol 'root'.
    """
    token = credentials.credentials
    dynamic_signing_key = f"{settings.root_secret}{settings.system_pepper}"

    try:
        payload = jwt.decode(
            token, dynamic_signing_key, algorithms=[settings.jwt_algorithm]
        )
        role: str = payload.get("role")
        if role != "root":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Privilegios insuficientes",
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_deterministic_salt() -> bytes:
    return settings.system_pepper.encode()[:16].ljust(16, b"0")


def verify_root_credentials(email: str, password: str) -> bool:
    input_payload = f"{email}{password}".encode()
    try:
        hashed_bytes = hash_secret_raw(
            secret=input_payload,
            salt=get_deterministic_salt(),
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=64,
            type=Type.ID,
        )
        hashed_hex = hashed_bytes.hex()
        return secrets.compare_digest(settings.root_secret, hashed_hex)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    dynamic_signing_key = f"{settings.root_secret}{settings.system_pepper}"
    return jwt.encode(to_encode, dynamic_signing_key, algorithm=settings.jwt_algorithm)
