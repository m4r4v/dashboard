<template>
  <div class="flex h-[420px] flex-col overflow-hidden rounded-lg border border-primary">
    <div class="flex flex-none items-center border-b border-gray-200 bg-gray-100 px-3 py-3 dark:border-gray-700 dark:bg-gray-800">
      <IconMdiXml class="mr-2 h-4 w-4 text-primary" />
      <span class="text-xs font-bold uppercase">Node Events</span>
      <div class="flex-1" />
      <span
        v-if="nodeStore.nodeInfo"
        class="rounded bg-accent px-2 py-0.5 text-xs font-bold text-white"
      >
        HOST: {{ nodeStore.nodeInfo.node_id }}
      </span>
    </div>

    <div class="flex flex-none items-center gap-4 border-b border-gray-200 bg-gray-50 px-4 py-2 dark:border-gray-700 dark:bg-gray-900">
      <div class="text-xs">
        <span class="text-primary/70">UPTIME:</span>
        <span class="ml-1 font-bold text-info">{{ formatUptime(nodeStore.nodeInfo?.uptime_seconds || 0) }}</span>
      </div>
      <div class="h-4 w-px bg-gray-300 dark:bg-gray-600" />
      <div class="text-xs">
        <span class="text-primary/70">MEM:</span>
        <span class="ml-1 font-bold text-info">{{ nodeStore.nodeInfo?.memory_usage_mb.toFixed(1) }}MB</span>
      </div>
    </div>

    <div class="min-h-0 flex-1 overflow-hidden bg-gray-950">
      <pre ref="logContainer" class="log-viewer p-3">
        <template v-if="nodeStore.logs.length > 0">
          <div v-for="(log, i) in nodeStore.logs" :key="i" class="log-row">
            <span class="log-time">[{{ log.timestamp.split(' ')[1] }}]</span>
            <span class="log-level" :class="getLevelClass(log.level)">{{ log.level }}</span>
            <span class="log-msg">{{ log.message }}</span>
          </div>
        </template>
        <template v-else>
          <div class="p-4 text-xs italic text-gray-500">No hay eventos registrados en el búfer.</div>
        </template>
      </pre>
    </div>

    <div class="flex flex-none items-center gap-2 border-t border-gray-200 bg-gray-100 px-2 py-2 dark:border-gray-700 dark:bg-gray-800">
      <button
        class="flex items-center gap-1 rounded bg-primary px-2 py-1 text-xs font-medium text-white hover:brightness-110 disabled:opacity-60"
        :disabled="nodeStore.isActionPending"
        @click="runAction('RELOAD_RESOURCES')"
      >
        <IconMdiSync class="h-3.5 w-3.5" :class="nodeStore.isActionPending ? 'animate-spin' : ''" />
        Sync Server State
      </button>

      <div class="flex-1" />

      <button
        class="rounded p-1 text-gray-500 hover:bg-gray-200 dark:text-gray-400 dark:hover:bg-gray-700"
        title="Forzar actualización de logs"
        @click="refreshAll"
      >
        <IconMdiRefresh class="h-4 w-4" :class="{ 'refreshing-anim': nodeStore.isLoading }" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted, onUnmounted, ref, watch } from 'vue'
  import { useNodeStore } from '@/stores/nodeStore'
  import { useUiStore } from '@/stores/uiStore'

  const nodeStore = useNodeStore()
  const uiStore = useUiStore()
  const logContainer = ref<HTMLElement | null>(null)
  let logInterval: any = null

  function refreshAll () {
    nodeStore.fetchNodeStatus()
    nodeStore.fetchLogs()
  }

  async function runAction (action: string) {
    try {
      const msg = await nodeStore.triggerAction(action)
      uiStore.notify.success(msg)
    } catch {
      uiStore.notify.error(`Fallo en acción: ${action}`)
    }
  }

  function formatUptime (seconds: number) {
    const h = Math.floor(seconds / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    return `${h}h ${m}m`
  }

  function getLevelClass (level: string) {
    if (level === 'ERROR') return 'text-red-400'
    if (level === 'WARNING') return 'text-orange-400'
    return 'text-blue-300'
  }

  watch(() => nodeStore.logs, () => {
    setTimeout(() => {
      if (logContainer.value) {
        logContainer.value.scrollTop = logContainer.value.scrollHeight
      }
    }, 50)
  }, { deep: true })

  onMounted(() => {
    refreshAll()
    logInterval = setInterval(nodeStore.fetchLogs, 5000)
  })

  onUnmounted(() => { if (logInterval) clearInterval(logInterval) })
</script>

<style scoped>
.refreshing-anim {
  animation: spin 0.8s ease-in-out;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.log-viewer {
  height: 100%;
  overflow-y: auto;
  font-family: 'Fira Code', monospace;
  font-size: 11px;
  line-height: 1.3;
  color: #eceff1;
}

.log-row {
  display: flex;
  gap: 12px;
  padding: 2px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.log-time {
  color: #546e7a;
  flex-shrink: 0;
}

.log-level {
  font-weight: bold;
  min-width: 50px;
  flex-shrink: 0;
}

.log-msg {
  word-break: break-all;
  white-space: pre-wrap;
}
</style>
