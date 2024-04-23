import './assets/main.css'

import { createApp, markRaw } from 'vue'
import { createPinia } from 'pinia'
import { useUserStore } from '@/stores/user'

import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App)
const pinia = createPinia()

// Vue router as pinia plugin
pinia.use(({ store }) => {
    store.$router = markRaw(router)
})

app.use(pinia)

// Handel error status code
axios.interceptors.response.use(response => response,
    async error => {
        const status = error.response ? error.response.status : null
        const userStore = useUserStore();

        if (status === 401 && userStore.user.isAuthenticated) {
            const originalRequest = error.config;

            if (originalRequest.url === '/api/accounts/refresh') {
                userStore.removeToken()
                router.push({ name: 'login' })
                return Promise.reject(error);
            }

            await userStore.refreshToken();
            originalRequest.headers['Authorization'] = "Bearer " + userStore.user.access;
            return axios(originalRequest);
        }
        console.log(error);
        return Promise.reject(error);
    });

app.use(router, axios)

app.mount('#app')
