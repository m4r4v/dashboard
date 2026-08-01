<template>
  <div class="hud-grid-bg fixed inset-0 -z-10" />
  <div class="flex min-h-screen items-center justify-center px-4">
    <div class="w-full max-w-md">
      <div class="overflow-hidden rounded-lg border border-brand-border shadow-xl">
        <div class="border-b border-brand-border bg-primary/10 px-6 py-4">
          <img v-if="logoUrl" alt="" class="mb-2 h-8 max-w-[160px] object-contain" :src="logoUrl">
          <h1 class="font-mono text-sm font-bold uppercase tracking-widest text-primary">
            {{ title }}
          </h1>
          <p v-if="subtitle" class="mt-1 text-xs text-gray-500 dark:text-gray-400">{{ subtitle }}</p>
        </div>

        <div class="bg-surface/80 p-8 backdrop-blur-sm">
          <slot />
        </div>
      </div>

      <p v-if="footer" class="mt-6 text-center text-xs text-gray-400 dark:text-gray-500">
        {{ footer }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
  export interface AuthCardProps {
    title: string
    logoUrl?: string | null
    subtitle?: string
    footer?: string
  }

  defineProps<AuthCardProps>()
</script>
