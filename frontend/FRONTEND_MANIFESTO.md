# FRONTEND MANIFESTO
>
> **Ámbito:** UI/UX & Cliente Web
> **Versión:** 1.3.0 (Store Nomenclature Standard)
> **Dependencias:** ROOT MANIFESTO

## 1. Definición del Stack Tecnológico

1. **Imagen Oficial:** `m4r4v/frontend:latest` (Docker Hub).
2. **Motor:** Node.js 20 (Alpine) + PNPM Global.
3. **Framework:** Vue 3 + Vuetify 3 (Stable).

## 2. Infraestructura y Entorno

El código fuente reside en el Host, pero su ejecución es exclusiva del Contenedor.

1. **Modelo de Persistencia:**
    * **Host:** `./frontend/app` (Fuente de Verdad).
    * **Contenedor:** `/workspace/app` (Entorno de Ejecución).
2. **Gestión de Dependencias:**
    * Prohibido instalar paquetes manualmente en el `Dockerfile`.
    * Toda dependencia debe agregarse vía `pnpm install <paquete>` dentro del contenedor corriendo o mediante la sincronización del volumen.

## 3. Estándares de Desarrollo (Code Style)

### 3.1. Estructura de Componentes (.vue)

El orden de los bloques es estricto e innegociable para mantener la consistencia visual y de lectura:

1. `<template>`
2. `<script setup lang="ts">`
3. `<style>`
4. `<route lang="yaml">` (Opcional, siempre al final)

### 3.2. Regla de TypeScript/ESLint

Aunque la lógica se escriba en Javascript estándar, la etiqueta de script **siempre** debe incluir el atributo `lang="ts"`.

* **Correcto:** `<script setup lang="ts">`
* **Incorrecto:** `<script setup>`
* *Razón:* Garantizar que ESLint valide el código correctamente bajo las reglas del proyecto.

### 3.3. Uso de Vuetify

1. **Prioridad de Props:** Antes de escribir una sola línea de CSS o clases utilitarias, se debe verificar si el componente de Vuetify ofrece una propiedad nativa para el efecto deseado (ej: usar `density="compact"` en lugar de reducir padding manualmente).
2. **Iconografía:** Se utilizarán estrictamente los iconos provistos por defecto en la instalación de Vuetify (Material Design Icons). No se permite la importación de librerías de iconos externas sin una justificación de arquitectura aprobada.

### 3.4. Nomenclatura y Enrutamiento (Vistas)

1. **Archivos PascalCase:** Se utilizará estrictamente **PascalCase** para todos los archivos `.vue` en `src/pages/` y `src/components/`.
    * *Correcto:* `SysCheck.vue`, `UserProfile.vue`
2. **URLs Personalizadas (Override):** Si se requiere una URL en `kebab-case` distinta al nombre del archivo, **está prohibido renombrar el archivo**. Se debe utilizar el bloque de configuración explícita al final del componente:

    ```yaml
    <route lang="yaml">
    path: /mi-ruta-personalizada
    </route>
    ```

### 3.5. Nomenclatura de Stores (Pinia)

1. **Archivos:** `camelCase.js` (ej: `auth.js`, `shoppingCart.js`). Se usa camelCase para diferenciarlos visualmente de los componentes.
2. **Composable:** Prefijo `use` + Nombre PascalCase + Sufijo `Store`.
    * *Correcto:* `export const useAuthStore = ...`
    * *Incorrecto:* `export const auth = ...` o `export const useAuth = ...`
3. **ID del Store:** El primer argumento de `defineStore` debe coincidir con el nombre del archivo.
    * *Archivo:* `cart.js` -> `defineStore('cart', ...)`

## 4. Estándares de Integración

1. **Consumo de API:** Prohibido "hardcodear" URLs. Uso estricto de variables de entorno (ej: `import.meta.env.VITE_API_URL`).
2. **Limpieza:** El código no debe contener `console.log` ni código comentado en los commits finales.
