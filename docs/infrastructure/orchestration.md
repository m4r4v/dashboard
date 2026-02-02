# Orquestación de Contenedores

> **Estado:** Activo
> **Implementación:** `root/docker-compose.yaml`

## 1. Estrategia Global

El proyecto utiliza Docker Compose como orquestador único para el entorno de desarrollo. La arquitectura prioriza la **inmutabilidad de las imágenes** frente a la **persistencia del código fuente** en el host.

## 2. Definición de Servicios

### 2.1 Frontend (`dashboard-frontend`)

* **Imagen Base:** `m4r4v/frontend:latest` (Docker Hub).
* **Estrategia de Volúmenes:**
  * `Host: ./frontend/app` -> `Container: /workspace/app`
  * *Propósito:* Permitir la edición de código en tiempo real desde el Host mientras la ejecución ocurre en el Container.
* **Networking:**
  * Puerto: `3000:3000` (Vite Dev Server).
  * Modo: Host (`--host`) requerido para exposición externa.
* **Ciclo de Vida:**
  * El contenedor no muere tras la ejecución; mantiene el servidor de desarrollo activo (`pnpm dev`).

## 3. Comandos Operativos

* **Iniciar Entorno:** `docker compose up`
* **Reconstruir (si cambia el Dockerfile):** No aplica (las imágenes se bajan de Hub).
* **Entrar al contenedor:** `docker exec -it dashboard-frontend sh`
