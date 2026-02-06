# Arquitectura de Base de Datos

> **Estado:** Operativo (Hito 3)
> **Stack:** PostgreSQL 16 (Alpine) + Asyncpg + SQLModel

## 1. Topología de Conexión

El servicio utiliza una arquitectura **estrictamente asíncrona** para comunicarse con PostgreSQL. Esto evita que el bucle de eventos de FastAPI se bloquee esperando respuestas de la base de datos (I/O Bound).

### Componentes Clave (`api/db.py`)

1.  **Motor Asíncrono (`AsyncEngine`):**
    Utilizamos `create_async_engine` con el driver `postgresql+asyncpg`.
    * *Configuración:* `echo=True` (Logs SQL en consola) y `future=True` (Compatibilidad v2.0).
    * *Pooling:* Gestionado nativamente por SQLAlchemy para reutilizar conexiones.

2.  **Sesión (`AsyncSession`):**
    No nos conectamos manualmente. Usamos `sessionmaker` para generar fábricas de sesiones.
    * `expire_on_commit=False`: Vital para que los objetos de SQLModel sigan accesibles después de guardar cambios.

### Inyección de Dependencias

Para usar la base de datos en un endpoint, nunca instanciamos la conexión directamente. Usamos el sistema de Dependencias de FastAPI (`Depends`):

```python
# Patrón de uso en Endpoints
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import get_session

@app.get("/items")
async def read_items(session: AsyncSession = Depends(get_session)):
    # La sesión se crea al entrar y se cierra automáticamente al salir
    results = await session.exec(...)
```

## 2. Ciclo de Vida (Lifespan Protocol)

Abandonamos los eventos heredados (`startup`/`shutdown`) en favor del estándar moderno **Lifespan** definido en `api/main.py`.

### Flujo de Arranque (Fail-Fast)

1.  **Inicio del Contenedor:** Uvicorn carga `main.py`.
2.  **Ejecución de Lifespan:** Antes de aceptar la primera petición HTTP (`yield`), se ejecuta `init_db()`.
3.  **Verificación:**
    * El sistema intenta conectar a PostgreSQL.
    * Verifica/Crea las tablas definidas en `SQLModel.metadata`.
4.  **Decisión Crítica:**
    * ✅ **Éxito:** La API arranca y comienza a servir tráfico.
    * ❌ **Fallo:** Si la credencial es errónea o la BD no responde, la excepción sube y **detiene el contenedor**. Esto previene despliegues "zombies" (servicios corriendo pero desconectados).

## 3. Variables de Entorno

La conexión es totalmente configurada vía *Environment Variables* (12-Factor App).

| Variable | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `DATABASE_URL` | Connection String completa | `postgresql+asyncpg://user:pass@host:5432/db` |