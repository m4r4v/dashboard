<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" md="4" sm="8">

        <v-card class="elevation-12" rounded="lg">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Acceso al Sistema</v-toolbar-title>
          </v-toolbar>

          <v-card-text class="pa-6">
            <v-form v-model="valid" @submit.prevent="handleLogin">

              <v-text-field
                v-model="email"
                color="primary"
                label="Correo Electrónico"
                prepend-inner-icon="mdi-email"
                required
                :rules="emailRules"
                type="email"
                variant="outlined"
              />

              <v-text-field
                v-model="password"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                class="mt-2"
                color="primary"
                label="Contraseña"
                prepend-inner-icon="mdi-lock"
                required
                :rules="passwordRules"
                :type="showPassword ? 'text' : 'password'"
                variant="outlined"
                @click:append-inner="showPassword = !showPassword"
              />

              <v-alert
                v-if="authStore.error"
                class="mt-4 mb-4"
                closable
                density="compact"
                type="error"
                variant="tonal"
              >
                {{ authStore.error }}
              </v-alert>

            </v-form>
          </v-card-text>

          <v-card-actions class="pa-6 pt-0">
            <v-spacer />
            <v-btn
              block
              color="primary"
              :disabled="!valid"
              :loading="authStore.loading"
              size="large"
              variant="elevated"
              @click="handleLogin"
            >
              Iniciar Sesión
            </v-btn>
          </v-card-actions>
        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'

  // --- Composable Injection ---
  const router = useRouter()
  const authStore = useAuthStore()

  // --- Local State ---
  const valid = ref(false)
  const email = ref('')
  const password = ref('')
  const showPassword = ref(false)

  // --- Validation Rules ---
  const emailRules = [
    (v: string) => !!v || 'El correo es requerido',
    (v: string) => /.+@.+\..+/.test(v) || 'El correo debe ser válido',
  ]

  const passwordRules = [
    (v: string) => !!v || 'La contraseña es requerida',
  ]

  // --- Handlers ---
  async function handleLogin() {
    // 1. Ejecutar acción del Store
    const success = await authStore.login(email.value, password.value)

    // 2. Si el login es correcto, redirigir al Dashboard
    if (success) {
      router.push('/')
    }
  }
</script>

<route lang="yaml">
meta:
  layout: default
</route>
