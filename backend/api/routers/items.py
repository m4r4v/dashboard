from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from api.db import get_session
from api.models import Item, ItemCreate, ItemRead
from api.deps import get_current_user  # <--- Importación del Guardián

router = APIRouter()

# --- RUTAS PÚBLICAS (Lectura) ---

@router.get("/", response_model=list[ItemRead])
async def read_items(session: AsyncSession = Depends(get_session)):
    """
    Obtiene la lista completa de registros.
    - Acceso: PÚBLICO
    """
    result = await session.execute(select(Item))
    items = result.scalars().all()
    return items

@router.get("/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    """
    Obtiene un registro específico por ID.
    - Acceso: PÚBLICO
    """
    item = await session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# --- RUTAS PROTEGIDAS (Escritura - Requieren Token) ---

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate, 
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user) # <--- CANDADO ACTIVADO
):
    """
    Crea un nuevo registro.
    - Acceso: PRIVADO (Requiere Token SuperAdmin)
    """
    db_item = Item.model_validate(item)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

@router.put("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int, 
    item_data: ItemCreate, 
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user) # <--- CANDADO ACTIVADO
):
    """
    Actualiza un registro existente.
    - Acceso: PRIVADO (Requiere Token SuperAdmin)
    """
    db_item = await session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data_dict = item_data.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data_dict)

    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user) # <--- CANDADO ACTIVADO
):
    """
    Elimina un registro.
    - Acceso: PRIVADO (Requiere Token SuperAdmin)
    """
    db_item = await session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    await session.delete(db_item)
    await session.commit()
    return None