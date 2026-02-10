import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // --- ESTADO ---
  // Inicializamos leyendo del storage para no perder sesión al recargar (F5)
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null) // Aquí guardaremos datos básicos (email, rol)

  // --- GETTERS ---
  const isAuthenticated = computed(() => !!token.value)

  // --- ACCIONES ---

  // 1. Iniciar Sesión
  async function login(email, password) {
    try {
      // Docker inyecta la URL correcta. Fallback a localhost para dev local.
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

      const response = await axios.post(`${API_URL}/api/auth/login`, {
        email,
        password
      })

      // EXTRACCIÓN DEL TOKEN
      const newToken = response.data.access_token

      // 1. Guardar en Estado (Reactividad)
      token.value = newToken

      // 2. Persistir en Disco (Sobrevivir al F5)
      localStorage.setItem('token', newToken)

      // 3. Setear usuario (Mockup por ahora, luego lo decodificamos del JWT)
      user.value = { email, role: 'root' }

      return true // Retornamos éxito a la Vista
    } catch (error) {
      console.error('Login Failed:', error)
      throw error // Lanzamos el error para que la Vista muestre la alerta roja
    }
  }

  // 2. Cerrar Sesión
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')

    // Redirigir forzosamente al login
    router.push('/login')
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout
  }
})
