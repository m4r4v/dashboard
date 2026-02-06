# Modelado de Datos (SQLModel)

> **Estándar:** SQLModel (SQLAlchemy Core + Pydantic)
> **Convención:** Code-First

## 1. Estructura Base de un Modelo

Cada tabla en la base de datos se representa como una clase en Python que hereda de `SQLModel`.

### Reglas de Definición

1. **Herencia:** Debe heredar de `SQLModel`.
2. **Tabla:** Debe incluir `table=True` si es una entidad persistente.
3. **Tipado:** Uso estricto de type hints de Python (`int`, `str`, `Optional`).
4. **Claves Primarias:** Siempre deben tener un campo `id` explícito.

```python
from typing import Optional
from sqlmodel import Field, SQLModel

class Item(SQLModel, table=True):
    # 'default=None' es necesario para que sea autoincremental en DB pero opcional en Python antes de guardar
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    is_active: bool = Field(default=True)
```

## 2. Patrón de Separación (DTOs vs Tablas)

Para evitar exponer datos sensibles (como passwords) o recibir datos basura, usamos modelos separados (Herencia):

* **Base Model:** Campos compartidos (ej: `ItemBase`).
* **Table Model:** Hereda de Base + `table=True` (Lo que va a la BD).
* **Create DTO:** Hereda de Base (Lo que el usuario envía para crear).
* **Read DTO:** Hereda de Base + `id` (Lo que la API devuelve).

## 3. Ubicación

Los modelos deben residir en `backend/api/models.py` (o en una carpeta `models/` si el proyecto crece).
