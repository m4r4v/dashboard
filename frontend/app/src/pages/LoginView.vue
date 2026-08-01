<template>
  <AuthCard :logo-url="themeConfig.logoDataUrl" footer="© Dashboard System · Stateless Mode" subtitle="Identifíquese para continuar." title="Control Room">
    <div v-if="errorMsg" class="mb-4 rounded-md bg-error/10 px-4 py-3 text-sm text-error">
      {{ errorMsg }}
    </div>

    <form novalidate @submit.prevent="handleLogin">
      <div class="mb-4">
        <label class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">Correo Electrónico</label>
        <input
          v-model="email"
          autocomplete="email"
          class="w-full rounded-md border border-brand-border bg-transparent px-3 py-2 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary"
          type="email"
        >
        <p v-if="emailError" class="mt-1 text-xs text-error">{{ emailError }}</p>
      </div>

      <div class="mb-4">
        <label class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">Contraseña</label>
        <input
          v-model="password"
          autocomplete="current-password"
          class="w-full rounded-md border border-brand-border bg-transparent px-3 py-2 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary"
          type="password"
        >
        <p v-if="passwordError" class="mt-1 text-xs text-error">{{ passwordError }}</p>
      </div>

      <!-- Honeypot: fuera de pantalla, nunca display:none. -->
      <input
        v-model="honeypot"
        autocomplete="off"
        style="position: absolute; left: -9999px;"
        tabindex="-1"
      >

      <button
        class="mt-2 flex w-full items-center justify-center rounded-md bg-primary px-4 py-3 text-sm font-bold text-primary-contrast transition hover:brightness-110 disabled:opacity-60"
        :disabled="authStore.isLoading"
        type="submit"
      >
        {{ authStore.isLoading ? 'Entrando...' : 'Entrar al Sistema' }}
      </button>
    </form>
  </AuthCard>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import AuthCard from '@/components/ui/AuthCard.vue'
  import { useAuthStore } from '@/stores/authStore'
  import { useThemeConfigStore } from '@/stores/themeConfigStore'

  const router = useRouter()
  const authStore = useAuthStore()
  const themeConfig = useThemeConfigStore()

  const email = ref('')
  const password = ref('')
  const honeypot = ref('')
  const errorMsg = ref<string | null>(null)
  const emailError = ref<string | null>(null)
  const passwordError = ref<string | null>(null)

  function validate (): boolean {
    emailError.value = !email.value
      ? 'Requerido'
      : !/.+@.+\..+/.test(email.value)
        ? 'Formato inválido'
        : null
    passwordError.value = !password.value ? 'Requerido' : null
    return !emailError.value && !passwordError.value
  }

  async function handleLogin () {
    if (honeypot.value || !validate()) return
    errorMsg.value = null

    try {
      await authStore.login(email.value, password.value, honeypot.value)
      router.push('/')
    } catch (error: any) {
      errorMsg.value = error.response?.status === 401 ? 'Acceso denegado.' : 'Servidor no disponible.'
    }
  }
</script>
