import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Configuración global de Axios
axios.defaults.baseURL = 'http://localhost:9000'
axios.defaults.withCredentials = true // para las cookies de Flask

const app = createApp(App)
app.config.globalProperties.$axios = axios
app.use(router)
app.mount('#app')