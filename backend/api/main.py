from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.db import init_db
from api.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    STARTUP PROTOCOL.
    Ensures database readiness before accepting traffic.
    """
    await init_db()
    yield


app = FastAPI(title="Backbone Matrix API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standardized API Routing (No special characters)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])


@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "message": "Backbone Matrix is active",
        "engine": "Hybrid (SQLite/Postgres)",
    }
