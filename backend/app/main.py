from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from app.core.config import settings
from app.api.routes import auth, system


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida del motor de base de datos."""
    engine = create_async_engine(settings.final_database_url)
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
    finally:
        await engine.dispose()
    yield


app = FastAPI(
    title="Dashboard Backend", version="1.3.0", lifespan=lifespan, docs_url="/api/docs"
)

# CORS Configurado para comunicación local/docker
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas estandarizadas
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(system.router, prefix="/api/system", tags=["System"])


@app.get("/health")
async def health():
    """Infra-check (Docker/K8s)"""
    return {"status": "active"}
