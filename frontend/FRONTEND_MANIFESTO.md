# FRONTEND MANIFESTO
>
> **Ámbito:** UI/UX & Cliente Web
> **Versión:** 1.0.0
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

### 3.2. Regla de TypeScript/ESLint

Aunque la lógica se escriba en Javascript estándar, la etiqueta de script **siempre** debe incluir el atributo `lang="ts"`.

* **Correcto:** `<script setup lang="ts">`
* **Incorrecto:** `<script setup>`
* *Razón:* Garantizar que ESLint valide el código correctamente bajo las reglas del proyecto.

### 3.3. Uso de Vuetify

1. **Prioridad de Props:** Antes de escribir una sola línea de CSS o clases utilitarias, se debe verificar si el componente de Vuetify ofrece una propiedad nativa para el efecto deseado (ej: usar `density="compact"` en lugar de reducir padding manualmente).
2. **Iconografía:** Se utilizarán estrictamente los iconos provistos por defecto en la instalación de Vuetify (Material Design Icons). No se permite la importación de librerías de iconos externas sin una justificación de arquitectura aprobada.

## 4. Estándares de Integración

1. **Consumo de API:** Prohibido "hardcodear" URLs. Uso estricto de variables de entorno (ej: `import.meta.env.VITE_API_URL`).
2. **Limpieza:** El código no debe contener `console.log` ni código comentado en los commits finales.
