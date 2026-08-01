<template>
  <router-view />

  <div
    v-if="uiStore.snackbar.show"
    class="fixed right-4 top-4 z-50 flex items-center gap-3 rounded-md px-4 py-3 text-sm text-white shadow-lg"
    :class="snackbarColorClass"
  >
    {{ uiStore.snackbar.text }}
    <button class="text-white/80 hover:text-white" @click="uiStore.snackbar.show = false">
      <IconMdiClose class="h-4 w-4" />
    </button>
  </div>
</template>

<script setup lang="ts">
  import { computed } from 'vue'
  import { useUiStore } from '@/stores/uiStore'

  const uiStore = useUiStore()

  const snackbarColorClass = computed(() => ({
    success: 'bg-success',
    error: 'bg-error',
    warning: 'bg-warning',
    info: 'bg-info',
  }[uiStore.snackbar.color]))
</script>
