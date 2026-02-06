# Seguridad y Autenticación

El backend implementa un modelo de seguridad **Stateless Root** (Raíz sin estado). No utilizamos una tabla de usuarios en la base de datos; en su lugar, la identidad del Administrador se valida criptográficamente contra variables de infraestructura.

## 🔐 Mecanismo de Acceso

Las rutas de lectura (`GET`) son públicas. Las rutas de escritura (`POST`, `PUT`, `DELETE`) están protegidas y requieren un **Token JWT**.

### Flujo de Autenticación

1. **Obtener Token:**
    * **Endpoint:** `POST /api/v1/auth/login`
    * **Body:**

      ```json
      {
        "email": "tu-email@admin.com",
        "password": "tu-password-secreta"
      }
      ```

    * **Respuesta:** Recibirás un `access_token` válido por 30 minutos.

2. **Usar Token:**
    * Incluye el token en el Header HTTP de tus peticiones:
    * `Authorization: Bearer <TU_TOKEN>`

## 🛠 Gestión de Identidad (Infrastructure as Code)

La contraseña del SuperAdmin no se guarda en texto plano. Se almacena como un hash Argon2 en el archivo `.env`.

### Generador Automático

Para configurar o rotar las credenciales, utiliza el script de utilidad incluido en el contenedor. Este script se encarga de calcular el hash y **formatearlo correctamente para Docker** (escapando los caracteres especiales).

**Comando:**

```bash
docker compose run --rm backend python generate_hash.py
```

El asistente interactivo realizará lo siguiente:

1. Solicitará Email y Password.
2. Generará un `AUTH_SECRET` (Pepper) si no existe.
3. Calculará el hash Argon2.
4. **Escribirá automáticamente** las variables `ROOT_AUTH_HASH` y `AUTH_SECRET` en tu archivo `.env`.

> **Nota:** Después de generar nuevas credenciales, debes reiniciar el backend (`docker compose restart backend`) para que surtan efecto.

## ⚠️ Políticas de Seguridad

* **Zero Knowledge:** El servidor nunca conoce tu contraseña real, solo valida su huella criptográfica.
* **Docker Compatibility:** Los hashes Argon2 contienen signos `$` que Docker interpreta como variables. Nuestro generador los convierte automáticamente a `$$` para evitar corrupción de datos.
