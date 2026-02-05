import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# 1. Configuración de la Conexión
# Leemos la URL inyectada por Docker Compose.
# Si falla, es mejor que explote ahora y no silenciosamente.
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL env var is missing")

# 2. Creación del Motor (Engine)
# echo=True permite ver las consultas SQL en los logs (útil para dev)
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


# 3. Inicialización de la DB (Tablas)
async def init_db():
    """
    Crea las tablas definidas en los modelos de SQLModel.
    Nota: En producción, esto se suele reemplazar por Alembic.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # Solo para reset total
        await conn.run_sync(SQLModel.metadata.create_all)


# 4. Dependency Injection para FastAPI
async def get_session() -> AsyncSession:
    """
    Generador de sesiones asíncronas.
    Se usa en los endpoints: session: AsyncSession = Depends(get_session)
    """
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
