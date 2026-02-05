# Dashboard Frontend Service

Cliente Web construido con **Vue 3** y **Vuetify 3**, servido mediante **Vite**.

## 🔧 Stack Tecnológico

* **Framework:** Vue 3 (Composition API)
* **UI Library:** Vuetify 3 (Material Design)
* **Build Tool:** Vite
* **Package Manager:** PNPM (Estricto)
* **Runtime:** Node.js 20 (Alpine)

## 🚀 Comandos de Desarrollo

La ejecución principal se realiza vía Docker, pero para referencia de scripts internos:

```bash
# Iniciar servidor de desarrollo (Mapeado al puerto 3000)
pnpm dev

# Construir para producción
pnpm build

# Linting y Formateo
pnpm lint
```

## 🏗️ Estructura del Proyecto
>
> Fuente de Verdad: `FRONTEND_MANIFESTO.md`

```text
frontend/
├── app/                 # Código Fuente (Montado en Docker)
│   ├── src/
│   │   ├── components/  # Componentes reutilizables (PascalCase)
│   │   ├── pages/       # Vistas y Rutas (Auto-routing)
│   │   └── plugins/     # Configuración de Vuetify/Router
│   └── package.json     # Definición de dependencias
├── FRONTEND_MANIFESTO.md # Gobernanza específica
└── Dockerfile           # Definición de imagen (Multistage)
```

## 🔌 Integración

Este servicio consume la API definida en `VITE_API_URL`.
Para validar la conexión, visitar `/sys-check`.
