<template>
    <div class="container mx-auto py-16">
        <div class="max-w-lg mx-auto shadow-lg px-6 py-7 rounded overflow-hidden">
            <h2 class="text-2xl uppercase font-medium mb-8">注册账号</h2>

            <form v-on:submit.prevent="submitForm">
                <div class="space-y-2 mb-4">
                    <div>
                        <label for="name" class="text-gray-600 mb-2 block">用户名</label>
                        <input type="text" name="name" id="name" v-model="form.name"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="username">
                    </div>
                    <div>
                        <label for="email" class="text-gray-600 mb-2 block">电子邮箱</label>
                        <input type="email" name="email" id="email" v-model="form.email"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="youremail@domain.com">
                    </div>
                    <div>
                        <label for="password1" class="text-gray-600 mb-2 block">密码</label>
                        <input type="password" name="password1" id="password1" v-model="form.password1"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="*******">
                    </div>
                    <div>
                        <label for="password2" class="text-gray-600 mb-2 block">密码确认</label>
                        <input type="password" name="password2" id="password2" v-model="form.password2"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="*******">
                    </div>
                </div>
                
                <template v-if="errors.length > 0">
                    <div class="bg-red-300 text-white rounded-lg p-4">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                </template>

                <div class="mt-4">
                    <button type="submit"
                        class="block w-full py-2 text-center text-white bg-primary border border-primary rounded hover:bg-transparent hover:text-primary transition uppercase font-roboto font-medium">注册账号</button>
                </div>
            </form>

            <p class="mt-4 text-center text-gray-600">已经有账号？<RouterLink :to="{'name': 'login'}" class="text-primary">登录</RouterLink></p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

import { useToastStore } from '@/stores/toast';
import Navbar from '@/components/Navbar.vue';

export default {
    name: 'RegisterView',
    components: {
        Navbar
    },
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },
    data() {
        return {
            form: {
                email: '',
                name: '',
                password1: '',
                password2: ''
            },
            errors: [],
        }
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('电子邮箱不能为空')
            }

            if (this.form.name === '') {
                this.errors.push('用户名不能为空')
            }

            if (this.form.password1 === '') {
                this.errors.push('密码不能为空')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('密码不匹配')
            }

            if (this.errors.length === 0) {
                axios.post('/api/accounts/signup', this.form)
                    .then(response => {
                        this.toastStore.showToast(5000, '账号已注册。请通过电子邮件激活您的帐户。', 'bg-emerald-500')
                        this.$router.push({ name: 'login' })
                    })
                    .catch(error => {
                        const status = error.response ? error.response.status : null
                        if (status === 400) {
                            const data = error.response.data
                            for (const key in data){
                                this.errors.push(...data[key])
                            }
                        } else {
                            this.toastStore.showToast(5000, '出错了。请重试', 'bg-red-300')
                        }
                    })
            }
        }
    }
}
</script>