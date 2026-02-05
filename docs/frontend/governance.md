# Gobernanza Frontend

> **Estado:** Activo
> **Fuente Legal:** `frontend/FRONTEND_MANIFESTO.md`

## 1. Stack Tecnológico

* **Imagen:** `m4r4v/frontend:latest`
* **Framework:** Vue 3 + Vuetify 3
* **Motor:** Node 20 (Alpine)

## 2. Reglas de Desarrollo

### Estructura de Componentes

El orden obligatorio es:

1. `<template>`
2. `<script setup lang="ts">`
3. `<style>`

### TypeScript

* **Etiqueta Obligatoria:** `<script setup lang="ts">`
* El uso de `lang="ts"` es mandatorio para validación ESLint, incluso si se escribe JS plano.

### Vuetify

* **Props > CSS:** Priorizar props nativas (ej: `density`) sobre clases CSS.
* **Iconos:** Solo Material Design Icons (default).

## 3. Integración

* **API:** Uso estricto de variables de entorno (`import.meta.env`).
* **Clean Code:** 0% `console.log` en commits.
