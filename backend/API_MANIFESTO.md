# API Manifesto (Reglas de Diseño REST)

> **Ámbito:** Backend Governance
> **Ubicación:** backend/API_MANIFESTO.md
> **Estándar:** RESTful Estricto + JSON API

## 1. Reglas Globales

1. **Prefijo:** `/api/v1` (Obligatorio para versionado).
2. **Formato:** `JSON` estricto en Request y Response.
3. **Trailing Slashes:** Prohibidos (ej: `/items/` -> `/items`).

## 2. Mapa de Verbos y Códigos (Tabla de Verdad)

| Acción | Verbo HTTP | Código de Éxito | Comportamiento Estricto |
| :--- | :--- | :--- | :--- |
| **Crear** | `POST` | **201 Created** | Retorna el recurso creado con ID. |
| **Leer (Lista)** | `GET` | **200 OK** | Retorna Array (vacío `[]` si no hay datos). |
| **Leer (Uno)** | `GET` | **200 OK** | Retorna Objeto. **404** si no existe. |
| **Actualizar** | `PUT` | **200 OK** | Reemplazo total o parcial. Retorna actualizado. |
| **Eliminar** | `DELETE` | **204 No Content** | Body vacío. **404** si el ID no existe. |

## 3. Estándar de Esquemas (DTOs)

Para garantizar la seguridad y limpieza de datos, cada Recurso (ej: `Item`) debe implementar el patrón de **Triple Esquema** en `api/models.py`:

1. **`Base`** (Mixins): Campos compartidos.
2. **`Create`** (Input): Hereda de Base. Lo que el usuario envía (Sin ID).
3. **`Read`** (Output): Hereda de Base. Lo que la API responde (Con ID).
    * *Regla:* Nunca devolver el modelo de DB directo (evitar leak de passwords/metadata).

## 4. Estructura de Rutas

* **Prohibido:** Definir rutas en `main.py`.
* **Obligatorio:** Usar `APIRouter` en archivos modulares dentro de `api/routers/{recurso}.py`.
