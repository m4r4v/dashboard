import os
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt

# 1. Configuración Criptográfica (Argon2)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 2. Configuración JWT
SECRET_KEY = os.getenv("AUTH_SECRET")
ALGORITHM = "HS256"

def verify_root_access(email: str, password: str) -> bool:
    """
    Validación Ciega (Zero Knowledge):
    El sistema no sabe cuál es el email del SuperAdmin.
    Solo sabe que: Hash(Input + Secret) debe ser igual a ROOT_AUTH_HASH.
    """
    root_hash = os.getenv("ROOT_AUTH_HASH")
    system_secret = os.getenv("AUTH_SECRET")

    if not root_hash or not system_secret:
        return False

    # Reconstrucción de la Fórmula: Input + Pepper
    # No filtramos por email. Si el email está mal, el hash dará diferente.
    raw_input = f"{email}{password}{system_secret}"

    # Verificación Criptográfica
    try:
        return pwd_context.verify(raw_input, root_hash)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # ... (Misma lógica de token que antes) ...
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt