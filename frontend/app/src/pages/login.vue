<template>
  <v-container class="fill-height bg-grey-lighten-4" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" lg="4" md="6" sm="8">

        <v-card class="elevation-12 rounded-lg overflow-hidden" min-height="440">
          <v-toolbar color="primary" flat>
            <v-toolbar-title class="text-uppercase font-weight-bold">
              Control Room <span class="text-caption ml-2">v1.3.0</span>
            </v-toolbar-title>
          </v-toolbar>

          <v-card-text class="pa-8">
            <div class="text-h6 mb-2 font-weight-bold">Login</div>
            <div class="text-body-2 mb-6 text-medium-emphasis">
              Identifíquese para gestionar el nodo stateless.
            </div>

            <div>
              <v-fade-transition>
                <v-alert
                  v-if="errorMsg"
                  class="mb-4"
                  density="compact"
                  type="error"
                  variant="tonal"
                >
                  {{ errorMsg }}
                </v-alert>
              </v-fade-transition>
            </div>

            <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="email"
                class="mb-4"
                color="primary"
                hide-details="auto"
                label="Correo Electrónico"
                prepend-inner-icon="mdi-email-outline"
                required
                :rules="emailRules"
                variant="outlined"
              />

              <v-text-field
                v-model="password"
                :append-inner-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
                class="mb-4"
                color="primary"
                hide-details="auto"
                label="Contraseña"
                prepend-inner-icon="mdi-lock-outline"
                required
                :rules="requiredRules"
                :type="showPass ? 'text' : 'password'"
                variant="outlined"
                @click:append-inner="showPass = !showPass"
              />

              <input v-model="honeypot" class="d-none" tabindex="-1">

              <v-btn
                block
                class="mt-6 font-weight-bold"
                color="primary"
                :disabled="!valid"
                :loading="authStore.isLoading"
                size="large"
                type="submit"
                variant="flat"
              >
                Entrar al Sistema
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <div class="text-center mt-6 text-caption text-disabled">
          &copy; {{ new Date().getFullYear() }} Dashboard System • Stateless Mode
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'

  const router = useRouter()
  const authStore = useAuthStore()

  const valid = ref(false)
  const showPass = ref(false)
  const errorMsg = ref(null)
  const email = ref('')
  const password = ref('')
  const honeypot = ref('')

  const requiredRules = [v => !!v || 'Requerido']
  const emailRules = [
    v => !!v || 'Requerido',
    v => /.+@.+\..+/.test(v) || 'Formato inválido'
  ]

  async function handleLogin () {
    if (honeypot.value || !valid.value) return
    errorMsg.value = null

    try {
      await authStore.login(email.value, password.value)
      router.push('/')
    } catch (error: any) {
      errorMsg.value = error.response?.status === 401 ? 'Acceso denegado.' : 'Servidor no disponible.';
    }
  }
</script>

<route lang="yaml">
meta:
  layout: blank
</route>
