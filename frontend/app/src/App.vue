<template>
  <v-app>
    <router-view />

    <v-snackbar
      v-model="uiStore.snackbar.show"
      :color="uiStore.snackbar.color"
      location="bottom right"
      :timeout="uiStore.snackbar.timeout"
      variant="elevated"
    >
      {{ uiStore.snackbar.text }}

      <template #actions>
        <v-btn icon="mdi-close" variant="text" @click="uiStore.snackbar.show = false" />
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup lang="ts">
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'
  import { useUiStore } from '@/stores/uiStore' // <--- NUEVO

  const authStore = useAuthStore()
  const uiStore = useUiStore() // <--- NUEVO
  const router = useRouter()

  // --- INTERCEPTORES AXIOS (Ahora con Loading y Notify) ---

  // 1. REQUEST (Salida)
  axios.interceptors.request.use((config) => {
    uiStore.startLoading() // Activamos barra de carga

    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  }, (error) => {
    uiStore.stopLoading()
    return Promise.reject(error)
  })

  // 2. RESPONSE (Llegada)
  axios.interceptors.response.use(
    (response) => {
      uiStore.stopLoading() // Apagamos barra de carga
      return response
    },
    (error) => {
      uiStore.stopLoading() // Apagamos barra de carga aunque falle

      // Manejo de 401 (Token vencido)
      if (error.response && error.response.status === 401) {
        uiStore.notify.error('Sesión expirada. Ingrese nuevamente.')
        authStore.logout()
        router.push('/login')
      }
      // Manejo de errores genéricos (Feedback visual)
      else if (error.code === 'ERR_NETWORK') {
        uiStore.notify.error('Error de conexión con el servidor')
      }

      return Promise.reject(error)
    }
  )
</script>
