import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useSystemStore = defineStore('system', () => {
  const status = ref(null)
  const isLoading = ref(false)

  const isOnline = computed(() => status.value?.status === 'online')

  async function fetchStatus() {
    if (isLoading.value) {return}

    try {
      isLoading.value = true
      const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const { data } = await axios.get(`${baseUrl}/api/system/status`)
      status.value = data
    } catch {
      status.value = { status: 'offline' }
    } finally {
      isLoading.value = false
    }
  }

  return { status, isOnline, fetchStatus, isLoading }
})
