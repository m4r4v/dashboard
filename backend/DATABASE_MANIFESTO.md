# DATABASE MANIFESTO
>
> **Ámbito:** Persistencia y Modelado de Datos
> **Versión:** 1.0.0
> **Stack:** PostgreSQL + SQLModel + Alembic

## 1. Tecnologías Base

1. **Motor:** PostgreSQL 16-alpine (Imagen Docker oficial).
2. **ORM:** SQLModel (Unificación de Pydantic + SQLAlchemy).
3. **Driver:** `asyncpg` (Asíncrono estricto para FastAPI).
4. **Migraciones:** Alembic (Control de versiones de esquema).

## 2. Estrategia de Conexión

1. **String de Conexión:** Prohibido hardcodear credenciales. Se inyectarán vía variable de entorno `DATABASE_URL`.
2. **Pooling:** Se utilizará el pool de conexiones nativo de SQLAlchemy/Asyncpg para evitar saturación.

## 3. Política de Cambios (Migraciones)

1. **Inmutabilidad:** Prohibido modificar tablas manualmente (SQL directo) en producción.
2. **Flujo de Trabajo:**
   * Modificar modelo en Python (`models.py`).
   * Generar migración: `alembic revision --autogenerate -m "mensaje"`.
   * Aplicar: `alembic upgrade head`.

## 4. Persistencia

* **Volumen Docker:** Los datos residen en el host en `./database/data`.
* **Seguridad:** La carpeta de datos debe estar ignorada en `.gitignore`.
