import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.db import init_db
from api.routers.items import router as items_router
from api.routers.auth import (
    router as auth_router,
)  # <--- NUEVO: Módulo de Autenticación


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Ciclo de Vida de la Aplicación.
    Se ejecuta al iniciar (antes de recibir peticiones) y al apagar.
    """
    try:
        await init_db()
        print("✅ Database connection established and tables verified.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise e

    yield


def create_app() -> FastAPI:
    """
    Application Factory Pattern.
    """
    is_prod = os.getenv("NODE_ENV") == "production"

    app = FastAPI(
        title="dashboard-backend",
        version="1.0.0",
        docs_url=None if is_prod else "/docs",
        redoc_url=None,
        lifespan=lifespan,
    )

    # --- Configuración CORS ---
    origins_raw = os.getenv("FRONTEND_ORIGINS", "")
    origins = [origin.strip() for origin in origins_raw.split(",") if origin]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Registro de Rutas (Endpoints) ---

    # 1. Módulo Auth (Seguridad e Identidad)
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

    # 2. Módulo Items (Recursos de Negocio)
    app.include_router(items_router, prefix="/api/v1/items", tags=["items"])

    # Health Check
    @app.get("/")
    def health_check():
        return {"service": "dashboard-backend", "status": "ok"}

    return app


app = create_app()
