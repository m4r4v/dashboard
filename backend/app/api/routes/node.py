import logging
import psutil
import time
from datetime import datetime
from collections import deque
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import PlainTextResponse
from app.core.config import settings
from app.core.security import get_current_root
from app.api.routes.system import check_db_health

router = APIRouter()
event_logs = deque(maxlen=settings.log_buffer_size)

# --- RECOLECTOR DE LOGS (RESTABLECIDO) ---
class InMemoryLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        event_logs.append(log_entry)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO) # Vital para capturar AUDIT
if not any(isinstance(h, InMemoryLogHandler) for h in logger.handlers):
    logger.addHandler(InMemoryLogHandler())

@router.get("/metrics", response_class=PlainTextResponse)
async def get_metrics(request: Request, current_root: dict = Depends(get_current_root)):
    db_status = await check_db_health()
    c_4xx = getattr(request.app.state, "http_errors_4xx", 0)
    c_5xx = getattr(request.app.state, "http_errors_5xx", 0)
    
    metrics = [
        f'http_errors_total{{code="4xx",node="{settings.node_id}"}} {c_4xx}',
        f'http_errors_total{{code="5xx",node="{settings.node_id}"}} {c_5xx}',
        f'node_database_status{{node="{settings.node_id}"}} {db_status}'
    ]
    return "\n".join(metrics)

@router.get("/status")
async def get_node_status(current_root: dict = Depends(get_current_root)):
    process = psutil.Process()
    return {
        "node_id": settings.node_id,
        "status": "active",
        "uptime_seconds": time.time() - process.create_time(),
        "memory_usage_mb": process.memory_info().rss / 1024 / 1024
    }

@router.get("/logs")
async def get_node_logs(current_root: dict = Depends(get_current_root)):
    return list(event_logs)

@router.post("/action")
async def execute_node_action(action: str, current_root: dict = Depends(get_current_root)):
    logger.info(f"NODE_ACTION: {action}")
    return {"msg": "OK"}