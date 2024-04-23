<template>
    <div class="container mx-auto py-16">
        <div class="max-w-lg mx-auto shadow px-6 py-7 rounded overflow-hidden">
            <h2 class="text-2xl uppercase font-medium mb-8">密码重置</h2>

            <form v-on:submit.prevent="submitForm" autocomplete="off">
                <div class="space-y-2">
                    <div>
                        <label for="email" class="text-gray-600 mb-2 block">电子邮箱</label>
                        <input type="email" name="email" id="email" v-model="form.email"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="youremail@domain.com">
                    </div>
                </div>

                <template v-if="errors.length > 0">
                    <div class="bg-red-300 text-white rounded-lg p-4">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                </template>

                <div class="mt-4">
                    <button type="submit"
                        class="block w-full py-2 text-center text-white bg-primary border border-primary rounded hover:bg-transparent hover:text-primary transition uppercase font-roboto font-medium">重置我的密码</button>
                </div>
            </form>

        </div>
    </div>
</template>

<script>
import axios from 'axios';

import { useToastStore } from '@/stores/toast';

export default {
    name: 'ResetPasswordView',
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

            if (this.errors.length === 0) {
                axios.post('/api/accounts/password_reset', this.form)
                    .then(() => { this.$router.push({ name: 'reset_password_done' }) })
                    .catch(error => {
                        const status = error.response ? error.response.status : null
                        if (status === 400) {
                            const data = error.response.data
                            for (const key in data) {
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