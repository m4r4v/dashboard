# Infraestructura y Despliegue

El proyecto se ejecuta sobre un stack contenerizado gestionado por Docker Compose.

## Definición del Stack

* [Orquestador (docker-compose.yaml)](../../docker-compose.yaml)
  * *Definición de servicios, redes y volúmenes.*

### Servicios

1. **Frontend:** `m4r4v/frontend:latest` (Puerto 3000)
2. **Backend:** Python 3.11 Slim + Poetry (Puerto 8000)
3. **Docs:** Vitepress (Puerto 5173)

## Comandos de Rutina

### Gestión del Ciclo de Vida

```bash
# Iniciar todo el sistema (Detached)
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f

# Reiniciar un servicio específico (ej: backend)
docker compose restart backend

# Destruir y limpiar volúmenes (Cuidado: borra DBs)
docker compose down -v
```

### Variables de Entorno Críticas

* `VITE_API_URL`: Dirección del Backend para el Frontend.
* `FRONTEND_ORIGINS`: Lista blanca de CORS en el Backend.
