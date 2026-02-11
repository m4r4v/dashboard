import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const isLoading = ref(false) // <--- RESTAURADO

  const isAuthenticated = computed(() => !!token.value)
  const isRoot = computed(() => isAuthenticated.value && user.value?.role === 'root')

  async function login(email, password) {
    isLoading.value = true // <--- AHORA EXISTE
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.post(`${API_URL}/api/auth/login`, { email, password })

      token.value = response.data.access_token
      user.value = { email, role: 'root' }

      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return true
    } finally {
      isLoading.value = false // <--- LIMPIEZA
    }
  }

  function logout() {
    localStorage.clear()
    token.value = null
    user.value = null
    router.push('/login')
  }

  return { token, user, isLoading, isAuthenticated, isRoot, login, logout }
})
