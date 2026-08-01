import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import httpClient from '@/services/httpClient'

export interface SystemStatus {
  status: string
  api_version: string
}

export const useSystemStore = defineStore('system', () => {
  const status = ref<SystemStatus | null>(null)
  const isLoading = ref(false)

  const isOnline = computed(() => status.value?.status === 'online')

  async function fetchStatus () {
    if (isLoading.value) return
    isLoading.value = true
    try {
      const { data } = await httpClient.get<SystemStatus>('/api/system/status')
      status.value = data
    } catch {
      status.value = { status: 'offline', api_version: '' }
    } finally {
      isLoading.value = false
    }
  }

  return { status, isOnline, isLoading, fetchStatus }
})
