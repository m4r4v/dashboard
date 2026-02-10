# DASHBOARD: STATELESS ROOT & HYBRID PERSISTENCE

> **Versión Arquitectura:** 1.2.0
> **Estado:** Estable (Backend + Auth Integrados)

Este proyecto es un Panel de Control autocontenido diseñado bajo la filosofía **Stateless Root**. Prioriza la seguridad criptográfica (Argon2id + Hex128) y utiliza un modelo de persistencia híbrida (SQLite Local / Postgres Cloud) para adaptarse a cualquier entorno sin cambios de código.

---

## 📍 PLAN MAESTRO DE EJECUCIÓN (Macro a Micro)

Este tablero rastrea el progreso del reinicio del sistema, yendo desde la configuración raíz hacia los componentes internos.

### FASE 1: ROOT & CONFIGURACIÓN (La Base)

*Objetivo: Establecer los archivos de configuración global y orquestación.*

- [x] **1.1 `.gitignore`**: Definir exclusiones de seguridad y entorno (RNF-01). ✅
- [x] **1.2 `README.md`**: Establecer el tablero de control y documentación inicial. ✅
- [x] **1.3 `mkdocs.yml`**: Configuración del sistema de documentación viva. ✅
- [x] **1.4 `docker-compose.yaml`**: Orquestador definitivo (v1.1.0) con servicios Backend, Frontend y Docs. ✅
- [x] **1.5 `.env`**: Plantilla de secretos con lógica v1.2 (Hash + Pepper). ✅

### FASE 2: DOCUMENTACIÓN (La Verdad)

*Objetivo: Formalizar la arquitectura antes de tocar código.*

- [x] **2.1 Estructura `/docs`**: Crear carpetas `architecture` y `guides` y el `index.md`. ✅
- [x] **2.2 `REQUIREMENTS.md`**: Congelar la especificación v1.1.0 oficial. ✅

### FASE 3: BACKEND (El Cerebro)

*Objetivo: Implementar la lógica híbrida y seguridad stateless.*

- [x] **3.1 `pyproject.toml`**: Definir dependencias con Poetry (FastAPI, Argon2, AsyncPG/AioSQLite). ✅
- [x] **3.2 `Dockerfile`**: Construcción Multi-Stage optimizada. ✅
- [x] **3.3 `backend/app/config.py`**: Implementar lógica "Hybrid Persistence" (Selector DB). ✅
- [x] **3.4 `backend/app/main.py`**: Entrypoint, CORS y Endpoint `/health`. ✅
- [x] **3.5 Auth Core**: Implementar hashing Argon2id (Hex 128) y JWT (Firma con Pepper). ✅

### FASE 4: FRONTEND (La Cara)

*Objetivo: Preparar la interfaz gráfica.*

- [x] **4.1 Limpieza**: Eliminar deuda técnica anterior. ✅
- [x] **4.2 Estructura**: Validar `package.json` (pnpm) y configuración de Vite. ✅
- [x] **4.3 Build & Smoke Test**: Verificar instalación de dependencias y arranque. ✅

### FASE 5: INTEGRACIÓN & DESPLIEGUE

*Objetivo: Verificar que todo funcione junto.*

- [x] **5.1 Build Inicial**: `docker compose up --build`. ✅
- [x] **5.2 Test de Persistencia**: Verificar creación de `dashboard.db`. ✅
- [x] **5.3 Test de Seguridad**: Verificar login con `ROOT_SECRET` + `SYSTEM_PEPPER`. ✅

### FASE 6: INTERFAZ DE USUARIO (CORE)

*Objetivo: Implementar gestión de sesión y vistas protegidas.*

- [X] **6.1 Store Auth**: Implementación de Pinia para gestión de JWT.
- [X] **6.2 Vista Login**: Formulario reactivo con componentes Vuetify.
- [ ] **6.3 Interceptor Axios**: Inyección automática de tokens en peticiones.

---

## 🛠 Comandos Rápidos

**Levantar entorno de desarrollo:**

```bash
docker compose up
```

**Generar credenciales Root (Docker-First):**
*Requiere el contenedor backend corriendo.*

```bash
cat generate_secret.py | docker compose exec -T backend python3
```

**Ver documentación:**
Acceder a `http://localhost:8080` una vez levantado el servicio.
