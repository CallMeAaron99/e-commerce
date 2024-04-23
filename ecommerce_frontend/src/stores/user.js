import { defineStore } from 'pinia'
import axios from 'axios'
import Cookies from 'js-cookie'

export const useUserStore = defineStore({
    id: 'user',

    state: () => ({
        user: {
            isAuthenticated: false,
            id: null,
            name: null,
            email: null,
            access: null,
            refresh: null,
            avatar: null
        }
    }),
    actions: {
        async initStore() {
            const refresh = Cookies.get('user.refresh')

            if (refresh) {
                this.user.refresh = refresh
                this.user.isAuthenticated = true
                this.user.id = localStorage.getItem('user.id')
                this.user.name = localStorage.getItem('user.name')
                this.user.email = localStorage.getItem('user.email')
                this.user.avatar = localStorage.getItem('user.avatar')
                await this.refreshToken()
            }
        },
        setToken(data, remember) {
            this.user.refresh = data.refresh
            this.user.access = data.access
            this.user.isAuthenticated = true
            axios.defaults.headers.common["Authorization"] = "Bearer " + this.user.access
            
            Cookies.set('user.refresh', this.user.refresh, { expires: remember ? 90 : null })
        },
        removeToken() {
            axios.defaults.headers.common["Authorization"] = ""

            this.user.access = null
            this.user.refresh = null
            this.user.isAuthenticated = false
            this.user.id = null
            this.user.name = null
            this.user.email = null
            this.user.avatar = null

            Cookies.remove('user.refresh')
            Cookies.remove('user.access')
            localStorage.setItem('user.id', '')
            localStorage.setItem('user.name', '')
            localStorage.setItem('user.email', '')
            localStorage.setItem('user.avatar', '')
        },
        setUserInfo(user) {
            this.user.id = user.id
            this.user.name = user.name
            this.user.email = user.email
            this.user.avatar = user.avatar

            localStorage.setItem('user.id', this.user.id)
            localStorage.setItem('user.name', this.user.name)
            localStorage.setItem('user.email', this.user.email)
            localStorage.setItem('user.avatar', this.user.avatar)
        },
        async refreshToken() {
            try {
                const response = await axios.post('/api/accounts/refresh', { refresh: this.user.refresh })
                this.user.access = response.data.access
                axios.defaults.headers.common["Authorization"] = "Bearer " + this.user.access
            } catch { this.removeToken() }
        },
    }
})