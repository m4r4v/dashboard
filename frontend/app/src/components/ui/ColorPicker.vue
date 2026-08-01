<template>
  <div>
    <label v-if="label" class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">
      {{ label }}
    </label>
    <div class="flex items-center gap-2">
      <button
        class="relative h-9 w-9 shrink-0 overflow-hidden rounded-md border border-brand-border"
        :style="{ backgroundColor: modelValue }"
        type="button"
        @click="nativeInput?.click()"
      >
        <input
          ref="nativeInput"
          class="absolute inset-0 h-full w-full cursor-pointer opacity-0"
          type="color"
          :value="modelValue"
          @input="onNativeInput"
        >
      </button>
      <input
        class="w-28 rounded-md border border-brand-border bg-transparent px-2 py-1.5 font-mono text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary"
        maxlength="7"
        spellcheck="false"
        :value="modelValue"
        @change="onTextChange"
      >
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  export interface ColorPickerProps {
    modelValue: string
    label?: string
  }

  defineProps<ColorPickerProps>()
  const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

  const nativeInput = ref<HTMLInputElement | null>(null)
  const HEX_RE = /^#[0-9a-fA-F]{6}$/

  function onNativeInput (event: Event) {
    emit('update:modelValue', (event.target as HTMLInputElement).value)
  }

  function onTextChange (event: Event) {
    const value = (event.target as HTMLInputElement).value.trim()
    if (HEX_RE.test(value)) {
      emit('update:modelValue', value)
    }
  }
</script>
