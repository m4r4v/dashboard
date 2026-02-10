import { setupLayouts } from 'virtual:generated-layouts'
/**
 * router/index.js
 * Configuración Corregida (v1.2.0)
 */
import { createRouter, createWebHistory } from 'vue-router/auto'
import { routes } from 'vue-router/auto-routes' // <--- 1. IMPORTAMOS LAS RUTAS MANUALMENTE

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // 2. LA CORRECCIÓN: Pasamos las rutas envueltas en layouts directamente
  routes: setupLayouts(routes),
})

// ========================================================
// 🛡️ ROUTER GUARD (El Portero)
// ========================================================
router.beforeEach((to, from, next) => {
    // Leemos el token directo del disco
    const token = localStorage.getItem('token')

    // Rutas públicas (Lista blanca)
    const publicPages = ['/login']
    const authRequired = !publicPages.includes(to.path)

    // Lógica de Semáforo
    if (authRequired && !token) {
        // 🛑 Intento de acceso a zona privada sin token -> Login
        next('/login')
    } else if (to.path === '/login' && token) {
        // 🔄 Usuario logueado intentando ir a login -> Dashboard
        next('/')
    } else {
        // ✅ Acceso permitido
        next()
    }
})

export default router
