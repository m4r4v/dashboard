<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Barra de carga global -->
    <div
      class="fixed inset-x-0 top-0 z-50 h-0.5 bg-primary transition-opacity"
      :class="uiStore.isLoading ? 'opacity-100 animate-pulse' : 'opacity-0'"
    />

    <header class="sticky top-0 z-40 flex items-center border-b border-gray-200 bg-white px-4 py-3 dark:border-gray-700 dark:bg-gray-800">
      <button class="mr-3 text-gray-500 hover:text-gray-700 dark:text-gray-400" @click="drawer = !drawer">
        <IconMdiMenu class="h-6 w-6" />
      </button>

      <h1 class="hidden text-xs font-bold uppercase tracking-wide text-gray-700 sm:block dark:text-gray-200">
        Dasboard Infraestructura
      </h1>

      <div class="flex-1" />

      <div class="flex items-center gap-2">
        <span
          class="mr-1 inline-block h-2.5 w-2.5 rounded-full"
          :class="systemStore.isOnline ? 'bg-success' : 'bg-error'"
          :style="{ boxShadow: `0 0 8px currentColor`, color: systemStore.isOnline ? 'var(--color-success)' : 'var(--color-error)' }"
          :title="`API: ${systemStore.isOnline ? 'Online' : 'Offline'}`"
        />
        <span class="mr-4 text-xs font-bold uppercase text-gray-500 dark:text-gray-400">Api</span>

        <button
          class="rounded-full p-2 text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
          @click="themeStore.toggleTheme"
        >
          <IconMdiWeatherSunny v-if="themeStore.isDark" class="h-5 w-5" />
          <IconMdiWeatherNight v-else class="h-5 w-5" />
        </button>
        <button
          class="rounded-full p-2 text-error hover:bg-error/10"
          @click="logout"
        >
          <IconMdiLogout class="h-5 w-5" />
        </button>
      </div>
    </header>

    <!-- Drawer mobile: panel simple + backdrop, sin Reka UI en esta pasada -->
    <div v-if="drawer" class="fixed inset-0 z-30 bg-black/40" @click="drawer = false" />
    <aside
      class="fixed inset-y-0 left-0 z-40 w-64 -translate-x-full border-r border-gray-200 bg-white p-4 transition-transform dark:border-gray-700 dark:bg-gray-800"
      :class="drawer ? 'translate-x-0' : ''"
    >
      <router-link
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-primary hover:bg-primary/10"
        to="/"
        @click="drawer = false"
      >
        <IconMdiViewDashboardOutline class="h-5 w-5" />
        Dashboard
      </router-link>
    </aside>

    <main>
      <router-view />
    </main>

    <!-- Snackbar -->
    <div
      v-if="uiStore.snackbar.show"
      class="fixed right-4 top-4 z-50 flex items-center gap-3 rounded-md px-4 py-3 text-sm text-white shadow-lg"
      :class="snackbarColor"
    >
      {{ uiStore.snackbar.text }}
      <button class="text-white/80 hover:text-white" @click="uiStore.snackbar.show = false">
        <IconMdiClose class="h-4 w-4" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, onMounted, onUnmounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'
  import { useSystemStore } from '@/stores/systemStore'
  import { useThemeStore } from '@/stores/themeStore'
  import { useUiStore } from '@/stores/uiStore'

  const drawer = ref(false)
  const themeStore = useThemeStore()
  const authStore = useAuthStore()
  const uiStore = useUiStore()
  const systemStore = useSystemStore()
  const router = useRouter()
  let statusInterval: any = null

  const snackbarColor = computed(() => ({
    success: 'bg-success',
    error: 'bg-error',
    warning: 'bg-warning',
    info: 'bg-info',
  }[uiStore.snackbar.color] || 'bg-info'))

  function logout () {
    authStore.logout()
    router.push('/login')
  }

  onMounted(() => {
    systemStore.fetchStatus()
    statusInterval = setInterval(() => { systemStore.fetchStatus() }, 30_000)
  })

  onUnmounted(() => { if (statusInterval) clearInterval(statusInterval) })
</script>
