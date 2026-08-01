import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useThemeConfigStore } from './themeConfigStore'

export const useThemeStore = defineStore('theme', () => {
  const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false
  const isDark = ref(prefersDark)

  applyClass()

  function toggleTheme () {
    isDark.value = !isDark.value
    applyClass()
    // El contraste de texto sobre primary/secondary depende de la superficie
    // (clara u oscura) contra la que se lee — recalcular al cambiar de modo.
    useThemeConfigStore().applyToDocument()
  }

  function applyClass () {
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  return { isDark, toggleTheme }
})
