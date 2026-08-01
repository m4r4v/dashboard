<template>
  <GlassPanel :accent="systemStore.isOnline ? 'success' : 'error'" title="API Response Data">
    <template #actions>
      <button
        class="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-white hover:brightness-110 disabled:opacity-60"
        :disabled="systemStore.isLoading"
        @click="systemStore.fetchStatus()"
      >
        <IconMdiRefresh class="h-3.5 w-3.5" :class="systemStore.isLoading ? 'animate-spin' : ''" />
        Sincronizar
      </button>
    </template>

    <div class="p-4">
      <pre
        class="min-h-[120px] overflow-y-auto whitespace-pre-wrap break-words rounded bg-surface-2 p-4 font-mono text-sm"
        :class="systemStore.isOnline ? 'text-success' : 'text-error'"
      >{{ systemStore.status || 'Esperando sincronización...' }}</pre>
    </div>
  </GlassPanel>
</template>

<script setup lang="ts">
  import GlassPanel from '@/components/ui/GlassPanel.vue'
  import { useSystemStore } from '@/stores/systemStore'

  const systemStore = useSystemStore()
</script>
