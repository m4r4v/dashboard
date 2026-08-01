<template>
  <router-view />
</template>

<script setup lang="ts">
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'
  import { useSystemStore } from '@/stores/systemStore'
  import { useUiStore } from '@/stores/uiStore'

  const authStore = useAuthStore()
  const uiStore = useUiStore()
  const router = useRouter()

  // --- INTERCEPTORES AXIOS (Silencio de Consola) ---

  axios.interceptors.request.use((config) => {
    uiStore.startLoading()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  }, (error) => {
    uiStore.stopLoading()
    return Promise.reject(error)
  })

  axios.interceptors.response.use(
    (response) => {
      uiStore.stopLoading()
      return response
    },
    (error) => {
      uiStore.stopLoading()

      if (!error.response) {
        uiStore.notify.error('API fuera de línea.')
        // Resolvemos la promesa silenciosamente para que el navegador no grite
        return Promise.resolve({ data: { status: 'offline' } })
      }

      else if (error.response.status === 401) {
        uiStore.notify.error('Sesión expirada.')
        authStore.logout()
      }

      return Promise.reject(error)
    }
  )
</script>
