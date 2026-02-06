import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None


async def get_current_user(token: Annotated[str, Depends(reusable_oauth2)]):
    """
    SENTINEL PROTECTOR.
    Verifies the JWT token and ensures the 'superadmin' role exists.
    """
    secret_key = os.getenv("AUTH_SECRET")
    algorithm = "HS256"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Access denied.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role != "superadmin":
            raise credentials_exception

        token_data = TokenData(username=username, role=role)

    except JWTError:
        raise credentials_exception

    return token_data
