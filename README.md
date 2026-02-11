# DASHBOARD: STATELESS ROOT & HYBRID PERSISTENCE

> **Versión Arquitectura:** 1.3.0
> **Estado:** Estable (Core & Security Hardened)

Este proyecto es un Panel de Control autocontenido diseñado bajo la filosofía **Stateless Root**. Prioriza la seguridad criptográfica (Argon2id + Hex128) y la estabilidad visual mediante una arquitectura de componentes modulares y una política de consola limpia.

---

## 🧠 Protocolo de Desarrollo (Reglas Maestras)

Para garantizar la estabilidad del proyecto y evitar alucinaciones, todo colaborador debe seguir estas reglas estrictas:

1. **Anclaje de Estado (State Recovery):**
    * Ante cualquier vacío de contexto, declarar: *"Basado en el README v1.3.0, nos quedamos en la Fase X, paso Y"*.

2. **Quiet Console Policy (Consola Silenciosa):**
    * Está estrictamente prohibido dejar `console.log` o `console.error` en producción.
    * Los errores de red se gestionan mediante interceptores silenciosos que resuelven promesas para evitar rastro de "stack traces" en el navegador.

3. **Zero Layout Shift (Anti-Rebote):**
    * Todo componente que dependa de datos asíncronos debe tener un contenedor con `min-height` o altura fija.
    * La UI no debe desplazarse verticalmente durante las fases de carga o error.

---

## 🛡️ ESPECIFICACIONES TÉCNICAS (Blindaje v1.3.0)

### 1. Autenticación Stateless Root

* **Hashing**: Implementación de **Argon2id** con un Salt determinista derivado del `SYSTEM_PEPPER`.
* **Validación**: Comparación de tiempo constante (`secrets.compare_digest`) para mitigar ataques de canal lateral.
* **Sesión**: Emisión de **JWT** firmado con una clave dinámica (`ROOT_SECRET` + `SYSTEM_PEPPER`).

### 2. Sistema de Feedback & Heartbeat

* **Heartbeat**: Ciclo de sincronización automática cada 30 segundos gestionado en el Layout global.
* **Quiet Axios**: Interceptores configurados para capturar errores 401 y fallos de red, notificando vía UI (Snackbar/LED) sin ensuciar la consola de desarrollo.
* **Modular Display**: Componente `SystemStatusDisplay.vue` autónomo que consume su propio store y gestiona su estado visual.

---

## 📍 PLAN MAESTRO DE EJECUCIÓN

### FASE 6: INTERFAZ DE USUARIO (CORE) - COMPLETADA ✅

* [x] **6.1 Store Auth**: Pinia + JWT Persistence (ESLint Clean). ✅
* [x] **6.2 Login View**: Anti-Rebote + Honeypot + Feedback tonal. ✅
* [x] **6.3 Security Guards**: Axios Interceptors (Silent Mode) + Router Guards. ✅
* [x] **6.4 Layout Premium**: App Bar con progreso absoluto, LED status y Heartbeat. ✅
* [x] **6.5 Feedback System**: Global Snackbar & UI Loading Store. ✅
* [x] **6.6 Dashboard Home**: Integración de `SystemStatusDisplay` modular. ✅

### FASE 7: MOTOR DE WIDGETS "DATA-DRIVEN" 🚧

*Objetivo: Implementar una arquitectura de Dashboard guiada por metadatos JSON.*

* [x] **7.1 Backend Telemetry**: Endpoint `/api/system/status` verificado. ✅
* [x] **7.2 Dashboard Store**: Implementar `systemStore` con reactividad completa. ✅
* [x] **7.3 Moldes Maestros**: Crear `SystemStatusDisplay.vue` como componente autónomo. ✅
* [ ] **7.4 Widgets Avanzados**: Implementar `WidgetStat.vue` para métricas CPU/RAM.
* [ ] **7.5 Orquestador de Grid**: Crear `DashboardGrid.vue` basado en configuración JSON.

---

## 🛠 Comandos Rápidos

**Limpieza de archivos huérfanos:**

```bash
rm frontend/app/src/components/HelloWorld.vue
rm frontend/app/src/stores/app.js
rm -rf frontend/app/src/components/widgets
```

**Levantar entorno:**

```bash
docker compose up
```
