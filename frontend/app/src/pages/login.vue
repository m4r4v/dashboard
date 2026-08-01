<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100 px-4 dark:bg-gray-900">
    <div class="w-full max-w-md">
      <div class="overflow-hidden rounded-lg shadow-xl">
        <div class="flex items-center bg-primary px-6 py-4">
          <h1 class="text-sm font-bold uppercase tracking-wide text-white">
            Control Room
          </h1>
          <span class="ml-2 text-xs text-white/70">v1.3.0</span>
        </div>

        <div class="bg-white p-8 dark:bg-gray-800">
          <h2 class="mb-1 text-lg font-bold text-gray-900 dark:text-gray-100">Login</h2>
          <p class="mb-6 text-sm text-gray-500 dark:text-gray-400">
            Identifíquese para gestionar el nodo stateless.
          </p>

          <div
            v-if="errorMsg"
            class="mb-4 rounded-md bg-error/10 px-4 py-3 text-sm text-error"
          >
            {{ errorMsg }}
          </div>

          <form novalidate @submit.prevent="handleLogin">
            <div class="mb-4">
              <label class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">
                Correo Electrónico
              </label>
              <div class="relative">
                <IconMdiEmailOutline class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
                <input
                  v-model="email"
                  autocomplete="email"
                  class="w-full rounded-md border border-gray-300 py-2 pl-10 pr-3 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
                  type="email"
                >
              </div>
              <p v-if="emailError" class="mt-1 text-xs text-error">{{ emailError }}</p>
            </div>

            <div class="mb-4">
              <label class="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-300">
                Contraseña
              </label>
              <div class="relative">
                <IconMdiLockOutline class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
                <input
                  v-model="password"
                  autocomplete="current-password"
                  class="w-full rounded-md border border-gray-300 py-2 pl-10 pr-10 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
                  :type="showPass ? 'text' : 'password'"
                >
                <button
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  type="button"
                  @click="showPass = !showPass"
                >
                  <IconMdiEye v-if="showPass" class="h-5 w-5" />
                  <IconMdiEyeOff v-else class="h-5 w-5" />
                </button>
              </div>
              <p v-if="passwordError" class="mt-1 text-xs text-error">{{ passwordError }}</p>
            </div>

            <!-- Honeypot: fuera de pantalla, nunca display:none (ver security-review-m4r4v) -->
            <input
              v-model="honeypot"
              autocomplete="off"
              style="position: absolute; left: -9999px;"
              tabindex="-1"
            >

            <button
              class="mt-6 flex w-full items-center justify-center rounded-md bg-primary px-4 py-3 text-sm font-bold text-white transition hover:brightness-110 disabled:opacity-60"
              :disabled="authStore.isLoading"
              type="submit"
            >
              <span v-if="authStore.isLoading">Entrando...</span>
              <span v-else>Entrar al Sistema</span>
            </button>
          </form>
        </div>
      </div>

      <p class="mt-6 text-center text-xs text-gray-400 dark:text-gray-500">
        &copy; {{ new Date().getFullYear() }} Dashboard System • Stateless Mode
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'

  const router = useRouter()
  const authStore = useAuthStore()

  const showPass = ref(false)
  const errorMsg = ref(null)
  const email = ref('')
  const password = ref('')
  const honeypot = ref('')
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

<route lang="yaml">
meta:
  layout: blank
</route>
