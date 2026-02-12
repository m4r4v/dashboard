# DASHBOARD: STATELESS ROOT & HYBRID PERSISTENCE

> **Versión Arquitectura:** 1.4.0
> **Estado:** Certificado (Security, Metrics & DevOps Ready)

Este sistema es una infraestructura de control diseñada bajo la filosofía **Stateless Root**. Prioriza la soberanía del administrador permitiendo el control total del nodo incluso en escenarios de degradación crítica de la persistencia, utilizando criptografía determinista y telemetría industrial compatible con Prometheus.

---

## 🧠 Protocolo de Desarrollo (Reglas Maestras)

1. **Anclaje de Estado (State Recovery):**
    * Ante cualquier reinicio de contexto, declarar: *"Basado en el README v1.4.0, el sistema está certificado hasta la Fase 8 y listo para iniciar la Fase 9"*.

2. **Quiet Console Policy (Consola Silenciosa):**
    * Prohibido el uso de `print()` o `console.log()` en producción. La visibilidad se gestiona mediante el `InMemoryLogHandler` para mantener la salida estándar limpia y reservada para auditorías de sistema.

3. **Zero Layout Shift (Anti-Rebote):**
    * La interfaz utiliza contenedores de tamaño fijo y guardias reactivas. Si la sesión expira o se cierra, el DOM se destruye instantáneamente mediante `v-if` para evitar fugas visuales de datos sensibles.

---

## 🛡️ ESPECIFICACIONES TÉCNICAS (Blindaje v1.4.0)

### 1. Seguridad Criptográfica (Stateless Root)

* **Auth**: Implementación de **Argon2id** con Salt determinista derivado del `SYSTEM_PEPPER`.
* **JWT**: Firmado asimétrico con secretos de 128-hex. Acceso Root garantizado sin consultas a base de datos.

### 2. Observabilidad de Nodo (Telemetría)

* **Metrics Endpoint**: `/api/node/metrics` expone contadores HTTP (4xx/5xx) y salud de DB en formato **Prometheus**.
* **Live Logs**: Búfer circular en RAM (`deque`) que captura la auditoría de peticiones sin persistencia física, garantizando privacidad y velocidad de acceso.

---

## 📍 PLAN MAESTRO DE EJECUCIÓN DETALLADO

### FASE 1: Cimentación & Core Asíncrono ✅

* [x] **1.1 FastAPI Backend**: Implementación de arquitectura asíncrona (`async/await`). **¿Por qué?** Para manejar múltiples peticiones concurrentes sin bloqueo de E/S. **¿Para qué?** Para garantizar una respuesta fluida del Dashboard bajo carga.
* [x] **1.2 Docker Orchestration**: Entorno multi-contenedor aislado. **¿Por qué?** Para eliminar el problema de "en mi máquina funciona". **¿Para qué?** Para asegurar que el despliegue sea idéntico en cualquier servidor.
* [x] **1.3 Environment Setup**: Gestión de secretos mediante `.env`. **¿Para qué?** Para separar las claves maestras del código fuente, siguiendo estándares de seguridad.

### FASE 2: Seguridad Stateless (Argon2id) ✅

* [x] **2.1 Hashing Determinista**: Uso de Argon2id para validar credenciales sin almacenarlas. **¿Por qué?** Es resistente a ataques de fuerza bruta por GPU. **¿Para qué?** Para proteger la identidad administrativa contra ataques de diccionario modernos.
* [x] **2.2 System Pepper**: Capa extra de entropía aplicada antes del hashing. **¿Para qué?** Para que un atacante no pueda predecir el hash ni siquiera con acceso parcial al código.

### FASE 3: Identidad de Nodo & JWT ✅

* [x] **3.1 Node ID Service**: Extracción dinámica del hostname del contenedor. **¿Para qué?** Para identificar unívocamente cada réplica en despliegues horizontales (Clustering).
* [x] **3.2 JWT Factory**: Emisión de tokens firmados. **¿Por qué?** Para que el cliente sea quien porte su propia identidad (Stateless), liberando memoria en el servidor.

### FASE 4: API de Autenticación & Control ✅

* [x] **4.1 Root Verification**: Lógica de "Entrada de Emergencia". **¿Para qué?** Para permitir reparaciones del sistema incluso si la base de datos principal está desconectada.
* [x] **4.2 Auth Endpoints**: Rutas de login protegidas contra ataques de temporización (Timing attacks).

