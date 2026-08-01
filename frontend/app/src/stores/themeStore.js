import { defineStore } from 'pinia'
import { ref } from 'vue'

// Setup Store (patrón vuejs-tailwind-m4r4v): Tailwind no trae theme system
// propio como Vuetify — el toggle alterna la clase "dark" en <html>, que
// activa el @custom-variant definido en style.css.
export const useThemeStore = defineStore('theme', () => {
  const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches
  const isDark = ref(prefersDark ?? false)

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
