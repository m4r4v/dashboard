import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

// Instancia única de axios: adjunta el token JWT automáticamente a toda
// llamada que pase por acá, en vez de repetir el header en cada store
// (bug real detectado: nodeStore.js llamaba a rutas protegidas sin él).
const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

httpClient.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

export default httpClient
