# Auth Manifesto (Seguridad & Identidad)

> **Ámbito:** Backend Security
> **Ubicación:** backend/AUTH_MANIFESTO.md
> **Estrategia:** Deterministic Identity + Stateless Root + GitOps Ready
> **Algoritmo:** Argon2 (Infrastructure Compatible)

## 1. La Fórmula de Identidad (The Core)

El sistema NO almacena contraseñas de Root. La autenticación se basa en comparar el resultado de una operación criptográfica determinista.

* **Fórmula:** `Auth_Hash = Argon2(Email + Password + SYSTEM_SECRET)`
* **SYSTEM_SECRET:** Una "Pepper" (variable de entorno) interna del servidor, desconocida por la BD o el Frontend.

## 2. El SuperAdmin (Stateless Root)

El acceso "Dios" se valida matemáticamente contra el entorno (Infraestructura como Código).

* **Variable Objetivo:** `ROOT_AUTH_HASH` (Almacenada en `.env` o Secret Manager).
* **Mecanismo de Login:**
    1. Backend recibe `email` y `password` (Body).
    2. Calcula el hash con la fórmula.
    3. Compara con `ROOT_AUTH_HASH` inyectado en tiempo de ejecución.
    4. Si coincide -> Emite JWT (Access Token).

## 3. Compatibilidad de Infraestructura (CRÍTICO)

Debido a que Docker Compose interpreta los signos `$` como variables de entorno, el Hash almacenado en `.env` debe seguir una regla de escape estricta:

* **Regla:** Todo signo `$` en el hash debe duplicarse como `$$`.
* **Automatización:** No editar manualmente. Usar siempre el script `backend/generate_hash.py`, el cual aplica este formato automáticamente.
* **Ejemplo:**
  * *Raw Hash:* `$argon2id$v=19...`
  * *Docker Env:* `$$argon2id$$v=19...`

## 4. Política de Acceso

1. **Cerrado por Defecto:** Sin registro público.
2. **Zero Knowledge:** El servidor nunca persiste las credenciales, solo opera sobre ellas en memoria volátil.
3. **GitOps Governance:** La identidad del SuperAdmin es inmutable en tiempo de ejecución. Solo cambia mediante un redespliegue (cambio de variables de entorno).

## 5. Variables de Entorno Requeridas

* `AUTH_SECRET`: La "Pepper" para salar los hashes.
* `ROOT_AUTH_HASH`: El hash resultante (escapado para Docker) que autoriza al SuperAdmin.
