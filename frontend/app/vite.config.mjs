import { fileURLToPath, URL } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import Vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/vite'

// Setup limpio y mínimo: sin auto-routing, sin auto-layouts, sin auto-import.
// Rutas declaradas a mano en src/router/index.ts.
export default defineConfig({
  plugins: [
    Vue(),
    tailwindcss(),
    Components({
      resolvers: [IconsResolver({ prefix: 'Icon' })],
      dts: false,
    }),
    Icons({ compiler: 'vue3', autoInstall: true }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: true,
    port: 3000,
  },
})
