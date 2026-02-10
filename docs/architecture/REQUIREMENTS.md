# PROYECTO DASHBOARD: ESPECIFICACIÓN DE REQUERIMIENTOS

> **VERSIÓN:** 1.2.0 (ACTUALIZADA - LÓGICA PEPPER)
> **ESTADO:** LISTO PARA IMPLEMENTACIÓN
> **ARQUITECTURA:** STATELESS ROOT + HYBRID PERSISTENCE + ASYNC IO

---

## 1. DEFINICIÓN DEL SISTEMA
El sistema es un **Panel de Control (Dashboard)** autocontenido. Su arquitectura "Stateless Root" desacopla la autenticación administrativa de la base de datos, basándose puramente en criptografía inyectada. Su modelo de persistencia es híbrido, permitiendo transiciones transparentes entre desarrollo local (SQLite) y producción (PostgreSQL) gestionadas por configuración.

---

## 2. REQUERIMIENTOS FUNCIONALES (RF)

### Módulo de Seguridad (Stateless Core)
* **RF-01 Inyección de Identidad:** La identidad del "Root" se define exclusivamente mediante la variable de entorno `ROOT_SECRET` inyectada al iniciar el contenedor.
* **RF-02 Verificación Criptográfica (Protocolo Hex-128):**
    * **Entrada:** Concatenación estricta de `Email + Password` (ej: `admin@dashboard.comadmin`).
    * **Algoritmo:** **Argon2id**.
    * **Formato:** Salida codificada estrictamente en **Hexadecimal** de **128 caracteres** (512 bits).
    * **Validación:** Comparación de tiempo constante contra `ROOT_SECRET`.
* **RF-03 Emisión de Sesión (JWT con Pepper):**
    * **Firma:** El token JWT debe ser firmado usando **HS256**.
    * **Llave de Firma:** La llave se deriva dinámicamente combinando `ROOT_SECRET` + `SYSTEM_PEPPER` (Variable de entorno).
* **RF-04 Fail-Safe:** El sistema aborta el inicio si `ROOT_SECRET` o `SYSTEM_PEPPER` no están presentes o no cumplen los requisitos de longitud.

### Módulo de Persistencia (Hybrid & Async)
* **RF-05 Configuración Adaptativa:** Evaluación de `DATABASE_URL` al arranque.
* **RF-06 Estrategia Local (SQLite Asíncrono):** Sin `DATABASE_URL` -> usa **`aiosqlite`** sobre el archivo `./backend/dashboard.db`.
* **RF-07 Estrategia Cloud (PostgreSQL Asíncrono):** Con `DATABASE_URL` -> usa **`asyncpg`** para conexión remota.

### Módulo de Interfaz & API
* **RF-08 SPA Frontend (Material Design):** Interfaz construida sobre **Vuetify 3** (Componentes Material Design) y **Vue 3 Composition API**.
* **RF-09 Documentación Viva:** Servicio MkDocs accesible en `/docs`.
* **RF-10 CORS:** Backend configurado para permitir orígenes cruzados explícitos (puerto 3000 <-> puerto 8000).

---

## 3. REQUERIMIENTOS NO FUNCIONALES (RNF)

### Seguridad & Compliance
* **RNF-01 Cero Secretos en Código:** Prohibición total de credenciales en el repositorio. Inyección estricta vía `.env`.
* **RNF-02 Ejecución Non-Root:** Contenedores de producción corriendo bajo UID 1000.

### Portabilidad & DevOps
* **RNF-03 Docker-First:** Despliegue único con `docker compose up`.
* **RNF-04 Gestión de Paquetes Determinista:**
    * **Backend:** Uso exclusivo de **Poetry** (con `poetry.lock`). Prohibido `pip` directo.
    * **Frontend:** Uso exclusivo de **pnpm** (con `pnpm-lock.yaml`). Prohibido `npm` o `yarn`.

### Desarrollo & DX
* **RNF-05 Hot-Reload:** Reinicio automático de Uvicorn y HMR de Vite ante cambios en código.
* **RNF-06 Estructura Espejo:** Los volúmenes de Docker deben mapear exactamente la estructura de carpetas del host.

---

## 4. STACK TECNOLÓGICO CONGELADO

| Capa | Tecnología | Detalle Crítico |
| :--- | :--- | :--- |
| **Backend** | Python 3.11 + FastAPI | Async Nativo |
| **Gestor Back** | **Poetry** | Versión 1.7+ |
| **Frontend** | Vue 3 + **Vuetify 3** | Composition API |
| **Gestor Front** | **pnpm** | Performance & Disk Space |
| **Auth** | Argon2id + JWT | **Hex 128 Output + Pepper** |
| **DB Drivers** | SQLAlchemy (Async) | `aiosqlite` / `asyncpg` |
| **Infra** | Docker Compose | V2 |

---

## 5. ESTRUCTURA DE ARCHIVOS OFICIAL (TREE)
Cualquier desviación de esta estructura se considera una violación de la arquitectura.

```text
/dashboard
├── .ai/                        # Contexto de IA
│   ├── BEHAVIOR.md
│   └── TECHNICAL_CTX.md
├── .env                        # [NO GIT] Secretos (ROOT_SECRET, SYSTEM_PEPPER)
├── .gitignore                  # Ignora .env, __pycache__, .venv
├── docker-compose.yaml         # Orquestador
├── mkdocs.yml                  # Configuración Documentación
├── README.md
│
├── backend/
│   ├── app/                    # Código Fuente Python
│   │   ├── __init__.py
│   │   ├── config.py           # Lógica Híbrida (SQLite/Postgres)
│   │   └── main.py             # Entrypoint FastAPI
│   ├── .dockerignore           # Exclusiones de contexto Docker
│   ├── Dockerfile              # Multi-Stage (Poetry)
│   └── pyproject.toml          # Definición de Dependencias
│
├── frontend/
│   ├── app/                    # Código Fuente Vue/Vuetify
│   │   ├── package.json        # Dependencias (pnpm)
│   │   ├── pnpm-lock.yaml      # Lockfile
│   │   ├── vite.config.mjs     # Configuración Build
│   │   └── src/                # Componentes
│   └── (Sin Dockerfile)        # Usa imagen base 'm4r4v/frontend'
│
└── docs/
    ├── architecture/           # REQUIREMENTS.md, Diagramas
    └── guides/                 # Manuales
```