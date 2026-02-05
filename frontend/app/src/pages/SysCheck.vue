<template>
  <v-container class="fill-height justify-center">
    <v-card elevation="4" rounded="lg" width="600">
      <v-card-item>
        <v-card-title class="text-h5 font-weight-bold d-flex align-center">
          <v-icon color="primary" icon="mdi-connection" start />
          Diagnóstico de Sistema
        </v-card-title>
        <v-card-subtitle>Integración Frontend-Backend</v-card-subtitle>
      </v-card-item>

      <v-divider />

      <v-card-text class="py-6">
        <div v-if="loading" class="d-flex flex-column align-center gap-4 py-4">
          <v-progress-circular color="primary" indeterminate size="48" />
          <div class="text-body-1 mt-4 text-medium-emphasis">Intentando handshake con API...</div>
          <div class="text-caption text-disabled font-family-monospace">Target: {{ apiUrl }}</div>
        </div>

        <v-alert
          v-else-if="error"
          border="start"
          class="mb-0"
          type="error"
          variant="tonal"
        >
          <template #title>Fallo de Conexión</template>
          <div class="text-body-2">{{ error }}</div>
          <div class="text-caption mt-2 font-weight-bold">Posibles causas:</div>
          <ul class="text-caption pl-4 mt-1">
            <li>El Backend no está corriendo (puerto 8000).</li>
            <li>Bloqueo de CORS (revisar consola del navegador).</li>
            <li>Variable VITE_API_URL incorrecta.</li>
          </ul>
        </v-alert>

        <v-alert
          v-else-if="backendData"
          border="start"
          class="mb-0"
          type="success"
          variant="tonal"
        >
          <template #title>¡Enlace Exitoso!</template>
          <div class="d-flex flex-column gap-2 mt-2">
            <div class="d-flex justify-space-between">
              <span class="text-medium-emphasis">Servicio:</span>
              <strong class="font-family-monospace">{{ backendData.service }}</strong>
            </div>
            <div class="d-flex justify-space-between">
              <span class="text-medium-emphasis">Estado:</span>
              <v-chip color="success" label size="x-small">{{ backendData.status }}</v-chip>
            </div>
            <v-divider class="my-2" />
            <div class="text-caption text-medium-emphasis">
              Respuesta recibida desde <code class="bg-surface-variant px-1 rounded">{{ apiUrl }}</code>
            </div>
          </div>
        </v-alert>
      </v-card-text>

      <v-card-actions class="pa-4 bg-grey-lighten-4">
        <v-spacer />
        <v-btn
          color="primary"
          :loading="loading"
          prepend-icon="mdi-refresh"
          variant="elevated"
          @click="checkStatus"
        >
          Probar Conexión
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
  import { onMounted, ref } from 'vue'

  // CORRECCIÓN 1: Iniciar loading en true para evitar renderizado prematuro
  const loading = ref(true)
  const error = ref(null)
  const backendData = ref(null)
  const apiUrl = import.meta.env.VITE_API_URL

  async function checkStatus () {
    loading.value = true
    error.value = null
    // CORRECCIÓN 2: Resetear data al reintentar
    backendData.value = null

    try {
      if (!apiUrl) throw new Error('VITE_API_URL no está definida en .env')

      console.log(`[SysCheck] Iniciando petición a: ${apiUrl}/`)

      const response = await fetch(`${apiUrl}/`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      console.log('[SysCheck] Respuesta recibida:', data)
      backendData.value = data

    } catch (error_) {
      console.error('[SysCheck] Error:', error_)
      error.value = error_ instanceof Error ? error_.message : 'Error desconocido de red';
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    checkStatus()
  })
</script>

<style scoped>
.gap-4 { gap: 16px; }
.font-family-monospace { font-family: monospace; }
</style>

<route lang="yaml">
path: /sys-check
meta:
  layout: false
</route>
