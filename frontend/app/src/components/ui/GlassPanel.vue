<template>
  <div class="relative overflow-hidden rounded-lg border" :class="borderClass">
    <!-- Esquinas HUD -->
    <span class="pointer-events-none absolute left-0 top-0 h-3 w-3 border-l-2 border-t-2" :class="cornerClass" />
    <span class="pointer-events-none absolute right-0 top-0 h-3 w-3 border-r-2 border-t-2" :class="cornerClass" />
    <span class="pointer-events-none absolute bottom-0 left-0 h-3 w-3 border-b-2 border-l-2" :class="cornerClass" />
    <span class="pointer-events-none absolute bottom-0 right-0 h-3 w-3 border-b-2 border-r-2" :class="cornerClass" />

    <header v-if="title || $slots.actions" class="flex items-center justify-between border-b px-4 py-3" :class="borderClass">
      <h3 v-if="title" class="font-mono text-xs font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
        {{ title }}
      </h3>
      <div v-if="$slots.actions" class="flex items-center gap-2">
        <slot name="actions" />
      </div>
    </header>

    <div class="bg-surface/70 backdrop-blur-sm">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed } from 'vue'

  export interface GlassPanelProps {
    title?: string
    accent?: 'neutral' | 'success' | 'error' | 'warning' | 'info'
  }

  const props = withDefaults(defineProps<GlassPanelProps>(), {
    title: undefined,
    accent: 'neutral',
  })

  const accentColorMap: Record<NonNullable<GlassPanelProps['accent']>, string> = {
    neutral: 'border-brand-border',
    success: 'border-success/50',
    error: 'border-error/50',
    warning: 'border-warning/50',
    info: 'border-info/50',
  }

  const borderClass = computed(() => accentColorMap[props.accent ?? 'neutral'])

  // "neutral" usa secondary, no primary: primary queda reservado para
  // botones/acciones; secondary es el acento estructural/decorativo de los
  // paneles (así secondary tiene un lugar visible real, no solo un color
  // que se puede elegir pero nunca se ve en ningún lado).
  const cornerColorMap: Record<NonNullable<GlassPanelProps['accent']>, string> = {
    neutral: 'border-secondary',
    success: 'border-success',
    error: 'border-error',
    warning: 'border-warning',
    info: 'border-info',
  }

  const cornerClass = computed(() => cornerColorMap[props.accent ?? 'neutral'])
</script>
