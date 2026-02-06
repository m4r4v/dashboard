from typing import Optional
from sqlmodel import Field, SQLModel


# 1. Base (Mixin): Datos compartidos
class ItemBase(SQLModel):
    name: str
    description: Optional[str] = None


# 2. Table (DB): Representación física en PostgreSQL
class Item(ItemBase, table=True):
    # 'default=None' es necesario para que la BD asigne el ID autoincremental
    id: Optional[int] = Field(default=None, primary_key=True)


# 3. Create (Input): Validación estricta de lo que entra
class ItemCreate(ItemBase):
    pass
    # Aquí podríamos agregar campos extra que solo sirven al crear
    # pero que no se guardan en la tabla base.


# 4. Read (Output): Sanitización estricta de lo que sale
class ItemRead(ItemBase):
    id: int
