import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// Configurar axios
import axios from 'axios'
axios.defaults.timeout = 30000

const app = createApp(App)
app.mount('#app')