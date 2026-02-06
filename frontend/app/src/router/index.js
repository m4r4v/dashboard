/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

import { setupLayouts } from 'virtual:generated-layouts'
// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: setupLayouts(routes),
})

// --- SECURITY GUARD (Middleware) ---
router.beforeEach((to, from, next) => {
  // Leemos el token directamente del almacenamiento (Fuente de Verdad)
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  // Lógica de Semáforo
  if (to.path === '/login' && isAuthenticated) {
    // REGLA 1 (Tu solicitud): Si ya estoy logueado, prohibido ver el Login.
    // Redirigir al Dashboard.
    next('/')
  } else if (to.path !== '/login' && !isAuthenticated) {
    // REGLA 2 (Seguridad): Si soy anónimo, prohibido ver el Dashboard.
    // Redirigir al Login.
    next('/login')
  } else {
    // Tráfico Legítimo
    next()
  }
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (localStorage.getItem('vuetify:dynamic-reload')) {
      console.error('Dynamic import error, reloading page did not fix it', err)
    } else {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
