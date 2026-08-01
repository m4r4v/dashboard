# TECHNICAL CONTEXT

> Fuente de verdad de la estructura real del proyecto, referenciada por `BEHAVIOR.md`.
> Antes vacío pese a esa referencia — corregido para que ambos archivos coincidan.

## Stack congelado
Ver `docs/architecture/REQUIREMENTS.md` §4 para el detalle completo (versiones, drivers).
Resumen: Python 3.11 + FastAPI (Poetry) / Vue 3 + Vuetify 3 (pnpm) / Docker Compose.

## Árbol de directorios real

```text
/dashboard
├── .ai/
│   ├── BEHAVIOR.md
│   └── TECHNICAL_CTX.md          # este archivo
├── docker-compose.yaml
├── mkdocs.yml
├── generate_secret.py            # genera ROOT_SECRET; lee de env, no hardcodea
│
├── backend/
│   ├── app/
│   │   ├── main.py                # entrypoint FastAPI, lifespan, CORS, routers
│   │   ├── core/
│   │   │   ├── config.py           # Settings (pydantic-settings), fail-fast en secretos
│   │   │   ├── database.py          # DatabaseSessionManager (singleton, wired al lifespan)
│   │   │   └── security.py           # Stateless Root: Argon2id + JWT clave derivada
│   │   ├── db/
│   │   │   └── base_class.py        # DeclarativeBase + TimestampMixin + UUIDMixin
│   │   ├── crud/
│   │   │   └── base.py               # CRUDBase genérico
│   │   └── api/routes/
│   │       ├── auth.py                # POST /login (con honeypot server-side)
│   │       ├── system.py               # GET /status (health check público)
│   │       └── node.py                  # /status, /logs, /metrics, /action (protegidos)
│   ├── alembic/                    # migraciones, env.py async
│   ├── generate_secret.py         # copia local del script (ver también el de la raíz)
│   ├── pyproject.toml              # Poetry, Ruff configurado en [tool.ruff]
│   └── smoke_test.py                # certificación manual rápida (no reemplaza pytest)
│
├── frontend/
│   └── app/
│       ├── src/
│       │   ├── components/          # NodeControlPanel.vue, SystemStatusDisplay.vue
│       │   ├── layouts/default.vue   # v-app-bar + navigation-drawer + snackbar global
│       │   ├── pages/                 # login.vue, index.vue (auto-routing)
│       │   ├── services/
│       │   │   └── httpClient.js       # instancia axios con interceptor de Authorization
│       │   └── stores/                 # authStore, nodeStore, systemStore, uiStore (Pinia)
│       └── package.json             # pnpm
│
└── docs/
    └── architecture/REQUIREMENTS.md  # requerimientos funcionales/no funcionales, fases
```

## Notas para el agente IA de este proyecto
- Backend real vive en `/backend/app`, no en `/backend/api` (corregido en `BEHAVIOR.md`).
- El patrón de auth es "Stateless Root": no hay tabla de usuarios, `ROOT_SECRET` se verifica
  recomputando el hash y comparando en tiempo constante. Ver `core/security.py`.
- Las rutas protegidas (`/api/node/*`) requieren `Authorization: Bearer <token>` — el cliente HTTP
  del frontend (`services/httpClient.js`) lo adjunta automáticamente vía interceptor.
- `check_db_health()` usa `sessionmanager.session()` (de `core/database.py`), nunca
  `request.app.state.engine` (nunca se asignaba ahí).
