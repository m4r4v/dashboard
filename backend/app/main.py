import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.core.database import sessionmanager
from app.api.routes import auth, system, node

logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_errors_4xx = 0
    app.state.http_errors_5xx = 0

    sessionmanager.init_db(settings.final_database_url)

    try:
        async with sessionmanager.session() as session:
            await session.execute(text("SELECT 1"))
        logger.info(f"NODE_ONLINE: {settings.node_id}")
    except Exception as e:
        logger.error(f"NODE_DEGRADED: {e}")

    yield
    
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(title="Stateless Dashboard", version="1.4.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)

@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    response = await call_next(request)
    path = request.url.path

    if not any(x in path for x in ["/logs", "/metrics"]) and request.method != "OPTIONS":
        logger.info(f"AUDIT: {request.method} {path} -> {response.status_code}")
        
        if 400 <= response.status_code < 500:
            request.app.state.http_errors_4xx += 1
        elif response.status_code >= 500:
            request.app.state.http_errors_5xx += 1

    return response

app.include_router(auth.router, prefix="/api/auth")
app.include_router(system.router, prefix="/api/system")
app.include_router(node.router, prefix="/api/node")