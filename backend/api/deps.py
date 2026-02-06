import os
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from api.security import ALGORITHM

# 1. El Extractor
# Esta utilidad busca automáticamente el header "Authorization: Bearer <token>"
# y extrae el string del token. También le dice a Swagger UI dónde enviar el token.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"  # La URL donde se consiguen los tokens
)


def get_current_user(token: str = Depends(reusable_oauth2)) -> dict:
    """
    El Guardián (Dependency).
    1. Recibe el token del Request.
    2. Verifica la firma criptográfica usando el AUTH_SECRET.
    3. Verifica que no haya expirado.
    4. Retorna los datos del usuario (Payload) si todo está bien.
    """
    secret_key = os.getenv("AUTH_SECRET")

    # Excepción estándar para problemas de autenticación
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # A. Decodificación y Validación de Firma
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])

        # B. Validación de Identidad (Claims)
        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None or role != "superadmin":
            raise credentials_exception

        # Si llegamos aquí, el token es legítimo
        return {"username": email, "role": role}

    except (JWTError, ValidationError):
        # Si la firma no coincide o el token está corrupto
        raise credentials_exception
