<template>
    <div class="col-span-6">
        <div class="bg-white rounded shadow-lg p-4 px-4 md:p-8 mb-6">
            <form v-on:submit.prevent="submitForm" class="grid gap-4 gap-y-2 text-sm grid-cols-1 md:grid-cols-5">
                <div class="md:col-span-5">
                    <label for="receiver">收货人</label>
                    <input type="text" name="receiver" id="receiver" v-model="address.receiver"
                        class="h-10 border mt-1 rounded px-4 w-full bg-gray-50" value="" />
                </div>

                <div class="md:col-span-5">
                    <label for="phone">手机号</label>
                    <input type="text" name="phone" id="phone" v-model="address.phone" @input="updatePhone"
                        class="h-10 border mt-1 rounded px-4 w-full bg-gray-50" value="" />
                </div>

                <div class="md:col-span-3">
                    <label for="street">街道</label>
                    <input type="text" name="street" id="street" v-model="address.street"
                        class="h-10 border mt-1 rounded px-4 w-full bg-gray-50" value="" placeholder="" />
                </div>

                <div class="md:col-span-2">
                    <label for="city">市区</label>
                    <input type="text" name="city" id="city" v-model="address.city"
                        class="h-10 border mt-1 rounded px-4 w-full bg-gray-50" value="" placeholder="" />
                </div>

                <div class="md:col-span-2">
                    <label for="country">国家 / 地区</label>
                    <div class="h-10 bg-gray-50 flex border border-gray-200 rounded items-center mt-1">
                        <select name="country" id="country" v-model="address.country"
                            class="px-4 outline-none text-gray-800 w-full bg-transparent">
                            <option value="" selected disabled hidden>选择一个国家</option>
                            <option :value="key" v-for="(country, key) in countries">{{ country }}</option>
                        </select>
                    </div>
                </div>

                <div class="md:col-span-2">
                    <label for="province">省</label>
                    <div class="h-10 bg-gray-50 flex border border-gray-200 rounded items-center mt-1">
                        <input name="province" id="province" v-model="address.province"
                            class="px-4 appearance-none outline-none text-gray-800 w-full bg-transparent" />
                    </div>
                </div>

                <div class="md:col-span-1">
                    <label for="zipcode">邮政编码</label>
                    <input type="text" name="zipcode" id="zipcode" v-model="address.zip_code"
                        class="transition-all flex items-center h-10 border mt-1 rounded px-4 w-full bg-gray-50"
                        placeholder="" value="" />
                </div>

                <div class="md:col-span-5">
                    <div class="inline-flex items-center">
                        <input type="checkbox" v-model="address.is_default" name="is_default" id="is_default"
                            class="form-checkbox" />
                        <label for="is_default" class="ml-2">保存为默认地址</label>
                    </div>
                </div>

                <template v-if="errors.length > 0">
                    <div class="md:col-span-5 bg-red-300 text-white rounded-lg p-4">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                </template>
                <hr class="md:col-span-5 my-4">

                <div class="md:col-span-3">
                    <div class="inline-flex items-start" v-if="address.id">
                        <button @click="removeAddress(address.id)"
                            class="flex items-center px-5 py-2.5 font-medium tracking-wide text-black capitalize bg-red-200 rounded-md hover:bg-primary hover:fill-current focus:outline-none transition duration-300 transform active:scale-95 ease-in-out">
                            <i class="fa-solid fa-trash"></i>
                            <span class="pl-2 mx-1">删除</span>
                        </button>
                    </div>
                </div>
                <div class="md:col-span-1 text-right">
                    <div class="inline-flex">
                        <RouterLink :to="{ 'name': 'address_list' }"
                            class="flex items-center px-5 py-2.5 font-medium tracking-wide text-black capitalize rounded-md hover:bg-slate-200 hover:fill-current hover:text-red-600 focus:outline-none transition duration-300 transform active:scale-95 ease-in-out">
                            <i class="fa-solid fa-ban"></i>
                            <span class="pl-2 mx-1">取消</span>
                        </RouterLink>
                    </div>
                </div>
                <div class="md:col-span-1 text-right">
                    <div class="inline-flex items-end">
                        <button type="submit"
                            class="flex items-center px-5 py-2.5 font-medium tracking-wide text-white capitalize bg-black rounded-md hover:bg-gray-800 focus:outline-none focus:bg-gray-900 transition duration-300 transform active:scale-95 ease-in-out">
                            <i class="fa-solid fa-floppy-disk"></i>
                            <span class="pl-2 mx-1">保存</span>
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'AddressEdit',
    data() {
        return {
            address: {
                receiver: '',
                country: '',
                city: '',
                street: '',
                province: '',
                zip_code: '',
                phone: '',
                is_default: false,
            },
            countries: {},
            errors: [],
        }
    },
    mounted() {
        this.getCountries()
        this.getAddress()
    },
    methods: {
        updatePhone() {
            const x = this.address.phone
                .replace(/\D/g, "")
                .match(/(\d{0,3})(\d{0,4})(\d{0,4})/);

            this.address.phone = !x[2]
                ? x[1]
                : x[1] + "-" + x[2] + (x[3] ? "-" + x[3] : "");
        },
        getCountries() {
            axios.get('/api/accounts/countries')
                .then(response => { this.countries = response.data })
        },
        getAddress() {
            if (this.$route.params.id) {
                axios.get(`/api/accounts/addresses/${this.$route.params.id}`)
                    .then(response => { this.address = response.data })
            }
        },
        removeAddress(id) {
            axios.delete(`/api/accounts/addresses/${id}`)
                .then(() => { this.$router.push({ name: 'address_list' }) })
        },
        async submitForm() {
            this.errors = []

            if (this.address.receiver === '') {
                this.errors.push('收货人不能为空')
            }

            if (this.address.country === '') {
                this.errors.push('国家不能为空')
            }

            if (this.address.city === '') {
                this.errors.push('市区不能为空')
            }

            if (this.address.street === '') {
                this.errors.push('街道不能为空')
            }

            if (this.address.province === '') {
                this.errors.push('省不能为空')
            }

            if (this.address.zip_code === '') {
                this.errors.push('邮政编码不能为空')
            }

            if (this.address.phone === '') {
                this.errors.push('手机号不能为空')
            }

            if (this.errors.length === 0) {
                try {
                    const response = this.address.id
                        ? await axios.put(`/api/accounts/addresses/${this.address.id}`, this.address)
                        : await axios.post('/api/accounts/addresses', this.address);
                    this.addresses = response.data;
                    this.$router.push({ name: 'address_list' })
                } catch (error) {
                    const status = error.response ? error.response.status : null
                    if (status === 400) {
                        const data = error.response.data
                        for (const key in data) {
                            this.errors.push(...data[key])
                        }
                    }
                }
            }
        }
    }
}
</script>