### FASE 5: Frontend Baseline (Vue 3 + Pinia) ✅

* [x] **5.1 Reactivity System**: Setup de Vue 3 con Composition API. **¿Por qué?** Para una gestión de componentes modular y escalable.
* [x] **5.2 Pinia Stores**: Centralización del estado de autenticación (`isLoading`, `token`, `user`). **¿Para qué?** Para que toda la UI reaccione instantáneamente a cambios en la sesión.

### FASE 6: Resiliencia Visual & Seguridad UI ✅

* [x] **6.1 Reactive Guards**: Protección de rutas mediante navegación programática. **¿Para qué?** Para expulsar al usuario al Login inmediatamente si el token es invalidado o expira.
* [x] **6.2 Anti-Shift Layout**: Uso de `min-height` y esqueletos de carga. **¿Por qué?** Para evitar movimientos bruscos de la UI (CLS) mientras se obtienen datos del servidor.

### FASE 7: Ingeniería de Componentes Modulares ✅

* [x] **7.1 SystemStatusDisplay**: Widget autónomo de salud. **¿Para qué?** Para monitorear Uptime y RAM de un vistazo rápido sin navegar por menús complejos.
* [x] **7.2 NodeControlPanel**: Consola de eventos integrada. **¿Por qué?** Para dar visibilidad al administrador sobre acciones internas del nodo en tiempo real.

### FASE 8: Observabilidad & Certificación (Quality Gate) ✅

* [x] **8.1 Telemetry Metrics**: Endpoint estilo Prometheus. **¿Por qué?** Para permitir que herramientas externas (Grafana) monitoreen la tasa de errores del sistema.
* [x] **8.2 Audit Middleware**: Interceptor de tráfico HTTP. **¿Para qué?** Para registrar automáticamente cada acceso, detectando escaneos o errores de integración.
* [x] **8.3 Atomic Auditing**: Implementación de `InMemoryLogHandler`. **¿Por qué?** Para capturar logs `INFO` en un búfer de RAM, garantizando un panel de eventos siempre actualizado.
* [x] **8.4 Smoke Test Suite**: Script de validación automatizada (`smoke_test.py`). **¿Para qué?** Para certificar que la seguridad y la telemetría son funcionales tras cada cambio de código.

### FASE 9: INFRASTRUCTURE ENABLERS (Data Hub) 🚧

*Objetivo: Construir el Framework de Datos Blindado y el Hub de Conexiones Dinámicas. Sin lógica de negocio.*

* [ ] **9.1 BaseModel (Data Contract)**: Definición de la clase maestra con UUIDv4 y Timestamps. **¿Por qué?** Para garantizar unicidad global y auditoría en todas las tablas futuras. **¿Para qué?** Para que el Root pueda gestionar datos de cualquier módulo mediante una interfaz universal.
* [ ] **9.2 SessionManager (Connection Hub)**: Motor de mapeo `.env` -> Conexiones. **¿Por qué?** Para permitir que el sistema se conecte a múltiples bases de datos (plugins) sin tocar el código fuente. **¿Para qué?** Para que el Root pueda "instalar" nuevos módulos (Ticketera, Inventario) simplemente configurando variables de entorno.
* [ ] **9.3 Alembic (Version Control)**: Configuración asíncrona del gestor de esquemas. **¿Por qué?** Para evolucionar la estructura de la base de datos sin pérdida de datos. **¿Para qué?** Para permitir actualizaciones seguras de los módulos en producción.
* [ ] **9.4 CRUDBase (Atomic Transactions)**: Implementación de operaciones genéricas con integridad transaccional. **¿Por qué?** Para evitar condiciones de carrera modificando objetos en memoria (`db_obj`). **¿Para qué?** Para proveer al Root de una "Mano Universal" capaz de administrar cualquier tabla del ecosistema.

---

## 🛠 Comandos de Operación

**Certificar Integridad (Smoke Test):**

````bash
python3 backend/smoke_test.py
```

**Despliegue de Infraestructura:**

```bash
docker compose up --build
```

**Consulta de Telemetría (Requiere Token Root):**

```bash
curl -X GET "http://localhost:8000/api/node/metrics" -H "Authorization: Bearer <TOKEN>"
```
