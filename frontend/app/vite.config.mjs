import { fileURLToPath, URL } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import Vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Fonts from 'unplugin-fonts/vite'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/vite'
import VueRouter from 'unplugin-vue-router/vite'
import { defineConfig } from 'vite'
import Layouts from 'vite-plugin-vue-layouts-next'

// Variante Tailwind (ver skill vuejs-tailwind-m4r4v) — reemplaza el plugin
// Vuetify por @tailwindcss/vite, e íconos mdi-* pasan de fuente completa
// (@mdi/font) a componentes SVG tree-shakeados vía unplugin-icons.
export default defineConfig({
  plugins: [
    VueRouter(),
    Layouts(),
    Vue(),
    tailwindcss(),
    Components({
      resolvers: [IconsResolver({ prefix: 'Icon' })],
    }),
    Icons({ compiler: 'vue3', autoInstall: true }),
    AutoImport({
      imports: [
        'vue',
        'vue-router',
        'pinia',
      ],
      dts: false, // Desactivado para evitar generación de archivos en runtime
    }),
    Fonts({
      google: {
        families: [{
          name: 'Roboto',
          styles: 'wght@100;300;400;500;700;900',
        }],
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    host: true,  // CRÍTICO: Escuchar en 0.0.0.0 para Docker
    port: 3000,  // CRÍTICO: Puerto alineado con docker-compose
    watch: {
      usePolling: true // Estabilidad en volúmenes Docker
    }
  }
})