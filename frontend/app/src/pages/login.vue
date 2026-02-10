<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" lg="4" md="6" sm="8">

        <v-card class="elevation-12 rounded-lg">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title class="text-uppercase font-weight-bold">
              Control Room
            </v-toolbar-title>
          </v-toolbar>

          <v-card-text class="pa-6">
            <div class="text-subtitle-1 mb-4 text-medium-emphasis">
              Identifíquese para acceder al sistema raíz.
            </div>

            <v-alert
              v-if="errorMsg"
              class="mb-4"
              closable
              type="error"
              variant="tonal"
              @click:close="errorMsg = null"
            >
              {{ errorMsg }}
            </v-alert>

            <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="email"
                autofocus
                label="Correo Electrónico"
                prepend-inner-icon="mdi-email"
                required
                :rules="emailRules"
                variant="outlined"
              />

              <v-text-field
                v-model="password"
                :append-inner-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
                label="Contraseña"
                prepend-inner-icon="mdi-lock"
                required
                :rules="requiredRules"
                :type="showPass ? 'text' : 'password'"
                variant="outlined"
                @click:append-inner="showPass = !showPass"
              />

              <v-text-field
                v-model="honeypot"
                autocomplete="off"
                class="d-none"
                name="phone"
                tabindex="-1"
              />

              <v-btn
                block
                class="mt-4 font-weight-bold"
                color="primary"
                :disabled="!valid"
                :loading="loading"
                size="large"
                type="submit"
              >
                Iniciar Sesión
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <div class="text-center mt-4 text-caption text-disabled">
          &copy; {{ new Date().getFullYear() }} Dashboard System v1.2.0
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

  // --- Estado Local ---
  const valid = ref(false)
  const loading = ref(false)
  const showPass = ref(false)
  const errorMsg = ref(null)

  // Campos del formulario
  const email = ref('')
  const password = ref('')
  const honeypot = ref('') // Campo trampa

  // --- Reglas de Validación ---
  const requiredRules = [v => !!v || 'Este campo es requerido']
  const emailRules = [
    v => !!v || 'El correo es requerido',
    v => /.+@.+\..+/.test(v) || 'El formato del correo no es válido'
  ]

  // --- Lógica de Negocio ---
  async function handleLogin () {
    errorMsg.value = null

    // 1. Verificación Honeypot (Cliente)
    if (honeypot.value) {
      console.warn('Bot detectado: Campo honeypot completado.')
      loading.value = true
      setTimeout(() => {
        loading.value = false
        errorMsg.value = 'Error de conexión.'
      }, 1000)
      return
    }

    // 2. Validación de Formulario
    if (!valid.value) return

    loading.value = true

    try {
      // 3. Llamada al Store
      await authStore.login(email.value, password.value)

      // 4. Redirección Éxitosa
      router.push('/')

    } catch (error) {
      // Manejo de errores HTTP
      if (error.response?.status === 401) {
        errorMsg.value = 'Credenciales incorrectas. Verifique y reintente.'
      } else if (error.code === 'ERR_NETWORK') {
        errorMsg.value = 'No hay conexión con el servidor.'
      } else {
        errorMsg.value = 'Error inesperado del sistema.'
      }
    } finally {
      loading.value = false
    }
  }
</script>

<route lang="yaml">
meta:
  layout: blank
</route>
