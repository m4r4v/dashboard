<template>
  <AppShell :nav-items="mainNavItems" title="Control Room">
    <template #actions>
      <button class="rounded-full p-2 text-gray-500 hover:bg-primary/10 hover:text-primary" @click="themeStore.toggleTheme">
        <IconMdiWeatherSunny v-if="themeStore.isDark" class="h-5 w-5" />
        <IconMdiWeatherNight v-else class="h-5 w-5" />
      </button>
      <button class="rounded-full p-2 text-error hover:bg-error/10" @click="authStore.logout">
        <IconMdiLogout class="h-5 w-5" />
      </button>
    </template>

    <div class="p-6">
      <h2 class="mb-6 font-mono text-2xl font-bold text-gray-900 dark:text-gray-100">Configuración</h2>

      <div class="mb-6 flex gap-1 border-b border-brand-border">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="border-b-2 px-4 py-2 text-sm font-medium transition"
          :class="activeTab === tab.key
            ? 'border-primary text-primary'
            : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400'"
          type="button"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Apariencia > General -->
      <GlassPanel v-if="activeTab === 'general'" class="max-w-lg" title="Apariencia · General">
        <div class="space-y-6 p-4">
          <ColorPicker v-model="primaryDraft" label="Color primario" />
          <ColorPicker v-model="secondaryDraft" label="Color secundario" />
          <FontSelect v-model="fontDraft" label="Tipografía" :options="FONT_OPTIONS" />

          <button
            class="text-xs font-medium text-gray-500 hover:text-error dark:text-gray-400"
            type="button"
            @click="onReset"
          >
            Restaurar valores por defecto
          </button>
        </div>
      </GlassPanel>

      <!-- Apariencia > Identidad -->
      <GlassPanel v-else-if="activeTab === 'identidad'" class="max-w-lg" title="Apariencia · Identidad">
        <div class="space-y-4 p-4">
          <LogoUploader v-model="logoDraft" @file-selected="onLogoFile" />

          <div v-if="suggestedColors.length" class="rounded-md bg-primary/5 p-3">
            <p class="mb-2 text-xs font-medium text-gray-600 dark:text-gray-300">
              Colores sugeridos a partir del logo — hacé clic para aplicar:
            </p>
            <div class="flex gap-2">
              <button
                v-for="color in suggestedColors"
                :key="color"
                class="h-8 w-8 rounded-md border border-brand-border transition hover:scale-110"
                :style="{ backgroundColor: color }"
                :title="color"
                type="button"
                @click="applySuggestedColor(color)"
              />
            </div>
          </div>
        </div>
      </GlassPanel>

      <!-- Ayuda -->
      <GlassPanel v-else class="max-w-2xl" title="Ayuda">
        <div class="space-y-5 p-4 text-sm text-gray-700 dark:text-gray-300">
          <section>
            <h3 class="mb-1 font-mono text-xs font-bold uppercase text-primary">Iniciar sesión</h3>
            <p>Ingresá con el correo y contraseña de la cuenta Root del sistema. La sesión se mantiene hasta que cierres sesión o expire el token.</p>
          </section>
          <section>
            <h3 class="mb-1 font-mono text-xs font-bold uppercase text-primary">Usar el dashboard</h3>
            <p>El panel "API Response Data" muestra el estado en vivo del backend, con un botón para sincronizar manualmente. El indicador junto a "API" en la barra superior refleja lo mismo en todo momento.</p>
          </section>
          <section>
            <h3 class="mb-1 font-mono text-xs font-bold uppercase text-primary">Cambiar apariencia</h3>
            <p>En Configuración → Apariencia podés elegir tus colores de marca y tipografía, y subir tu logo corporativo. Los cambios se aplican y se guardan al instante en este navegador.</p>
          </section>
        </div>
      </GlassPanel>
    </div>
  </AppShell>
</template>

<script setup lang="ts">
  import { ref, watch } from 'vue'
  import AppShell from '@/components/ui/AppShell.vue'
  import GlassPanel from '@/components/ui/GlassPanel.vue'
  import ColorPicker from '@/components/ui/ColorPicker.vue'
  import FontSelect from '@/components/ui/FontSelect.vue'
  import LogoUploader from '@/components/ui/LogoUploader.vue'
  import { mainNavItems } from '@/navigation'
  import { extractDominantColors } from '@/services/colorExtraction'
  import { useAuthStore } from '@/stores/authStore'
  import { FONT_OPTIONS, useThemeConfigStore } from '@/stores/themeConfigStore'
  import { useThemeStore } from '@/stores/themeStore'

  const DEFAULT_PRIMARY = '#0891b2'
  const DEFAULT_SECONDARY = '#a21caf'

  const authStore = useAuthStore()
  const themeStore = useThemeStore()
  const themeConfig = useThemeConfigStore()

  type TabKey = 'general' | 'identidad' | 'ayuda'
  const tabs: { key: TabKey; label: string }[] = [
    { key: 'general', label: 'General' },
    { key: 'identidad', label: 'Identidad' },
    { key: 'ayuda', label: 'Ayuda' },
  ]
  const activeTab = ref<TabKey>('general')

  const primaryDraft = ref(themeConfig.primaryColor ?? DEFAULT_PRIMARY)
  const secondaryDraft = ref(themeConfig.secondaryColor ?? DEFAULT_SECONDARY)
  const fontDraft = ref(themeConfig.fontKey)
  const logoDraft = ref(themeConfig.logoDataUrl)
  const suggestedColors = ref<string[]>([])

  // Aplicar en vivo (auto-guardado en localStorage vía el store).
  watch([primaryDraft, secondaryDraft], ([p, s]) => themeConfig.setColors(p, s))
  watch(fontDraft, key => themeConfig.setFont(key))
  watch(logoDraft, url => themeConfig.setLogo(url))

  async function onLogoFile (file: File) {
    suggestedColors.value = await extractDominantColors(file)
  }

  function applySuggestedColor (color: string) {
    if (!primaryDraft.value || primaryDraft.value === DEFAULT_PRIMARY) {
      primaryDraft.value = color
    } else {
      secondaryDraft.value = color
    }
  }

  function onReset () {
    themeConfig.resetToDefaults()
    primaryDraft.value = DEFAULT_PRIMARY
    secondaryDraft.value = DEFAULT_SECONDARY
    fontDraft.value = 'system'
    logoDraft.value = null
    suggestedColors.value = []
  }
</script>
