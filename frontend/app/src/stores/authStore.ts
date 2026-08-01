import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const email = ref<string | null>(localStorage.getItem('email'))
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  async function login (loginEmail: string, password: string, honeypot = '') {
    isLoading.value = true
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        email: loginEmail,
        password,
        honeypot,
      })

      token.value = response.data.access_token
      email.value = loginEmail

      localStorage.setItem('token', token.value as string)
      localStorage.setItem('email', loginEmail)
    } finally {
      isLoading.value = false
    }
  }

  function logout () {
    localStorage.clear()
    token.value = null
    email.value = null
    router.push('/login')
  }

  return { token, email, isLoading, isAuthenticated, login, logout }
})
