import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import verify_root_credentials, create_access_token

logger = logging.getLogger("app")
router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str
    honeypot: str = ""  # campo señuelo del form; un humano nunca lo llena


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    # [CORREGIDO] El honeypot ya existía en el frontend pero nunca se validaba
    # acá — un bot que ignorase el JS y pegara directo a este endpoint lo
    # esquivaba por completo. Misma respuesta que credenciales inválidas, sin
    # distinguir el motivo, para no darle información al bot.
    if credentials.honeypot:
        logger.warning(f"BOT DETECTADO: honeypot lleno en intento de login ({credentials.email})")
        raise HTTPException(status_code=401, detail="Credenciales Inválidas")

    is_valid = verify_root_credentials(credentials.email, credentials.password)

    if not is_valid:
        logger.warning(f"ACCESO RECHAZADO: Intento de login para {credentials.email}")
        raise HTTPException(status_code=401, detail="Credenciales Inválidas")

    logger.info(f"SESIÓN INICIADA: Root conectado como {credentials.email}")
    access_token = create_access_token(data={"sub": credentials.email, "role": "root"})

    return {"access_token": access_token, "token_type": "bearer"}
