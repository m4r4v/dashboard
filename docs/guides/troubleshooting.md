# Guía de Resolución de Problemas (Troubleshooting)

Bitácora de errores conocidos y soluciones validadas para el entorno de desarrollo.

## Frontend

### 1. Pantalla Negra / "No match found for location"

**Síntoma:** Al crear un nuevo archivo en `src/pages/`, el navegador muestra pantalla negra y la consola dice `[Vue Router warn]: No match found`.
**Causa:** El plugin `unplugin-vue-router` pierde la sincronización con la caché de Vite persistida en el volumen de Docker.
**Solución:**

```bash
# 1. Detener el contenedor
docker compose stop frontend

# 2. Purgar la caché de Vite (Desde el host)
rm -rf frontend/app/node_modules/.vite

# 3. Reiniciar
docker compose up -d frontend
```

### 2. Error "Cannot read properties of null" en SysCheck

**Síntoma:** El componente crashea inmediatamente al cargar.
**Causa:** Renderizado prematuro del template antes de que la promesa `fetch` termine.
**Solución:** Asegurar que los bloques `v-if` / `v-else-if` cubran todos los estados de carga y usar Optional Chaining o guardas (`v-if="data"`) antes de leer propiedades.

## Backend

### 1. Error "poetry.lock is not consistent" durante el Build

**Síntoma:** Al ejecutar `docker compose build`, el proceso falla en el paso `RUN poetry install` con el error `Warning: poetry.lock is not consistent with pyproject.toml`.
**Causa:** Se modificó `pyproject.toml` en el host, pero el archivo `poetry.lock` no se regeneró.
**Solución (Regeneración Quirúrgica):**

```bash
docker run --rm -v "$(pwd)/backend:/workspace" -w /workspace python:3.11-slim \
  /bin/sh -c "pip install poetry && poetry lock"
```

Una vez regenerado, reconstruir: `docker compose up -d --build backend`

## Infraestructura

### 1. Error "Network not found" al levantar Backend

**Síntoma:** `failed to set up container networking: network ... not found`.
**Causa:** El contenedor estaba detenido y referenciaba una red Docker antigua que fue recreada por otro servicio.
**Solución:** Eliminar el contenedor huérfano para forzar su recreación.

```bash
docker rm -f dashboard-backend
docker compose up -d backend
```
