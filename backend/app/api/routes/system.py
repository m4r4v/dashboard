from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import sessionmanager

router = APIRouter()

async def check_db_health() -> int:
    """Usa el sessionmanager ya inicializado en el lifespan de main.py, no
    request.app.state.engine (nunca se asignaba ahí -> AttributeError en producción)."""
    try:
        async with sessionmanager.session() as session:
            await session.execute(text("SELECT 1"))
        return 1
    except Exception:
        return 0

@router.get("/status")
async def get_system_status():
    db_ok = await check_db_health()
    return {"status": "online" if db_ok else "degraded", "api_version": "1.3.4"}