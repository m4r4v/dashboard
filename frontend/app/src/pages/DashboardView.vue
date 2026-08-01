<template>
  <AppShell :nav-items="navItems" title="Control Room">
    <template #actions>
      <StatusDot :status="systemStore.isOnline ? 'online' : 'offline'" label="API" />
      <button class="ml-2 rounded-full p-2 text-gray-500 hover:bg-primary/10 hover:text-primary" @click="themeStore.toggleTheme">
        <IconMdiWeatherSunny v-if="themeStore.isDark" class="h-5 w-5" />
        <IconMdiWeatherNight v-else class="h-5 w-5" />
      </button>
      <button class="rounded-full p-2 text-error hover:bg-error/10" @click="authStore.logout">
        <IconMdiLogout class="h-5 w-5" />
      </button>
    </template>

    <div class="p-6">
      <h2 class="mb-6 font-mono text-2xl font-bold text-gray-900 dark:text-gray-100">System Dashboard</h2>

      <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
        <SystemStatusDisplay />
      </div>
    </div>
  </AppShell>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'
  import AppShell from '@/components/ui/AppShell.vue'
  import StatusDot from '@/components/ui/StatusDot.vue'
  import SystemStatusDisplay from '@/components/SystemStatusDisplay.vue'
  import { useAuthStore } from '@/stores/authStore'
  import { useSystemStore } from '@/stores/systemStore'
  import { useThemeStore } from '@/stores/themeStore'

  const authStore = useAuthStore()
  const systemStore = useSystemStore()
  const themeStore = useThemeStore()

  const navItems = [
    { label: 'Dashboard', to: '/' },
  ]

  onMounted(() => {
    systemStore.fetchStatus()
  })
</script>
