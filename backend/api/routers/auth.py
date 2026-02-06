from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from api.security import verify_root_access, create_access_token

router = APIRouter()

# --- Modelos de Datos (DTOs) ---


class Token(BaseModel):
    """
    Estructura de la respuesta exitosa (Standard OAuth2).
    """

    access_token: str
    token_type: str


# --- Endpoints ---


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    Endpoint Estándar OAuth2.

    - Content-Type: application/x-www-form-urlencoded
    - Fields: username, password (client_id, client_secret, etc. opcionales)
    """

    # 1. Validación Criptográfica
    # Mapeamos 'form_data.username' a nuestro concepto de 'email'.
    # El estándar OAuth2 usa 'username' genérico, nosotros usamos email como identificador.
    is_valid = verify_root_access(form_data.username, form_data.password)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas o acceso denegado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Generación del Token
    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={
            "sub": form_data.username,  # Subject: Email
            "role": "superadmin",  # Scope: Root
        },
        expires_delta=access_token_expires,
    )

    # 3. Entrega del Token
    return {"access_token": access_token, "token_type": "bearer"}
