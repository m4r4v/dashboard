import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Ciclo de Vida de la Aplicación.
    Se ejecuta al iniciar (antes de recibir peticiones) y al apagar.
    """
    # 1. Startup: Intentar conexión a BD e inicializar tablas
    # Si init_db falla (ej: credenciales mal), la API no arranca.
    try:
        await init_db()
        print("✅ Database connection established and tables verified.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        # En producción, aquí podríamos decidir si hacer 'raise' para detener el contenedor
        # o permitir arranque degradado. Por ahora, dejamos que el error suba.
        raise e

    yield

    # 2. Shutdown: (Opcional) Cerrar pools o liberar recursos
    # print("🛑 Shutting down...")


def create_app() -> FastAPI:
    """
    Application Factory Pattern.
    Crea y configura la instancia de FastAPI.
    """
    # Lógica de entorno: Si es producción, ocultamos la documentación
    is_prod = os.getenv("NODE_ENV") == "production"

    app = FastAPI(
        title="dashboard-backend",
        version="1.0.0",
        docs_url=None if is_prod else "/docs",
        redoc_url=None,
        lifespan=lifespan,  # <--- Inyectamos el ciclo de vida aquí
    )

    # --- Configuración CORS (Defensive Networking) ---
    # Leemos la variable y limpiamos espacios para evitar errores de red
    origins_raw = os.getenv("FRONTEND_ORIGINS", "")
    origins = [origin.strip() for origin in origins_raw.split(",") if origin]

    # Si la lista está vacía en producción, esto es un riesgo o un error de config.
    # Por ahora permitimos el arranque, pero FastAPI bloqueará todo por defecto si origins está vacío.

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # ------------------------------------------------

    # Health Check (Contrato con Frontend/SysCheck)
    @app.get("/")
    def health_check():
        return {"service": "dashboard-backend", "status": "ok"}

    return app


# Punto de entrada para Uvicorn (Production Server)
app = create_app()
