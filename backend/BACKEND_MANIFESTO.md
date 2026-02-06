# Backend Manifesto

> **Estado:** 🚧 En Construcción
> **Stack:** FastAPI + SQLModel + AsyncPG
> **Documentación Hija:** [API Rules](./API_MANIFESTO.md), [Database Rules](./DATABASE_MANIFESTO.md), [Auth Rules](./AUTH_MANIFESTO.md)

## 1. Arquitectura Modular

El backend se divide estrictamente en "Routers" aislados. Prohibido código monolítico en `main.py`.

### Módulos Activos

* **[✅] Items:** Gestión de inventario (CRUD Completo).
  * *Estado:* Operativo (`/api/v1/items`).
  * *Dependencias:* `db.py`, `models.py`.

* **[✅] Auth:** Sistema de Identidad Stateless (JWT).
  * *Estado:* Operativo (`/api/v1/auth`).
  * *Dependencias:* `security.py`, `routers/auth.py`.
  * *Estrategia:* Zero Knowledge (Argon2 + Variables de Entorno) + Stateless Root.

### Módulos Planificados

* (Vacío por ahora - Próximos módulos se definirán aquí)

## 2. Política de Seguridad (Nuevo)

> **Regla de Oro:** "Zero Trust" para operaciones de escritura.

1. **Público:** `GET` (Lectura) puede ser público (según caso de uso).
2. **Privado:** `POST`, `PUT`, `DELETE` **SIEMPRE** requieren autenticación.
3. **Token:** Se usará `Bearer Token` (JWT) con expiración corta.
4. **Hashing:** Passwords nunca se guardan en texto plano (Usar `Argon2` obligatoriamente).

## 3. Flujo de Desarrollo (Regla de Oro)

1. Actualizar Manifesto.
2. Definir Modelos (DTOs).
3. Implementar Router.
4. Registrar en `main.py`.
