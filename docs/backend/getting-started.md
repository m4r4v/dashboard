# Primeros Pasos (Backend)

Guía para inicializar y ejecutar el entorno de desarrollo del Backend.

## 1. Inicialización del Proyecto

El proyecto utiliza **Poetry** sobre Docker. La estructura base se mantiene sincronizada mediante `pyproject.toml` y `poetry.lock`.

## 2. Ejecución Automática (Development)

El servicio `dashboard-backend` está configurado para instalar dependencias y levantar el servidor automáticamente al iniciar el stack.

### Comandos de Rutina

```bash
# Iniciar todo el stack (Frontend + Backend + Docs)
docker compose up -d

# Ver logs del backend (útil para debug)
docker logs -f dashboard-backend
