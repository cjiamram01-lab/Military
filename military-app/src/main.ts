import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@fontsource/kanit/300.css'
import '@fontsource/kanit/400.css'
import '@fontsource/kanit/500.css'
import '@fontsource/kanit/600.css'
import './style.css'
import App from './App.vue'
import router from './router'
import { ensureApiConfigured } from './api'

ensureApiConfigured().then(() => {
	createApp(App).use(createPinia()).use(router).mount('#app')
})
