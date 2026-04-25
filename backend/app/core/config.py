import sys
import socket
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ValidationInfo

class Settings(BaseSettings):
    # --- 1. SEGURIDAD ---
    root_secret: str
    system_pepper: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # --- 2. IDENTIDAD Y LOGS ---
    node_id: str = socket.gethostname()
    log_buffer_size: int = 20

    # --- 3. PERSISTENCIA HÍBRIDA ---
    database_url: Optional[str] = None

    @field_validator("root_secret")
    @classmethod
    def validate_root_secret(cls, v: str, info: ValidationInfo) -> str:
        if len(v) != 128:
            print(f"FATAL: ROOT_SECRET debe tener 128 caracteres. Actual: {len(v)}")
            sys.exit(1)
        return v

    @property
    def final_database_url(self) -> str:
        if self.database_url:
            if self.database_url.startswith("postgresql://"):
                return self.database_url.replace(
                    "postgresql://", "postgresql+asyncpg://"
                )
            return self.database_url
        return "sqlite+aiosqlite:///./dashboard.db"

    # Docker inyecta las variables en el OS, Pydantic las toma automáticamente
    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()