<template>
  <v-card class="rounded-lg overflow-hidden d-flex flex-column" color="primary" height="420" variant="outlined">
    <v-card-title class="d-flex align-center pa-3 bg-grey-lighten-4 border-b flex-none">
      <v-icon class="mr-2" color="primary" icon="mdi-xml" size="small" />
      <span class="text-caption font-weight-bold text-uppercase">Node Events</span>
      <v-spacer />
      <v-chip
        v-if="nodeStore.nodeInfo"
        color="accent"
        label
        size="x-small"
        variant="flat"
      >
        HOST: {{ nodeStore.nodeInfo.node_id }}
      </v-chip>
    </v-card-title>

    <div class="px-4 py-2 bg-grey-lighten-5 d-flex gap-4 border-b flex-none">
      <div class="text-caption">
        <span class="text-medium-emphasis text-primary">UPTIME:</span>
        <span class="font-weight-bold ml-1 text-info">{{ formatUptime(nodeStore.nodeInfo?.uptime_seconds || 0) }}</span>
      </div>
      <v-divider class="mx-2" vertical />
      <div class="text-caption">
        <span class="text-medium-emphasis text-primary">MEM:</span>
        <span class="font-weight-bold ml-1 text-info">{{ nodeStore.nodeInfo?.memory_usage_mb.toFixed(1) }}MB</span>
      </div>
    </div>

    <v-card-text class="pa-0 flex-grow-1 bg-grey-darken-4 overflow-hidden d-flex flex-column" style="min-height: 0;">
      <pre ref="logContainer" class="log-viewer pa-3">
        <template v-if="nodeStore.logs.length > 0">
          <div v-for="(log, i) in nodeStore.logs" :key="i" class="log-row">
            <span class="log-time">[{{ log.timestamp.split(' ')[1] }}]</span>
            <span class="log-level" :class="getLevelClass(log.level)">{{ log.level }}</span>
            <span class="log-msg">{{ log.message }}</span>
          </div>
        </template>
        <template v-else>
          <div class="pa-4 text-grey-darken-1 text-caption italic">No hay eventos registrados en el búfer.</div>
        </template>
      </pre>
    </v-card-text>

    <v-divider />
    <v-card-actions class="pa-2 bg-grey-lighten-4 flex-none">
      <v-btn
        color="primary"
        :loading="nodeStore.isActionPending"
        prepend-icon="mdi-sync"
        size="x-small"
        variant="flat"
        @click="runAction('RELOAD_RESOURCES')"
      >
        Sync Server State
      </v-btn>

      <v-spacer />

      <v-tooltip location="top" text="Forzar actualización de logs">
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            :class="{ 'refreshing-anim': nodeStore.isLoading }"
            icon="mdi-refresh"
            size="x-small"
            variant="text"
            @click="refreshAll"
          />
        </template>
      </v-tooltip>
    </v-card-actions>
  </v-card>
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
    if (level === 'ERROR') return 'text-red-lighten-2'
    if (level === 'WARNING') return 'text-orange-lighten-2'
    return 'text-blue-lighten-3'
  }

  // Scroll automático al final cuando llegan nuevos logs
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
  flex-grow: 1;
  overflow-y: auto;
  font-family: 'Fira Code', monospace;
  font-size: 11px;
  line-height: 1.3;
  color: #eceff1;
  background-color: #121212;
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

.flex-none { flex: none; }
.gap-4 { gap: 16px; }

.rotate-animation {
  animation: rotate 1s linear infinite;
}
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
