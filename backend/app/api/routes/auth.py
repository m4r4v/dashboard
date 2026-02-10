from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import verify_root_credentials, create_access_token

# Cambiamos el nombre del tag a 'Auth' para consistencia total
router = APIRouter(tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """
    Endpoint de autenticación bajo estándar Stateless Root.
    """
    is_valid = verify_root_credentials(credentials.email, credentials.password)

    if not is_valid:
        raise HTTPException(
            status_code=401, detail="Credenciales Inválidas (Root Check Failed)"
        )

    access_token = create_access_token(data={"sub": credentials.email, "role": "root"})

    return {"access_token": access_token, "token_type": "bearer"}
