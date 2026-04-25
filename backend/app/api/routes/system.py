from fastapi import APIRouter, Request
from sqlalchemy import text

router = APIRouter()

async def check_db_health(request: Request) -> int:
    try:
        async with request.app.state.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return 1
    except:
        return 0

@router.get("/status")
async def get_system_status(request: Request):
    db_ok = await check_db_health(request)
    return {"status": "online" if db_ok else "degraded", "api_version": "1.3.4"}