<template>
  <AppShell :logo-url="themeConfig.logoDataUrl" :nav-items="mainNavItems" title="Control Room">
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
            ? 'border-primary text-primary-text'
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
        <div class="space-y-7 p-4 text-sm text-gray-700 dark:text-gray-300">
          <section>
            <h3 class="mb-2 font-mono text-xs font-bold uppercase text-primary-text">Qué es este sistema</h3>
            <p>
              Control Room es un panel de administración con autenticación "Stateless Root": la identidad
              de administrador no depende de una base de datos, se verifica de forma criptográfica contra
              variables de entorno del servidor. Esto significa que podés acceder incluso si la
              persistencia principal está degradada.
            </p>
          </section>

          <section>
            <h3 class="mb-2 font-mono text-xs font-bold uppercase text-primary-text">Iniciar sesión</h3>
            <p class="mb-2">
              Ingresá con el correo y contraseña de la cuenta Root configurada para este servidor. Si las
              credenciales son incorrectas, el sistema responde igual sin importar si el correo existe o
              no — es intencional, para no revelar información a terceros.
            </p>
            <p>
              La sesión queda activa mientras el token siga vigente. Si te desconecta de forma
              inesperada, probablemente el token expiró — volvé a iniciar sesión.
            </p>
          </section>

          <section>
            <h3 class="mb-2 font-mono text-xs font-bold uppercase text-primary-text">El dashboard principal</h3>
            <p class="mb-2">
              El panel "API Response Data" consulta el estado del backend en tiempo real. Un fondo verde
              con <code class="rounded bg-surface-2 px-1 font-mono text-xs">"status": "online"</code>
              significa que el backend respondió correctamente; rojo indica que no pudo conectarse o
              respondió con error.
            </p>
            <p>
              El botón "Sincronizar" fuerza una consulta inmediata sin esperar al refresco automático. El
              punto junto a "API" en la barra superior muestra el mismo estado, visible desde cualquier
              pantalla del sistema.
            </p>
          </section>

          <section>
            <h3 class="mb-2 font-mono text-xs font-bold uppercase text-primary-text">Apariencia · General</h3>
            <p>
              Elegí un color primario (para botones y elementos interactivos) y uno secundario (acento
              estructural de los paneles), más una tipografía de una lista curada. Los cambios se ven de
              inmediato en toda la interfaz — no hace falta guardar aparte, cada ajuste se aplica y
              persiste en este navegador al instante.
            </p>
          </section>

          <section>
            <h3 class="mb-2 font-mono text-xs font-bold uppercase text-primary-text">Apariencia · Identidad</h3>
            <p class="mb-2">
              Subí tu logo corporativo (PNG, JPG o SVG, máximo 2MB). Aparece en la barra superior de
              todas las pantallas y en la pantalla de inicio de sesión.
            </p>
            <p>
              Al subirlo, el sistema analiza la imagen y sugiere colores dominantes extraídos de ella —
              son solo sugerencias, hacé clic en cualquiera para aplicarlo como color primario o
              secundario; nada se aplica automáticamente sin tu confirmación.
            </p>
          </section>

          <section>
            <h3 class="mb-2 font-mono text-xs font-bold uppercase text-primary-text">Próximamente · Módulos</h3>
            <p>
              Este dashboard va a poder ampliarse con módulos propios (monitoreo, métricas, un CRM, lo
              que necesite cada proyecto) — internos o conectados a una API externa. Todavía no está
              disponible; cuando lo esté, cada módulo va a declarar cómo se muestra (una tarjeta de
              estado, un número, un gráfico, una lista), de dónde saca sus datos y con qué frecuencia
              se actualiza, para que el sistema los pueda organizar sin conocer su lógica interna.
              Ninguna credencial de conexión se va a poder ingresar desde esta pantalla — como con la
              base de datos, eso siempre queda del lado del servidor.
            </p>
          </section>

          <section>
            <h3 class="mb-2 font-mono text-xs font-bold uppercase text-primary-text">Preguntas frecuentes</h3>
            <dl class="space-y-3">
              <div>
                <dt class="font-medium text-gray-900 dark:text-gray-100">¿Dónde se guarda mi configuración de apariencia hoy?</dt>
                <dd>En este navegador únicamente. Si entrás desde otro dispositivo o navegador, vas a ver la apariencia por defecto — la persistencia en servidor está planeada para una fase posterior.</dd>
              </div>
              <div>
                <dt class="font-medium text-gray-900 dark:text-gray-100">¿Por qué "API" aparece en rojo?</dt>
                <dd>El backend no respondió o respondió con error. Probá "Sincronizar"; si persiste, es un problema del servidor, no de tu sesión.</dd>
              </div>
              <div>
                <dt class="font-medium text-gray-900 dark:text-gray-100">¿Puedo volver a los colores originales?</dt>
                <dd>Sí, "Restaurar valores por defecto" en Apariencia → General borra tu personalización y vuelve a los colores base del sistema.</dd>
              </div>
            </dl>
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
