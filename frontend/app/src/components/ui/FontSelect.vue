<template>
  <div>
    <label v-if="label" class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">
      {{ label }}
    </label>
    <div class="space-y-1.5">
      <button
        v-for="option in options"
        :key="option.key"
        class="flex w-full items-center justify-between rounded-md border px-3 py-2 text-left transition"
        :class="option.key === modelValue
          ? 'border-primary bg-primary/5'
          : 'border-brand-border hover:border-primary/50'"
        type="button"
        @click="emit('update:modelValue', option.key)"
      >
        <span :style="{ fontFamily: option.family }" class="text-sm">{{ option.label }}</span>
        <IconMdiCheck v-if="option.key === modelValue" class="h-4 w-4 text-primary" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
  export interface FontSelectOption {
    key: string
    label: string
    family: string
  }

  export interface FontSelectProps {
    modelValue: string
    options: FontSelectOption[]
    label?: string
  }

  defineProps<FontSelectProps>()
  const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
