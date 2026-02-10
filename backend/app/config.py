import os
import sys
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo

# ==============================================================================
# CONFIGURACIÓN CENTRALIZADA (RF-05, RF-04)
# ==============================================================================


class Settings(BaseSettings):
    # --- 1. SEGURIDAD (RF-01, RF-02, RF-03) ---
    root_secret: str
    system_pepper: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # --- 2. PERSISTENCIA HÍBRIDA (RF-06, RF-07) ---
    # Si viene vacío del .env, asumimos modo local (SQLite)
    database_url: Optional[str] = None

    @field_validator("root_secret")
    @classmethod
    def validate_root_secret(cls, v: str, info: ValidationInfo) -> str:
        """
        RF-04: Fail-Safe. Verifica que el secreto sea Hexadecimal de 128 caracteres.
        """
        if len(v) != 128:
            print(
                f"FATAL: ROOT_SECRET debe tener 128 caracteres (Hex). Actual: {len(v)}"
            )
            sys.exit(1)
        try:
            int(v, 16)  # Verifica que sea hex válido
        except ValueError:
            print("FATAL: ROOT_SECRET contiene caracteres no hexadecimales.")
            sys.exit(1)
        return v

    @property
    def final_database_url(self) -> str:
        """
        Lógica de decisión Híbrida (RF-06 vs RF-07).
        Retorna la URL de conexión asíncrona definitiva.
        """
        if self.database_url:
            # RF-07: Estrategia Cloud (PostgreSQL)
            # Aseguramos usar el driver asíncrono si el usuario puso 'postgresql://'
            if self.database_url.startswith("postgresql://"):
                return self.database_url.replace(
                    "postgresql://", "postgresql+asyncpg://"
                )
            return self.database_url

        # RF-06: Estrategia Local (SQLite Asíncrono)
        # Se crea en /workspace/dashboard.db (dentro del contenedor)
        return "sqlite+aiosqlite:///./dashboard.db"

    class Config:
        env_file = ".env"
        # Ignoramos variables extra para evitar errores con comentarios o vars de sistema
        extra = "ignore"


# Instancia Global (Singleton)
settings = Settings()
