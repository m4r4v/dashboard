<template>
  <div>
    <div
      class="flex min-h-[140px] cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed border-brand-border p-6 text-center transition hover:border-primary"
      :class="dragOver ? 'border-primary bg-primary/5' : ''"
      @click="fileInput?.click()"
      @dragleave="dragOver = false"
      @dragover.prevent="dragOver = true"
      @drop.prevent="onDrop"
    >
      <img v-if="modelValue" alt="Logo" class="max-h-24 max-w-full object-contain" :src="modelValue">
      <template v-else>
        <IconMdiImageOutline class="h-8 w-8 text-gray-400" />
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Arrastra tu logo aquí o hacé clic para seleccionar<br>
          PNG, JPG o SVG · máx. {{ maxSizeMb }}MB
        </p>
      </template>
      <input
        ref="fileInput"
        accept="image/png,image/jpeg,image/svg+xml"
        class="hidden"
        type="file"
        @change="onFileChange"
      >
    </div>

    <div v-if="modelValue" class="mt-2 flex justify-end">
      <button class="text-xs font-medium text-error hover:underline" type="button" @click="clear">
        Quitar logo
      </button>
    </div>

    <p v-if="errorMsg" class="mt-2 text-xs text-error">{{ errorMsg }}</p>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'

  export interface LogoUploaderProps {
    modelValue: string | null
    maxSizeMb?: number
  }

  const props = withDefaults(defineProps<LogoUploaderProps>(), { maxSizeMb: 2 })
  const emit = defineEmits<{
    'update:modelValue': [value: string | null]
    'file-selected': [file: File]
  }>()

  const fileInput = ref<HTMLInputElement | null>(null)
  const dragOver = ref(false)
  const errorMsg = ref<string | null>(null)

  const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'image/svg+xml']

  function handleFile (file: File) {
    errorMsg.value = null

    if (!ALLOWED_TYPES.includes(file.type)) {
      errorMsg.value = 'Formato no soportado. Usa PNG, JPG o SVG.'
      return
    }
    if (file.size > props.maxSizeMb * 1024 * 1024) {
      errorMsg.value = `El archivo supera ${props.maxSizeMb}MB.`
      return
    }

    const reader = new FileReader()
    reader.onload = () => {
      emit('update:modelValue', reader.result as string)
    }
    reader.readAsDataURL(file)
    emit('file-selected', file)
  }

  function onFileChange (event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0]
    if (file) handleFile(file)
  }

  function onDrop (event: DragEvent) {
    dragOver.value = false
    const file = event.dataTransfer?.files?.[0]
    if (file) handleFile(file)
  }

  function clear () {
    emit('update:modelValue', null)
    if (fileInput.value) fileInput.value.value = ''
  }
</script>
