<template>
  <v-container v-if="authStore.isAuthenticated" class="pa-6" fluid>

    <v-row align="center" class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-primary">System Dashboard</h1>
        <div class="text-subtitle-1 text-medium-emphasis">
          Nodo: <span class="text-info font-weight-bold">{{ node_id }}</span>
        </div>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="error"
          prepend-icon="mdi-logout"
          variant="tonal"
          @click="authStore.logout"
        >
          Cerrar Sesión
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" :md="authStore.isRoot ? 6 : 12">
        <SystemStatusDisplay />
      </v-col>

      <v-col v-if="authStore.isRoot" cols="12" md="6">
        <NodeControlPanel />
      </v-col>
    </v-row>
  </v-container>

  <v-container v-else class="fill-height d-flex align-center justify-center">
    <v-progress-circular color="primary" indeterminate size="64" />
  </v-container>
</template>

<script setup lang="ts">
  import { computed, onMounted, watchEffect } from 'vue'
  import { useRouter } from 'vue-router'
  import NodeControlPanel from '@/components/NodeControlPanel.vue'
  import SystemStatusDisplay from '@/components/SystemStatusDisplay.vue'
  import { useAuthStore } from '@/stores/authStore'
  import { useSystemStore } from '@/stores/systemStore'

  const authStore = useAuthStore()
  const systemStore = useSystemStore()
  const router = useRouter()

  const node_id = computed(() => systemStore.status?.node_id || 'Cargando...')

  // Seguridad Reactiva: Si el estado cambia a "no autenticado", fuera de aquí.
  watchEffect(() => {
    if (!authStore.isAuthenticated) {
      router.push('/login')
    }
  })

  onMounted(async () => {
    if (authStore.isAuthenticated) {
      await systemStore.fetchStatus()
    }
  })
</script>
