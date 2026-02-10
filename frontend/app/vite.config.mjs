import { fileURLToPath, URL } from 'node:url'
import Vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Fonts from 'unplugin-fonts/vite'
import Components from 'unplugin-vue-components/vite'
import VueRouter from 'unplugin-vue-router/vite'
import { defineConfig } from 'vite'
import Layouts from 'vite-plugin-vue-layouts-next'
import Vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    VueRouter(),
    Layouts(),
    Vue({
      template: { transformAssetUrls }
    }),
    Vuetify({
      autoImport: true,
      styles: {
        configFile: 'src/styles/settings.scss',
      },
    }),
    Components(),
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