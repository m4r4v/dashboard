import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import verify_root_credentials, create_access_token

logger = logging.getLogger("app")
router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    is_valid = verify_root_credentials(credentials.email, credentials.password)

    if not is_valid:
        logger.warning(f"ACCESO RECHAZADO: Intento de login para {credentials.email}")
        raise HTTPException(status_code=401, detail="Credenciales Inválidas")

    logger.info(f"SESIÓN INICIADA: Root conectado como {credentials.email}")
    access_token = create_access_token(data={"sub": credentials.email, "role": "root"})

    return {"access_token": access_token, "token_type": "bearer"}
