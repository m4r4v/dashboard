import { defineStore } from 'pinia'
import { ref } from 'vue'

export type SnackbarColor = 'success' | 'error' | 'warning' | 'info'

export const useUiStore = defineStore('ui', () => {
  const isLoading = ref(false)
  const snackbar = ref<{ show: boolean; text: string; color: SnackbarColor }>({
    show: false,
    text: '',
    color: 'info',
  })

  function startLoading () { isLoading.value = true }
  function stopLoading () { isLoading.value = false }

  function notify (text: string, color: SnackbarColor = 'info') {
    snackbar.value = { show: true, text, color }
  }

  return { isLoading, snackbar, startLoading, stopLoading, notify }
})
