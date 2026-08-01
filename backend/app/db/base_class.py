import uuid
from datetime import datetime
from typing import Any
from sqlalchemy import DateTime, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    id: Any
    __name__: str

    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

class UUIDMixin:
    # Uuid genérico (SQLAlchemy 2.0+), no dialects.postgresql.UUID: el proyecto
    # también corre sobre SQLite en dev (RF-06), y el tipo específico de Postgres
    # no es portable entre dialectos.
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

class BaseModel(Base, UUIDMixin, TimestampMixin):
    __abstract__ = True