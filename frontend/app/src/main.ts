import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useThemeConfigStore } from './stores/themeConfigStore'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Aplica colores/fuente de marca (localStorage por ahora) antes de montar,
// para que no haya "flash" sin marca ni siquiera en /login.
useThemeConfigStore()

app.mount('#app')
