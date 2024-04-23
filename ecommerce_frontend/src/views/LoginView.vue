<template>
    <div class="container mx-auto py-16">
        <div class="max-w-lg mx-auto shadow-lg px-6 py-7 rounded overflow-hidden">
            <h2 class="text-2xl uppercase font-medium mb-8">登录</h2>

            <form v-on:submit.prevent="submitForm">
                <div class="space-y-2">
                    <div>
                        <label for="email" class="text-gray-600 mb-2 block">电子邮箱</label>
                        <input type="email" name="email" id="email" v-model="form.email"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="youremail@domain.com">
                    </div>
                    <div>
                        <label for="password" class="text-gray-600 mb-2 block">密码</label>
                        <input type="password" name="password" id="password" v-model="form.password"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="*******">
                    </div>
                </div>
                <div class="flex items-center justify-between mt-6 mb-4">
                    <div class="flex items-center">
                        <input type="checkbox" name="remember" id="remember" v-model="remember"
                            class="text-primary focus:ring-0 rounded-sm cursor-pointer">
                        <label for="remember" class="text-gray-600 ml-3 cursor-pointer">记住我</label>
                    </div>
                    <RouterLink :to="{ 'name': 'reset_password' }" class="text-primary">忘记密码</RouterLink>
                </div>

                <template v-if="errors.length > 0">
                    <div class="bg-red-300 text-white rounded-lg p-4">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                </template>

                <div class="mt-4">
                    <button type="submit"
                        class="block w-full py-2 text-center text-white bg-primary border border-primary rounded hover:bg-transparent hover:text-primary transition uppercase font-roboto font-medium">登录</button>
                </div>
            </form>

            <p class="mt-4 text-center text-gray-600">没有账号？<RouterLink :to="{ 'name': 'sign_up' }" class="text-primary">
                    注册
                </RouterLink>
            </p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { useWishlistStore } from '@/stores/wishlist';
import { useCartStore } from '@/stores/cart';

export default {
    name: 'LoginView',
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
        const wishlistStore = useWishlistStore()
        const cartStore = useCartStore()

        return {
            userStore,
            toastStore,
            wishlistStore,
            cartStore
        }
    },
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            remember: false,
            errors: [],
        }
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('电子邮箱不能为空')
            }

            if (this.form.password === '') {
                this.errors.push('密码不能为空')
            }

            if (this.errors.length === 0) {
                axios.post('/api/accounts/login', this.form)
                    .then(response => {
                        this.userStore.setToken(response.data, this.remember)

                        localStorage.setItem('cartInited', "false")
                        this.wishlistStore.initStore()
                        this.cartStore.initStore()
                    })
                    .then(() => {
                        axios.get('/api/accounts/me')
                            .then(response => {
                                this.userStore.setUserInfo(response.data)
                                const toPath = this.$route.query.to || '/'
                                this.$router.push(toPath)
                            })
                    })
                    .catch(error => {
                        const status = error.response ? error.response.status : null
                        if (status === 401) {
                            this.errors.push('电子邮箱或密码不正确！或用户未激活！')
                        } else {
                            this.toastStore.showToast(5000, '出错了。请重试', 'bg-red-300')
                        }
                    })
            }
        }
    }
}
</script>