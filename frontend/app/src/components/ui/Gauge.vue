<template>
  <div class="flex flex-col items-center gap-1">
    <svg class="h-24 w-24 -rotate-90" viewBox="0 0 100 100">
      <circle
        class="text-brand-border"
        cx="50" cy="50" fill="none" r="40"
        stroke="currentColor" stroke-width="8"
      />
      <circle
        class="text-primary transition-[stroke-dashoffset] duration-500 ease-out"
        cx="50" cy="50" fill="none" r="40"
        stroke="currentColor"
        stroke-dasharray="251.2"
        :stroke-dashoffset="dashOffset"
        stroke-linecap="round"
        stroke-width="8"
      />
    </svg>
    <div class="-mt-16 flex flex-col items-center">
      <span class="font-mono text-lg font-bold text-gray-900 dark:text-gray-100">
        {{ displayValue }}<span class="text-xs font-normal text-gray-500 dark:text-gray-400">{{ unit }}</span>
      </span>
    </div>
    <span class="mt-14 text-xs font-bold uppercase text-gray-500 dark:text-gray-400">{{ label }}</span>
  </div>
</template>

<script setup lang="ts">
  import { computed } from 'vue'

  export interface GaugeProps {
    value: number
    max: number
    label: string
    unit?: string
  }

  const props = withDefaults(defineProps<GaugeProps>(), { unit: '' })

  const CIRCUMFERENCE = 251.2 // 2 * PI * 40

  const percentage = computed(() => {
    if (!props.max) return 0
    return Math.min(100, Math.max(0, (props.value / props.max) * 100))
  })

  const dashOffset = computed(() => CIRCUMFERENCE - (percentage.value / 100) * CIRCUMFERENCE)

  const displayValue = computed(() => Math.round(props.value * 10) / 10)
</script>
