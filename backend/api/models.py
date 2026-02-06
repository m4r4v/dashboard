from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class ItemBase(SQLModel):
    """
    EL CONTRATO (Atributos compartidos).
    Aquí definimos lo que es común tanto para crear como para leer.
    """

    title: str = Field(index=True)
    description: Optional[str] = None


class Item(ItemBase, table=True):
    """
    LA TABLA (Atributos de persistencia).
    'table=True' le dice a SQLModel que esto debe existir físicamente
    en SQLite o Postgres.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    # Añadimos un campo de auditoría para demostrar profesionalismo.
    # Usamos default_factory para que el servidor ponga la fecha automáticamente.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ItemCreate(ItemBase):
    """
    EL FILTRO DE ENTRADA.
    Lo que el desarrollador pide al Frontend que envíe.
    No incluimos el ID ni la fecha, porque el sistema los genera solo.
    """

    pass


class ItemPublic(ItemBase):
    """
    EL FILTRO DE SALIDA.
    Lo que el mundo exterior puede ver.
    """

    id: int
    created_at: datetime
