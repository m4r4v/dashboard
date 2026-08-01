import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { useUiStore } from '@/stores/uiStore'

const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

httpClient.interceptors.request.use((config) => {
  const auth = useAuthStore()
  const ui = useUiStore()
  ui.startLoading()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

httpClient.interceptors.response.use(
  (response) => {
    useUiStore().stopLoading()
    return response
  },
  (error) => {
    const ui = useUiStore()
    ui.stopLoading()

    if (!error.response) {
      ui.notify('API fuera de línea.', 'error')
    } else if (error.response.status === 401) {
      ui.notify('Sesión expirada.', 'error')
      useAuthStore().logout()
    }

    return Promise.reject(error)
  },
)

export default httpClient
