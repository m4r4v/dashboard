<template>
  <v-app>
    <v-app-bar border color="surface" density="comfortable" elevation="0">
      <v-progress-linear
        absolute
        :active="uiStore.isLoading"
        bottom
        color="primary"
        height="2"
        indeterminate
      />

      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title class="text-uppercase font-weight-bold text-caption d-none d-sm-flex">
        Control Room <span class="text-primary ml-1">v1.3.0</span>
      </v-app-bar-title>

      <v-spacer />

      <div class="d-flex align-center gap-2 mr-2">
        <v-tooltip location="bottom">
          <template #activator="{ props }">
            <v-avatar
              v-bind="props"
              class="mr-2"
              :color="systemStore.isOnline ? 'success' : 'error'"
              size="10"
              style="box-shadow: 0 0 8px currentColor; cursor: help;"
            />
          </template>
          <span>API: {{ systemStore.isOnline ? 'Online' : 'Offline' }}</span>
        </v-tooltip>
        <span class="text-caption font-weight-bold text-medium-emphasis mr-4 text-uppercase">Api</span>

        <v-btn color="medium-emphasis" icon @click="toggleTheme">
          <v-icon>{{ theme.global.current.value.dark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
        </v-btn>
        <v-btn color="medium-emphasis" icon @click="logout">
          <v-icon color="error">mdi-logout</v-icon>
        </v-btn>
      </div>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" border elevation="0">
      <v-list nav>
        <v-list-item
          color="primary"
          prepend-icon="mdi-view-dashboard-outline"
          rounded="lg"
          title="Dashboard"
          to="/"
        />
      </v-list>
    </v-navigation-drawer>

    <v-main class="bg-grey-lighten-4">
      <router-view />
    </v-main>

    <v-snackbar v-model="uiStore.snackbar.show" :color="uiStore.snackbar.color" location="top right" variant="flat">
      {{ uiStore.snackbar.text }}
      <template #actions>
        <v-btn icon="mdi-close" variant="text" @click="uiStore.snackbar.show = false" />
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup lang="ts">
  import { onMounted, onUnmounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useTheme } from 'vuetify'
  import { useAuthStore } from '@/stores/authStore'
  import { useSystemStore } from '@/stores/systemStore'
  import { useUiStore } from '@/stores/uiStore'

  const drawer = ref(false)
  const theme = useTheme()
  const authStore = useAuthStore()
  const uiStore = useUiStore()
  const systemStore = useSystemStore()
  const router = useRouter()
  let statusInterval: any = null

  function toggleTheme () {
    theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  }

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

<style scoped>
.gap-2 { gap: 8px; }
</style>
