import os
import binascii
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import jwt

# Argon2id: The industry standard for brute-force resistance.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = os.getenv("AUTH_SECRET")
ALGORITHM = "HS256"


def verify_root_access(credentials_input: str) -> bool:
    """
    GLOBAL VALIDATOR (Hex-Shielded).
    Decodes the Hex identity from environment and performs a secure comparison.
    """
    hex_identity = os.getenv("ROOT_AUTH_KEY")

    if not hex_identity:
        return False

    try:
        # Hex Decoding: Removing the alphanumeric shield to get the raw Argon2 hash.
        raw_root_hash = binascii.unhexlify(hex_identity).decode("utf-8")
        return pwd_context.verify(credentials_input, raw_root_hash)
    except (binascii.Error, ValueError, Exception):
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    JWT Access Token Generator.
    Ensures tokens are timezone-aware and stateless.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
