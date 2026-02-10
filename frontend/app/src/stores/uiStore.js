import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  // --- ESTADO: SNACKBAR (Notificaciones) ---
  const snackbar = ref({
    show: false,
    text: '',
    color: 'info',
    timeout: 3000
  })

  // --- ESTADO: LOADING (Barra de carga global) ---
  const isLoading = ref(false)

  // --- ACCIONES ---

  // Mostrar mensaje
  function showMessage(text, color = 'info') {
    snackbar.value = {
      show: true,
      text,
      color,
      timeout: 3000
    }
  }

  // Helpers rápidos
  const notify = {
    success: (msg) => showMessage(msg, 'success'),
    error: (msg) => showMessage(msg, 'error'),
    info: (msg) => showMessage(msg, 'info'),
    warning: (msg) => showMessage(msg, 'warning')
  }

  // Control de carga
  function startLoading() { isLoading.value = true }
  function stopLoading() { isLoading.value = false }

  return {
    snackbar,
    isLoading,
    notify,
    startLoading,
    stopLoading
  }
})
