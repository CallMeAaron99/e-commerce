<template>
    <div class="col-span-9 grid grid-cols-2 gap-4">

        <div class="shadow-lg px-6 py-7 rounded overflow-hidden">
            <h2 class="text-2xl uppercase font-medium mb-8">账号信息</h2>

            <form v-on:submit.prevent="submitForm" autocomplete="off">
                <div class="space-y-2 mb-4">
                    <div>
                        <label for="name" class="text-gray-600 mb-2 block">头像</label>
                        <input type="file" ref="file">
                    </div>
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
                email: this.userStore.user.email,
                name: this.userStore.user.name
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

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)

                axios.put('/api/accounts/edit-profile', formData, {
                    headers: { "Content-Type": "multipart/form-data" }
                })
                    .then(response => {
                        this.userStore.setUserInfo({
                            id: response.data.id,
                            name: response.data.name,
                            email: response.data.email,
                            avatar: response.data.avatar
                        })

                        this.toastStore.showToast(5000, '信息已修改', 'bg-emerald-500')

                        this.$router.push({ name: 'account_info' })
                    })
                    .catch(error => {
                        const status = error.response ? error.response.status : null
                        if (status === 409) {
                            this.errors.push("邮箱账号已存在")
                        } else {
                            this.toastStore.showToast(5000, '出错了。请重试', 'bg-red-300')
                        }
                    })
            }
        }
    }
}

</script>