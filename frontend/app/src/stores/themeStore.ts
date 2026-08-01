import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false
  const isDark = ref(prefersDark)

  applyClass()

  function toggleTheme () {
    isDark.value = !isDark.value
    applyClass()
  }

  function applyClass () {
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  return { isDark, toggleTheme }
})
