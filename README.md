# DASHBOARD: STATELESS ROOT & HYBRID PERSISTENCE

> **Versión Arquitectura:** 1.3.0
> **Estado:** Estable (UI Core Completo)

Este proyecto es un Panel de Control autocontenido diseñado bajo la filosofía **Stateless Root**. Prioriza la seguridad criptográfica (Argon2id + Hex128) y utiliza un modelo de persistencia híbrida (SQLite Local / Postgres Cloud) para adaptarse a cualquier entorno sin cambios de código.

---

## 🧠 Protocolo de Desarrollo (Reglas Maestras)

Para garantizar la estabilidad del proyecto y evitar alucinaciones, todo colaborador (incluida la IA) debe seguir estas reglas estrictas:

1. **Anclaje de Estado (State Recovery):**
    * Ante cualquier vacío de contexto o reinicio de sesión, se debe declarar explícitamente: *"Basado en el README v1.3.0, nos quedamos en la Fase X, paso Y"*. Nunca asumir o improvisar el estado actual.

2. **Aprobación Previa (Pre-Flight Check):**
    * Antes de escribir una sola línea de código para una nueva Fase, se deben **discutir y aprobar** los objetivos, la lógica y el alcance de dicha fase.
    * *No se implementa nada que no haya sido analizado primero.*

---

## 📍 PLAN MAESTRO DE EJECUCIÓN (Estado Actual)

### FASE 1: ROOT & CONFIGURACIÓN (La Base)

- [x] **1.1 `.gitignore`**: Definir exclusiones de seguridad y entorno. ✅
* [x] **1.2 `README.md`**: Tablero de control y documentación viva. ✅
* [x] **1.3 `mkdocs.yml`**: Sistema de documentación. ✅
* [x] **1.4 `docker-compose.yaml`**: Orquestador v1.1.0. ✅
* [x] **1.5 `.env`**: Secretos v1.2 (Hash + Pepper). ✅

### FASE 2: DOCUMENTACIÓN

- [x] **2.1 Estructura `/docs`**: Arquitectura y Guías. ✅
* [x] **2.2 `REQUIREMENTS.md`**: Especificación oficial. ✅

### FASE 3: BACKEND (El Cerebro)

- [x] **3.1 Dependencias**: Poetry (FastAPI, Argon2, AsyncPG). ✅
* [x] **3.2 Dockerfile**: Multi-Stage optimizado. ✅
* [x] **3.3 Persistencia**: Lógica Híbrida (SQLite/Postgres). ✅
* [x] **3.4 Entrypoint**: Main, CORS y Health Check. ✅
* [x] **3.5 Auth Core**: Argon2id (Hex 128) + JWT. ✅

### FASE 4: FRONTEND (La Cara)

- [x] **4.1 Estructura**: Vite + Vuetify + TypeScript. ✅
* [x] **4.2 Build**: Verificación de compilación. ✅

### FASE 5: INTEGRACIÓN & DESPLIEGUE

- [x] **5.1 Docker Build**: Levantamiento conjunto. ✅
* [x] **5.2 Test DB**: Verificación de persistencia. ✅
* [x] **5.3 Test Auth**: Login Root verificado. ✅

### FASE 6: INTERFAZ DE USUARIO (CORE)

- [x] **6.1 Store Auth**: Pinia + JWT Persistence. ✅
* [x] **6.2 Login View**: Honeypot + Feedback visual. ✅
* [x] **6.3 Security Guards**: Axios Interceptors + Router Guards. ✅
* [x] **6.4 Layout Premium**: App Bar, Drawer, Theme Switcher. ✅
* [x] **6.5 Feedback System**: Global Snackbar & Loading Store. ✅
* [x] **6.6 Dashboard Home**: Widgets de resumen y estructura EN. ✅

### FASE 7: GESTIÓN DE USUARIOS (Fase Activa) 🚧

*Objetivo: Transformar el sistema en una plataforma multi-usuario real.*

* [ ] **7.1 Análisis**: Discusión de modelo de datos y endpoints.
* [ ] **7.2 Backend DB**: Modelo SQLAlchemy `User` y Migración.
* [ ] **7.3 API CRUD**: Endpoints (Create, Read, Update, Delete).
* [ ] **7.4 Frontend Store**: Lógica Pinia para usuarios.
* [ ] **7.5 UI Gestión**: Tabla de datos y formularios.

---

## 🔮 Roadmap Futuro (2026+)

### FASE 8: AUDITORÍA Y TRAZABILIDAD

* **Objetivo:** Registro inmutable de acciones ("Quién hizo qué").
* **Alcance:** Middleware de intercepción, Logs de seguridad, Vista de Auditoría.

### FASE 9: TELEMETRÍA Y VISUALIZACIÓN

* **Objetivo:** Datos reales en tiempo real.
* **Alcance:** Librería de gráficas (ApexCharts/Chart.js), Endpoints de agregación (KPIs).

### FASE 10: CONFIGURACIÓN DINÁMICA

* **Objetivo:** Controlar el negocio sin reiniciar Docker.
* **Alcance:** Tabla `settings`, UI de configuración de variables del sistema.

### FASE 11: HARDENING & PRODUCCIÓN

* **Objetivo:** Salida al mundo real.
* **Alcance:** Nginx Reverse Proxy (SSL), CI/CD Pipelines, Optimización Gzip/Cache.

---

## 🛠 Comandos Rápidos

**Levantar entorno:**

```bash
docker compose up
```

**Generar credenciales Root:**

```bash
cat generate_secret.py | docker compose exec -T backend python3
```
