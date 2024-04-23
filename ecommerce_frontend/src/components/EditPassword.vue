<template>
    <div class="col-span-9 grid grid-cols-2 gap-4">

        <div class="shadow-lg px-6 py-7 rounded overflow-hidden">
            <h2 class="text-2xl uppercase font-medium mb-8">修改密码</h2>

            <form v-on:submit.prevent="submitForm" autocomplete="off">
                <div class="space-y-2 mb-4">
                    <div>
                        <label for="old_password" class="text-gray-600 mb-2 block">原密码</label>
                        <input type="password" name="old_password" id="old_password" v-model="form.old_password"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="*******">
                    </div>
                    <div>
                        <label for="new_password1" class="text-gray-600 mb-2 block">新密码</label>
                        <input type="password" name="new_password1" id="new_password1" v-model="form.new_password1"
                            class="block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400"
                            placeholder="*******">
                    </div>
                    <div>
                        <label for="new_password2" class="text-gray-600 mb-2 block">重复新密码</label>
                        <input type="password" name="new_password2" id="new_password2" v-model="form.new_password2"
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
                        class="block w-full py-2 text-center text-white bg-primary border border-primary rounded hover:bg-transparent hover:text-primary transition uppercase font-roboto font-medium">保存更改</button>
                </div>
            </form>
        </div>

    </div>
</template>

<script>
import axios from 'axios';

import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },
    data() {
        return {
            form: {
                old_password: '',
                new_password1: '',
                new_password2: '',
            },
            errors: [],
        }
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.form.old_password === '') {
                this.errors.push('原密码不能为空')
            }

            if (this.form.new_password1 !== this.form.new_password2) {
                this.errors.push('新密码不匹配')
            }

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('old_password', this.form.old_password)
                formData.append('new_password1', this.form.new_password1)
                formData.append('new_password2', this.form.new_password2)

                axios.put('/api/accounts/edit-password', formData)
                    .then(response => {
                        this.toastStore.showToast(5000, '密码已修改', 'bg-emerald-500')

                        this.$router.push({ name: 'account_info' })
                    })
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