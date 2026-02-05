# Dashboard Backend Service

Microservicio API construido con **FastAPI** y gestionado por **Poetry**.

## 🔧 Stack Tecnológico

* **Runtime:** Python 3.11
* **Framework:** FastAPI
* **Package Manager:** Poetry
* **Linter:** Ruff

## 🚀 Comandos de Desarrollo

El servicio está diseñado para correr dentro de Docker, pero para gestión de dependencias local:

```bash
# Instalar dependencias
poetry install

# Ejecutar servidor (Hot Reload)
poetry run uvicorn api.main:app --reload
```

## 🏗️ Estructura

```text
backend/
├── pyproject.toml   # Definición de dependencias
├── api/
│   ├── main.py      # Application Factory & Rutas
│   └── __init__.py  # Paquete
```
