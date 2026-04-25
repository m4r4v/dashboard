<template>
  <v-card class="rounded-md overflow-hidden" color="primary" variant="outlined">

    <v-card-title class="px-4 pt-4 text-overline text-medium-emphasis text-info">
      API Response Data
    </v-card-title>

    <v-card-text>
      <div class="debug-display-wrapper">
        <pre
          class="pa-4 rounded shadow-inner bg-grey-darken-4 monospace-text"
          :class="systemStore.isOnline ? 'text-green-accent-3' : 'text-red-accent-3'"
        >{{ systemStore.status || 'Esperando sincronización...' }}</pre>
      </div>
    </v-card-text>

    <v-card-actions class="px-4 pb-4">
      <v-btn
        color="primary"
        :loading="systemStore.isLoading"
        prepend-icon="mdi-refresh"
        variant="flat"
        @click="systemStore.fetchStatus()"
      >
        Sincronizar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
  import { useSystemStore } from '@/stores/systemStore'
  const systemStore = useSystemStore()
</script>

<style scoped>
.debug-display-wrapper {
  min-height: 120px;
  display: flex;
  flex-direction: column;
}

pre {
  margin: 0;
  min-height: 120px;
  font-size: 0.875rem;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  transition: color 0.4s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.monospace-text {
  font-family: 'Fira Code', 'Courier New', monospace !important;
}

.shadow-inner {
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
}
</style>
