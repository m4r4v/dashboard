from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from argon2.low_level import hash_secret_raw, Type
import secrets
from app.config import settings

# ==============================================================================
# MÓDULO DE SEGURIDAD (RF-02, RF-03) - VERSIÓN DETERMINISTA
# ==============================================================================


def get_deterministic_salt() -> bytes:
    """
    Deriva un Salt de 16 bytes a partir del SYSTEM_PEPPER.
    Esto permite que el hash sea reproducbible (Stateless) sin base de datos.
    """
    # Tomamos los primeros 16 caracteres del pepper y aseguramos bytes
    return settings.system_pepper.encode()[:16].ljust(16, b"0")


def verify_root_credentials(email: str, password: str) -> bool:
    """
    RF-02: Verificación Criptográfica (Hex-128).
    """
    input_payload = f"{email}{password}".encode()

    try:
        # Generamos el hash en tiempo real usando el Pepper como Salt
        hashed_bytes = hash_secret_raw(
            secret=input_payload,
            salt=get_deterministic_salt(),
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=64,  # 64 bytes = 128 Hex chars
            type=Type.ID,
        )

        # Convertimos a Hex para comparar con ROOT_SECRET (que es Hex)
        hashed_hex = hashed_bytes.hex()

        # Comparación segura de tiempo constante
        return secrets.compare_digest(settings.root_secret, hashed_hex)

    except Exception as e:
        print(f"Auth Error: {e}")
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    RF-03: Emisión de Sesión (JWT con Pepper).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})

    dynamic_signing_key = f"{settings.root_secret}{settings.system_pepper}"

    encoded_jwt = jwt.encode(
        to_encode, dynamic_signing_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt
