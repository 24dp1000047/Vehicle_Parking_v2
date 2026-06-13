import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './routes.js'

window.API_URL = 'https://vehicle-parking-v2-5zb6.onrender.com'

const app = createApp(App)
app.use(router)
app.mount('#app')
