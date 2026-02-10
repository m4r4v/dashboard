<template>
  <v-container class="pa-6" fluid>
    <v-row align="start" justify="start">
      <v-col cols="auto">
        <h1 class="text-h4 font-weight-bold text-primary">System Dashboard</h1>
        <div class="text-subtitle-1 text-medium-emphasis text-primary">Stateless Node Management</div>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <SystemStatusDisplay />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'
  import SystemStatusDisplay from '@/components/SystemStatusDisplay.vue'
  import { useSystemStore } from '@/stores/systemStore'

  const systemStore = useSystemStore()

  onMounted(() => {
    systemStore.fetchStatus()
  })
</script>
