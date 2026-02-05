# Gobernanza Backend

> **Estado:** Activo
> **Fuente Legal:** `backend/BACKEND_MANIFESTO.md`

## 1. Stack Tecnológico

* **Lenguaje:** Python 3.11 (Slim)
* **Framework:** FastAPI
* **Gestor:** Poetry (Estricto)
* **Linter:** Ruff

## 2. Infraestructura

* **Servicio:** `dashboard-backend`
* **Ruta de Código:** `backend/api/`

## 3. Protocolo de Inicialización

* **Factory:** Uso de `create_app()`.
* **Identidad:** El título en Swagger debe ser **`dashboard-backend`**.

## 4. Integración

* **CORS:** Restringido al origen del Frontend.
* **Docs:** Swagger habilitado en Desarrollo.
