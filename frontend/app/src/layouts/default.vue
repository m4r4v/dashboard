<template>
  <v-app-bar border color="surface" density="comfortable" elevation="0">
    <template v-if="uiStore.isLoading" #extension>
      <v-progress-linear color="primary" height="2" indeterminate />
    </template>

    <v-app-bar-nav-icon @click="drawer = !drawer" />

    <v-app-bar-title class="text-uppercase font-weight-bold text-caption d-none d-sm-flex">
      Control Room <span class="text-primary ml-1">v1.2.0</span>
    </v-app-bar-title>

    <v-spacer />

    <div class="d-flex align-center gap-2 mr-2">

      <v-btn color="medium-emphasis" icon @click="toggleTheme">
        <v-icon>{{ theme.global.current.value.dark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
        <v-tooltip activator="parent" location="bottom">Toggle Theme</v-tooltip>
      </v-btn>

      <v-btn color="medium-emphasis" icon>
        <v-badge color="error" dot>
          <v-icon>mdi-bell-outline</v-icon>
        </v-badge>
      </v-btn>

      <v-menu min-width="200px" rounded>
        <template #activator="{ props }">
          <v-btn v-bind="props" class="ml-1" icon>
            <v-avatar color="primary" size="32">
              <span class="text-caption font-weight-bold text-white">RA</span>
            </v-avatar>
          </v-btn>
        </template>
        <v-card>
          <v-list-item
            class="pb-4 pt-4"
            prepend-avatar="https://cdn.vuetifyjs.com/images/john.jpg"
            subtitle="admin@dashboard.com"
            title="Root Admin"
          >
            <template #prepend>
              <v-avatar color="primary"><v-icon color="white" icon="mdi-account" /></v-avatar>
            </template>
          </v-list-item>
          <v-divider />
          <v-list density="compact">
            <v-list-item prepend-icon="mdi-cog-outline" title="My Account" value="account" />
            <v-list-item color="error" prepend-icon="mdi-logout" title="Logout" @click="handleLogout" />
          </v-list>
        </v-card>
      </v-menu>
    </div>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" color="background" elevation="1">
    <div class="pa-4 d-flex align-center justify-center">
      <v-icon class="mr-2" color="primary" icon="mdi-chart-box" size="40" />
      <div>
        <div class="text-h6 font-weight-bold text-primary" style="line-height: 1.2">DASHBOARD</div>
        <div class="text-caption text-medium-emphasis">Control Room</div>
      </div>
    </div>

    <v-divider class="mb-2" />

    <v-list class="pa-2" density="compact" nav>
      <v-list-subheader class="text-caption text-uppercase font-weight-bold mb-2">Main</v-list-subheader>

      <v-list-item
        color="primary"
        prepend-icon="mdi-view-dashboard-outline"
        rounded="lg"
        title="Dashboard"
        to="/"
      />

      <v-list-subheader class="text-caption text-uppercase font-weight-bold mt-4 mb-2">Administration</v-list-subheader>

      <v-list-item
        color="primary"
        disabled
        prepend-icon="mdi-account-group-outline"
        rounded="lg"
        title="Users"
        value="users"
      />

      <v-list-item
        color="primary"
        disabled
        prepend-icon="mdi-tune"
        rounded="lg"
        title="Settings"
        value="settings"
      />
    </v-list>

    <template #append>
      <div class="pa-4 text-center">
        <v-chip color="medium-emphasis" size="x-small" variant="outlined">
          System Active • v1.2.0
        </v-chip>
      </div>
    </template>
  </v-navigation-drawer>

  <v-main class="bg-grey-lighten-4">
    <router-view />
  </v-main>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useTheme } from 'vuetify'
  import { useAuthStore } from '@/stores/authStore'
  import { useUiStore } from '@/stores/uiStore'

  const drawer = ref(true)
  const theme = useTheme()
  const authStore = useAuthStore()
  const uiStore = useUiStore()

  function handleLogout() {
    uiStore.notify.info('Logging out securely...')
    authStore.logout()
  }

  function toggleTheme() {
    theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  }
</script>
