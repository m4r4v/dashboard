# BACKEND MANIFESTO
>
> **Ámbito:** API & Lógica de Negocio
> **Versión:** 1.0.0
> **Dependencias:** ROOT MANIFESTO

## 1. Definición del Stack Tecnológico

1. **Lenguaje:** Python 3.11 (Slim Bookworm/Alpine).
2. **Framework:** FastAPI (Última versión estable).
3. **Gestor de Paquetes:** **Poetry** (Estricto).
    * Uso prohibido de `pip install` manual.
    * Archivo de verdad: `pyproject.toml`.
4. **Calidad de Código:** **Ruff**.
    * Debe actuar como Linter y Formatter (Zero Config).

## 2. Infraestructura y Entorno

1. **Imagen Base:** `python:3.11-slim`.
2. **Estructura de Directorios:**
    * `backend/` (Raíz del servicio, contiene `pyproject.toml`).
    * `backend/api/` (Código fuente Python).
3. **Modelo de Persistencia (Docker):**
    * **Host:** `./backend:/workspace` (Montaje de raíz para acceso a configs).
    * **Working Dir:** `/workspace`.
    * **Python Path:** Configurado para reconocer `api` como módulo.

## 3. Protocolo de Inicialización

1. **Application Factory:** Uso obligatorio de patrón Factory (`create_app`) en `api/main.py`.
2. **Identidad:** El nombre del proyecto en configuraciones (OpenAPI/Swagger) será estrictamente **`dashboard-backend`**.

## 4. Estándares de Integración

1. **CORS:** Restringido explícitamente al origen del Frontend (según env var).
2. **Documentación:** `/docs` (Swagger) habilitado en entorno DEV.
