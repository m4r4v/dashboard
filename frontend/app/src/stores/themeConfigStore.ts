import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ensureReadableAsText, getContrastingColor } from '@/services/colorContrast'

const STORAGE_KEY = 'themeConfig'

export interface FontOption {
  key: string
  label: string
  family: string
}

export const FONT_OPTIONS: FontOption[] = [
  { key: 'inter', label: 'Inter', family: "'Inter', ui-sans-serif, system-ui, sans-serif" },
  { key: 'roboto', label: 'Roboto', family: "'Roboto', ui-sans-serif, system-ui, sans-serif" },
  { key: 'ibm-plex-sans', label: 'IBM Plex Sans', family: "'IBM Plex Sans', ui-sans-serif, system-ui, sans-serif" },
  { key: 'system', label: 'Sistema (default)', family: 'ui-sans-serif, system-ui, sans-serif' },
]

interface ThemeConfigState {
  primaryColor: string | null
  secondaryColor: string | null
  fontKey: string
  logoDataUrl: string | null
}

function loadFromStorage (): ThemeConfigState {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) {
    return { primaryColor: null, secondaryColor: null, fontKey: 'system', logoDataUrl: null }
  }
  try {
    return { ...JSON.parse(raw) }
  } catch {
    return { primaryColor: null, secondaryColor: null, fontKey: 'system', logoDataUrl: null }
  }
}

export const useThemeConfigStore = defineStore('themeConfig', () => {
  const initial = loadFromStorage()

  const primaryColor = ref<string | null>(initial.primaryColor)
  const secondaryColor = ref<string | null>(initial.secondaryColor)
  const fontKey = ref<string>(initial.fontKey)
  const logoDataUrl = ref<string | null>(initial.logoDataUrl)

  function applyColorContrast (root: HTMLElement, cssVar: string, color: string) {
    const surface = getComputedStyle(root).getPropertyValue('--brand-surface').trim() || '#ffffff'
    root.style.setProperty(`--brand-${cssVar}`, color)
    root.style.setProperty(`--brand-${cssVar}-contrast`, getContrastingColor(color))
    root.style.setProperty(`--brand-${cssVar}-text`, ensureReadableAsText(color, surface))
  }

  function applyToDocument () {
    const root = document.documentElement
    if (primaryColor.value) applyColorContrast(root, 'primary', primaryColor.value)
    if (secondaryColor.value) applyColorContrast(root, 'secondary', secondaryColor.value)

    const font = FONT_OPTIONS.find(f => f.key === fontKey.value) ?? FONT_OPTIONS[FONT_OPTIONS.length - 1]
    root.style.setProperty('--brand-font', font.family)
  }

  function persist () {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      primaryColor: primaryColor.value,
      secondaryColor: secondaryColor.value,
      fontKey: fontKey.value,
      logoDataUrl: logoDataUrl.value,
    }))
  }

  function setColors (primary: string | null, secondary: string | null) {
    primaryColor.value = primary
    secondaryColor.value = secondary
    applyToDocument()
    persist()
  }

  function setFont (key: string) {
    fontKey.value = key
    applyToDocument()
    persist()
  }

  function setLogo (dataUrl: string | null) {
    logoDataUrl.value = dataUrl
    persist()
  }

  function resetToDefaults () {
    primaryColor.value = null
    secondaryColor.value = null
    fontKey.value = 'system'
    logoDataUrl.value = null
    for (const prop of ['primary', 'secondary']) {
      document.documentElement.style.removeProperty(`--brand-${prop}`)
      document.documentElement.style.removeProperty(`--brand-${prop}-contrast`)
      document.documentElement.style.removeProperty(`--brand-${prop}-text`)
    }
    document.documentElement.style.removeProperty('--brand-font')
    localStorage.removeItem(STORAGE_KEY)
  }

  // Aplicar de inmediato al crear el store (boot de la app), para que no haya "flash" sin marca.
  applyToDocument()

  return {
    primaryColor,
    secondaryColor,
    fontKey,
    logoDataUrl,
    applyToDocument,
    setColors,
    setFont,
    setLogo,
    resetToDefaults,
  }
})
