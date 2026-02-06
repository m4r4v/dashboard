# Dashboard Project

> **Estado:** 🟢 Operativo (Hito 7 Completado)
> **Stack:** FastAPI + SQLModel + AsyncPG + Vue3
> **Seguridad:** Zero Trust / Stateless Root (Argon2 + JWT)

## 📋 Resumen de Situación

El proyecto opera bajo una arquitectura de microservicios estricta.

- **Backend:** Expone una API RESTful con validación Pydantic y documentación automática.
- **Seguridad:** Implementa autenticación OAuth2 (Form Data) con tokens JWT.
- **Frontend:** SPA en Vue 3 con gestión de estado (Pinia) y enrutamiento protegido.

## 🚀 Inicio Rápido

### 1. Levantar Infraestructura

```bash
docker compose up -d
```

### 2. Verificar Servicios

- **Frontend:** <http://localhost:3000> (Redirige a Login si no hay sesión)
- **API Docs:** <http://localhost:8000/docs>
- **Health Check:** `curl http://localhost:8000/`

## 📍 Mapa de Navegación

- **[Frontend Governance](./frontend/FRONTEND_MANIFESTO.md):** Reglas de UI y Estado.
- **[Backend & Auth](./docs/backend/auth.md):** Guía de seguridad.
- **[Database](./docs/backend/database.md):** Modelos y conexión.

## 📅 Hoja de Ruta (Roadmap)

- [x] **Hito 0:** Configuración de Docker y Entorno.
- [x] **Hito 1:** Integración Frontend-Backend.
- [x] **Hito 2:** Inicialización del Backend (Factory Pattern).
- [x] **Hito 3:** Base de Datos (SQLModel + AsyncPG).
- [x] **Hito 4:** API Items (CRUD Completo).
- [x] **Hito 5:** Seguridad y Auth (JWT + Argon2 + Middleware).
- [x] **Hito 6:** Integración Frontend (Login + Router Guard).
- [x] **Hito 7:** Interfaz de Inventario (Items).
  - [x] **Paso 1:** Capa de Servicio.
  - [x] **Paso 2:** Capa de Estado (Pinia).
  - [x] **Paso 3:** UI Listado y CRUD (Items.vue).
- [ ] **Hito 8:** Integración de Navegación (Menú Lateral).

---
*Para detener el entorno:*
`docker compose down`
