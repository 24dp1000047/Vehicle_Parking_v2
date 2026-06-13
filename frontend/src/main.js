import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './routes.js'
window.API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const app = createApp(App)
app.use(router)
app.mount('#app')
