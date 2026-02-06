# Dashboard Project

> **Estado:** 🟡 En Auditoría (Hito 8)
> **Stack:** FastAPI + SQLModel + AsyncPG + Vue3
> **Seguridad:** Zero Trust / Stateless Root (Argon2 + JWT)

## 📋 Resumen de Situación

El proyecto se encuentra en una fase de **Consolidación y Auditoría**. Se han detenido los desarrollos de nuevas funcionalidades para verificar la solidez de la arquitectura base (Microservicios, Auth, Estado).

## 🚀 Inicio Rápido

### 1. Levantar Infraestructura

```bash
docker compose up -d
```

### 2. Verificar Servicios

- **Frontend:** <http://localhost:3000> (Login requerido)
- **API Docs:** <http://localhost:8000/docs>
- **Health Check:** `curl http://localhost:8000/`

## 📍 Gobernanza (Manifestos)

Las reglas del juego son inmutables y deben auditarse constantemente.

- **[Frontend Rules](./frontend/FRONTEND_MANIFESTO.md)**
- **[Backend Rules](./docs/backend/backend_manifesto.md)** (Pendiente de mover)
- **[Security Rules](./docs/backend/auth.md)**

## 📅 Hoja de Ruta (Roadmap)

### Fase 1: Cimentación (Completada)

* [x] **Hito 0:** Configuración de Docker y Entorno.
- [x] **Hito 1:** Integración Frontend-Backend.
- [x] **Hito 2:** Inicialización del Backend.
- [x] **Hito 3:** Base de Datos y Modelos.
- [x] **Hito 4:** API RESTful (Items).
- [x] **Hito 5:** Seguridad (Auth Zero Trust).
- [x] **Hito 6:** Integración UI (Login).
- [x] **Hito 7:** UI Funcional (Inventario).

### Fase 2: Consolidación (Actual)

* [ ] **Hito 8:** Auditoría Técnica Integral.
  - [ ] Performance & Resiliencia.
  - [ ] Seguridad & Compliance.
  - [ ] Arquitectura de Datos.
- [ ] **Hito 9:** Documentación Maestra (VitePress).
  - [ ] Actualización de guías.
  - [ ] Referencia de API y Componentes.

### Fase 3: Expansión (Futuro)

* [ ] **Hito 10:** Diseño UI/UX y Dashboard (Dependencias).
