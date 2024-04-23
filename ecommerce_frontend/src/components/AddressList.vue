<template>
    <div class="col-span-9 grid grid-cols-3 gap-4">
        <RouterLink :to="{ name: 'address_edit', params: { id: 0 } }"
            class="relative w-full flex justify-center items-center border border-black px-5 py-2.5 font-medium tracking-wide text-black capitalize bg-white rounded-md hover:bg-neutral-400 focus:outline-none transition duration-300 transform active:scale-95 ease-in-out">
            <i class="fa-solid fa-plus"></i>
            <span class="pl-2 mx-1">创建新地址</span>
        </RouterLink>
        <div class="shadow rounded bg-white px-4 pt-6 pb-8" v-for="address in addresses" v-bind:key="address.id">
            <div class="inline-block relative py-1 text-xs">
                <div class="flex-grow h-full bg-indigo-200 rounded-md px-2 py-1" v-if="address.is_default">
                    <span class="relative text-indigo-500 uppercase font-semibold">默认地址</span>
                </div>
            </div>
            <div class="flex items-center justify-between mb-4">
                <h3 class="font-medium text-gray-800 text-lg">{{ address.receiver }}</h3>
                <RouterLink :to="{ name: 'address_edit', params: { id: address.id } }" class="text-primary">编辑</RouterLink>
            </div>
            <div class="space-y-1">
                <p class="text-gray-800">{{ address.country }}, {{ address.province }} {{ address.city }}</p>
                <p class="text-gray-800">{{ address.street }}</p>
                <p class="text-gray-800">{{ address.zip_code }}</p>
                <p class="text-gray-800">{{ address.phone }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'AddressList',
    data() {
        return {
            addresses: [],
        }
    },
    mounted() {
        this.getAddresses()
    },
    methods: {
        getAddresses() {
            axios.get('/api/accounts/addresses')
                .then(response => { this.addresses = response.data })
        }
    }
}
</script>