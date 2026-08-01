<template>
  <div class="overflow-hidden rounded-md border border-primary">
    <div class="px-4 pt-4 text-xs font-medium uppercase tracking-wide text-info">
      API Response Data
    </div>

    <div class="p-4">
      <pre
        class="min-h-[120px] overflow-y-auto whitespace-pre-wrap break-words rounded bg-gray-900 p-4 font-mono text-sm shadow-inner transition-colors"
        :class="systemStore.isOnline ? 'text-green-400' : 'text-red-400'"
      >{{ systemStore.status || 'Esperando sincronización...' }}</pre>
    </div>

    <div class="px-4 pb-4">
      <button
        class="flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:brightness-110 disabled:opacity-60"
        :disabled="systemStore.isLoading"
        @click="systemStore.fetchStatus()"
      >
        <IconMdiRefresh class="h-4 w-4" :class="systemStore.isLoading ? 'animate-spin' : ''" />
        Sincronizar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useSystemStore } from '@/stores/systemStore'
  const systemStore = useSystemStore()
</script>
