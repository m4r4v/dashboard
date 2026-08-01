<template>
  <div v-if="authStore.isAuthenticated" class="p-6">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-primary">System Dashboard</h1>
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Nodo: <span class="font-bold text-info">{{ node_id }}</span>
        </div>
      </div>
      <button
        class="flex items-center gap-2 rounded-md bg-error/10 px-4 py-2 text-sm font-medium text-error hover:bg-error/20"
        @click="authStore.logout"
      >
        <IconMdiLogout class="h-4 w-4" />
        Cerrar Sesión
      </button>
    </div>

    <div class="grid grid-cols-1 gap-6" :class="authStore.isRoot ? 'md:grid-cols-2' : ''">
      <SystemStatusDisplay />
      <NodeControlPanel v-if="authStore.isRoot" />
    </div>
  </div>

  <div v-else class="flex min-h-screen items-center justify-center">
    <div class="h-16 w-16 animate-spin rounded-full border-4 border-primary border-t-transparent" />
  </div>
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
