/**
 * Service Layer: Cliente HTTP Único
 * Todas las peticiones al backend deben pasar por aquí.
 */
import axios from 'axios'

// 1. Crear instancia con configuración base
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10_000, // 10 segundos de espera máxima
})

// 2. Interceptor de Request (Inyección de Token)
api.interceptors.request.use(
  (config) => {
    // Leemos el token del almacenamiento local
    const token = localStorage.getItem('token')

    // Si existe, lo inyectamos en el header Authorization
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 3. Interceptor de Response (Manejo Global de Errores)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Si el backend dice "401 Unauthorized" (Token inválido o expirado)
    if (error.response && error.response.status === 401) {
      // Limpiamos la basura local
      localStorage.removeItem('token')
      localStorage.removeItem('user')

      // Opcional: Redirigir al login si estamos en el navegador
      // window.location.href = '/login'
      // (Lo manejaremos mejor con el Router luego)
    }
    return Promise.reject(error)
  }
)

export default api
