/**
 * Auth Store (Pinia)
 * Gestión de estado de identidad y sesión.
 */
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import router from '@/router'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // --- STATE (Estado Reactivo) ---
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const loading = ref(false)
  const error = ref(null)

  // --- GETTERS (Propiedades Computadas) ---
  const isAuthenticated = computed(() => !!token.value)

  // --- ACTIONS (Lógica de Negocio) ---

  /**
   * Iniciar Sesión (OAuth2 Standard Flow)
   * @param {string} email - Se enviará como 'username' según RFC 6749
   * @param {string} password
   */
  async function login(email, password) {
    loading.value = true
    error.value = null

    try {
      // 1. Preparar Form Data (application/x-www-form-urlencoded)
      const formData = new URLSearchParams()
      formData.append('username', email) // Mapping crítico: Email -> Username standard
      formData.append('password', password)

      // 2. Petición al Backend
      const response = await api.post('/api/v1/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })

      // 3. Extraer datos
      const { access_token } = response.data

      // 4. Persistir en Storage
      localStorage.setItem('token', access_token)
      const userData = { email, role: 'superadmin' }
      localStorage.setItem('user', JSON.stringify(userData))

      // 5. Actualizar Estado
      token.value = access_token
      user.value = userData

      return true

    } catch (error_) {
      console.error('Login error:', error_)

      // CORRECCIÓN ESLINT: Uso de operador lógico OR (||) en lugar de ternario redundante
      error.value = error_.response?.data?.detail || 'Error de conexión o servidor no disponible'

      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Cerrar Sesión
   */
  function logout() {
    // 1. Limpiar Estado
    token.value = null
    user.value = null
    error.value = null

    // 2. Limpiar Storage
    localStorage.removeItem('token')
    localStorage.removeItem('user')

    // 3. Redirigir al Login
    router.push('/login')
  }

  return {
    // State
    token,
    user,
    loading,
    error,
    // Getters
    isAuthenticated,
    // Actions
    login,
    logout
  }
})
