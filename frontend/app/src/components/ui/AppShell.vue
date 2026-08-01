<template>
  <div class="hud-grid-bg fixed inset-0 -z-10" />
  <div class="min-h-screen">
    <header class="sticky top-0 z-40 flex items-center border-b px-4 py-3 backdrop-blur-sm" :class="borderClass">
      <button
        v-if="navItems.length"
        class="mr-3 text-gray-500 hover:text-primary dark:text-gray-400"
        @click="drawer = !drawer"
      >
        <IconMdiMenu class="h-6 w-6" />
      </button>

      <h1 class="font-mono text-xs font-bold uppercase tracking-widest text-gray-700 dark:text-gray-200">
        {{ title }}
      </h1>

      <div class="flex-1" />

      <div class="flex items-center gap-2">
        <slot name="actions" />
      </div>
    </header>

    <template v-if="navItems.length">
      <div v-if="drawer" class="fixed inset-0 z-30 bg-black/40" @click="drawer = false" />
      <aside
        class="fixed inset-y-0 left-0 z-40 w-64 -translate-x-full border-r bg-surface p-4 transition-transform"
        :class="[borderClass, drawer ? 'translate-x-0' : '']"
      >
        <router-link
          v-for="item in navItems"
          :key="item.to"
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-primary hover:bg-primary/10"
          :to="item.to"
          @click="drawer = false"
        >
          <component :is="item.icon" v-if="item.icon" class="h-5 w-5" />
          {{ item.label }}
        </router-link>
      </aside>
    </template>

    <main>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  export interface AppShellNavItem {
    label: string
    to: string
    icon?: unknown
  }

  export interface AppShellProps {
    title: string
    navItems?: AppShellNavItem[]
  }

  withDefaults(defineProps<AppShellProps>(), {
    navItems: () => [],
  })

  const drawer = ref(false)
  const borderClass = 'border-brand-border'
</script>
