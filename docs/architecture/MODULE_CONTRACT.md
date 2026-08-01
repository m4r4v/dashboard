# CONTRATO DE PROPIEDADES DE MÓDULO

> **ESTADO:** DISEÑO — no implementado en código todavía.
> **ALCANCE:** Plantilla de frontend (rama `feature/frontend-template`), no el dashboard de monitoreo específico.

---

## 1. Qué problema resuelve

Hoy el dashboard muestra paneles fijos, escritos a mano (`SystemStatusDisplay.vue`, etc.). Para que la
plantilla sirva para cualquier tipo de app (CRM, monitoreo de infra, analítica, e-commerce), un
"módulo" no puede ser un componente Vue arbitrario sin reglas — necesita declarar un **contrato de
propiedades** común, para que el sistema que arma el dashboard (grid, modos de vista, refresco,
permisos) pueda tratar todos los módulos igual sin conocer su lógica interna.

La regla central: **el contrato es el mismo sin importar si el módulo es código interno (una store de
Pinia, una función) o una integración externa conectada por API.** Un módulo que consulta Stripe y uno
que consulta el store de autenticación se describen con las mismas propiedades.

## 2. Precedentes que validan el patrón

No es una idea inventada desde cero — es la misma forma en que resuelven esto sistemas ya probados en
producción: paneles de Grafana (cada panel declara tipo de visualización + datasource, desacoplados),
tarjetas de Home Assistant, widgets de Retool/Appsmith, plugins de Backstage, dashboards de
Metabase/Superset.

## 3. El contrato (propiedades declaradas por cada módulo)

```ts
interface ModuleDefinition {
  id: string
  label: string

  /** Cómo se renderiza en el grid del dashboard. */
  preview: PreviewType

  /** De dónde saca sus datos — mismo shape para código interno o integración externa. */
  dataSource: InternalDataSource | IntegrationDataSource

  /** Cuánta prominencia visual reclama. El sistema decide *cómo* mostrarlo (color, orden,
   *  agrupación) — el módulo solo declara el nivel, nunca fuerza su propio estilo. */
  attentionLevel: 'normal' | 'warning' | 'critical'

  /** Tamaño relativo en el grid. */
  size: 'sm' | 'md' | 'lg' | 'full'

  /** Cada cuánto se refresca. `manual` = solo por acción explícita del usuario. */
  refreshInterval: number | 'manual' | 'realtime'

  /** Acciones que el usuario puede disparar desde la card (ej. "Sincronizar", "Reintentar"). */
  actions?: ModuleAction[]
}

type PreviewType =
  | 'status'   // punto/badge de estado (online, offline, degradado)
  | 'metric'   // un número destacado + tendencia
  | 'chart'    // serie temporal o distribución
  | 'list'     // lista corta de ítems (últimos eventos, registros recientes)
  | 'log'      // salida de texto/consola (como el panel actual de API Response Data)
  | 'custom'   // el módulo aporta su propio componente de preview

interface InternalDataSource {
  kind: 'internal'
  /** Nombre de la store de Pinia o función que provee los datos. */
  source: string
}

interface IntegrationDataSource {
  kind: 'integration'
  /** Identificador de la integración configurada (ver §4 — credenciales nunca en el módulo). */
  integrationId: string
  endpoint: string
}

interface ModuleAction {
  id: string
  label: string
  /** Nombre de la función que ejecuta la acción — el módulo no maneja el evento directamente,
   *  lo declara para que el sistema decida cómo exponerlo (botón, menú, atajo). */
  handler: string
}
```

## 4. Integraciones externas — misma regla que ya existe para bases de datos

Un módulo con `dataSource.kind === 'integration'` **nunca** captura ni guarda credenciales desde el
GUI. Las credenciales de cualquier integración (API key, token, secreto) viven exclusivamente en
variables de entorno del servidor — el mismo principio ya aplicado a la configuración de base de
datos. El GUI solo permite elegir *qué* integración ya configurada usar, nunca ingresar el secreto.

## 5. Modos de vista (evaluado, no decidido)

La idea de "Simple / Atención / Pulso" como formas distintas de organizar el mismo conjunto de
módulos registrados — elegidas explícitamente por el usuario, nunca decididas en silencio por el
sistema — sigue en evaluación. No forma parte de este contrato todavía; se documentará por separado
cuando se decida.

## 6. Secuenciación

Este contrato **no se implementa de una sola vez**. Se valida primero contra 2-3 casos de uso reales
de ByteLab (el propio dashboard de monitoreo, más un CRM y un panel de e-commerce) antes de considerar
si vale la pena convertirlo en estándar abierto. Ver decisión registrada en memoria de sesión
(`dashboard-frontend-architecture`).
