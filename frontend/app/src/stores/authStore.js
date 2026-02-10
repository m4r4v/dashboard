import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email, password) {
    isLoading.value = true
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

      const response = await axios.post(`${API_URL}/api/auth/login`, {
        email,
        password
      })

      const newToken = response.data.access_token
      token.value = newToken
      localStorage.setItem('token', newToken)
      user.value = { email, role: 'root' }

      return true
    } finally {
      // El error fluye automáticamente a la vista sin necesidad de un catch vacío
      isLoading.value = false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    router.push('/login')
  }

  return {
    token,
    user,
    isLoading,
    isAuthenticated,
    login,
    logout
  }
})
