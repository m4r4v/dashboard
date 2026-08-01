<template>
  <div class="inline-flex items-center gap-2">
    <span class="relative flex h-2.5 w-2.5">
      <span
        v-if="status === 'online'"
        class="absolute inline-flex h-full w-full animate-ping rounded-full opacity-60"
        :class="dotColorClass"
      />
      <span class="relative inline-flex h-2.5 w-2.5 rounded-full" :class="dotColorClass" />
    </span>
    <span v-if="label" class="text-xs font-bold uppercase text-gray-500 dark:text-gray-400">
      {{ label }}
    </span>
  </div>
</template>

<script setup lang="ts">
  import { computed } from 'vue'

  export interface StatusDotProps {
    status: 'online' | 'degraded' | 'offline'
    label?: string
  }

  const props = defineProps<StatusDotProps>()

  const colorMap: Record<StatusDotProps['status'], string> = {
    online: 'bg-success',
    degraded: 'bg-warning',
    offline: 'bg-error',
  }

  const dotColorClass = computed(() => colorMap[props.status])
</script>
