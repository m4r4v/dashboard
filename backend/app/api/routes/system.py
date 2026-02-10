from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def get_system_status():
    """
    Endpoint de paridad con systemStore.js.
    Define el estado 'online' que el frontend busca.
    """
    return {"status": "online", "api_version": "1.3.0", "mode": "stateless_root"}
