import { defineStore } from 'pinia'
import { ref } from 'vue'
import httpClient from '@/services/httpClient'

export const useNodeStore = defineStore('node', () => {
  const nodeInfo = ref(null)
  const logs = ref([])
  const isLoading = ref(false)
  const isActionPending = ref(false)

  // 1. Identidad y Salud (Node ID + Uptime + RAM)
  // [CORREGIDO] Estas 3 rutas son protegidas (Depends(get_current_root) en el
  // backend) y antes se llamaban sin el header Authorization -> 403 silencioso
  // siempre. httpClient lo adjunta automáticamente vía interceptor.
  async function fetchNodeStatus() {
    isLoading.value = true
    try {
      const { data } = await httpClient.get('/api/node/status')
      nodeInfo.value = data
    } catch {
      nodeInfo.value = null
    } finally {
      isLoading.value = false
    }
  }

  // 2. Búfer de Eventos (Ruta B)
  async function fetchLogs() {
    try {
      const { data } = await httpClient.get('/api/node/logs')
      logs.value = data
    } catch {
      logs.value = []
    }
  }

  // 3. Acciones de Mantenimiento (Ruta A)
  async function triggerAction(actionName) {
    if (isActionPending.value) {return}

    isActionPending.value = true
    try {
      const { data } = await httpClient.post('/api/node/action', null, {
        params: { action: actionName }
      })

      // Actualización inmediata del flujo de eventos
      await fetchLogs()
      return data.msg
    } finally {
      // El error sube automáticamente a la vista y aquí solo limpiamos el estado
      isActionPending.value = false
    }
  }

  return {
    nodeInfo,
    logs,
    isLoading,
    isActionPending,
    fetchNodeStatus,
    fetchLogs,
    triggerAction
  }
})
