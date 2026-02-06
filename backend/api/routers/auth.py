import os
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from api.security import verify_root_access, create_access_token

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    IDENTITY RECEPTION.
    Validates credentials against the deterministic environment key.
    """
    system_secret = os.getenv("AUTH_SECRET")

    # Deterministic Identity String (Email + Pass + Secret)
    credentials_to_check = f"{form_data.username}{form_data.password}{system_secret}"

    is_authorized = verify_root_access(credentials_to_check)

    if not is_authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matrix identity rejected.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Stateless Session Token Generation
    access_token = create_access_token(
        data={"sub": form_data.username, "role": "superadmin"}
    )

    return {"access_token": access_token, "token_type": "bearer"}
