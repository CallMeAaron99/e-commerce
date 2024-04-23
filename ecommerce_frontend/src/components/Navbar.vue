<template>

    <!-- Header -->
    <header class="py-4 shadow-sm bg-white">
        <div class="container mx-auto flex items-center justify-between">
            <RouterLink :to="{ 'name': 'home' }">
                <img src="@/assets/logo.png" alt="Logo" class="size-16">
            </RouterLink>

            <form v-on:submit.prevent="submitForm" autocomplete="off" class="w-full max-w-xl relative hidden md:flex">
                <span class="absolute left-4 top-3 text-lg text-gray-400">
                    <i class="fa-solid fa-magnifying-glass"></i>
                </span>
                <input type="text" name="search" id="search" v-model="search"
                    class="w-full border border-primary border-r-0 pl-12 py-3 pr-3 rounded-l-md focus:outline-none"
                    placeholder="搜索商品">
                <button type="submit"
                    class="bg-primary border border-primary text-white px-8 rounded-r-md hover:bg-transparent hover:text-primary transition whitespace-nowrap">搜索</button>
            </form>

            <div class="flex items-center space-x-4">
                <RouterLink :to="{ 'name': 'wishlist' }"
                    class="text-center text-gray-700 hover:text-primary transition relative">
                    <div class="text-2xl">
                        <i class="fa-regular fa-heart"></i>
                    </div>
                    <div class="text-xs leading-3">收藏</div>
                    <div v-if="wishlistStore.wishlist.length < 9"
                        class="absolute -right-3 -top-1 w-5 h-5 rounded-full flex items-center justify-center bg-primary text-white text-xs">
                        {{ wishlistStore.wishlist.length }}</div>
                    <div v-else
                        class="absolute -right-3 -top-1 w-5 h-5 rounded-full flex items-center justify-center bg-primary text-white text-xs">
                        9+</div>
                </RouterLink>
                <RouterLink :to="{ 'name': 'cart' }"
                    class="text-center text-gray-700 hover:text-primary transition relative">
                    <div class="text-2xl">
                        <i class="fa-solid fa-bag-shopping"></i>
                    </div>
                    <div class="text-xs leading-3">购物车</div>
                    <div v-if="cartStore.cart.cartTotalLength < 9"
                        class="absolute -right-2 -top-1 w-5 h-5 rounded-full flex items-center justify-center bg-primary text-white text-xs">
                        {{ cartStore.cart.cartTotalLength }}</div>
                    <div v-else
                        class="absolute -right-2 -top-1 w-5 h-5 rounded-full flex items-center justify-center bg-primary text-white text-xs">
                        9+</div>
                </RouterLink>
                <RouterLink :to="{ 'name': 'account_info' }"
                    class="text-center text-gray-700 hover:text-primary transition relative">
                    <div class="text-2xl">
                        <i class="fa-regular fa-user"></i>
                    </div>
                    <div class="text-xs leading-3">账号</div>
                </RouterLink>
            </div>
        </div>
    </header>

    <!-- Navbar -->
    <nav class="bg-gray-800">
        <div class="container mx-auto flex">
            <div class="px-8 py-4 bg-primary flex items-center cursor-pointer relative group">
                <span class="text-white">
                    <i class="fa-solid fa-bars"></i>
                </span>
                <span class="capitalize ml-2 text-white">所有品牌</span>

                <!-- Dropdown -->
                <div
                    class="absolute w-full left-0 top-full bg-white shadow-md py-3 divide-y divide-gray-300 divide-dashed opacity-0 group-hover:opacity-100 transition duration-300 invisible group-hover:visible z-50">

                    <RouterLink :to="{ 'name': 'shop', query: { brand: brand.id } }" v-for="brand in brands"
                        v-bind:key="brand.id" class="flex items-center px-6 py-3 hover:bg-gray-100 transition">
                        <img :src="brand.logo" alt="brand logo" class="w-5 h-5 object-contain">
                        <span class="ml-6 text-gray-600 text-sm">{{ brand.name }}</span>
                    </RouterLink>

                </div>
            </div>

            <div class="flex items-center justify-between flex-grow pl-12">
                <div class="flex items-center space-x-6 capitalize">
                    <RouterLink :to="{ 'name': 'home' }" class="text-gray-200 hover:text-white transition">首页
                    </RouterLink>
                    <RouterLink :to="{ 'name': 'shop' }" class="text-gray-200 hover:text-white transition">商品
                    </RouterLink>
                </div>
                <RouterLink :to="{ 'name': 'login' }" v-if="!userStore.user.isAuthenticated"
                    class="text-gray-200 hover:text-white transition">登录</RouterLink>
            </div>
        </div>
    </nav>
</template>

<script>
import axios from 'axios'

import { useUserStore } from '@/stores/user'
import { useWishlistStore } from '@/stores/wishlist';
import { useCartStore } from '@/stores/cart';

export default {
    setup() {
        const userStore = useUserStore()
        const wishlistStore = useWishlistStore()
        const cartStore = useCartStore()

        return {
            userStore,
            wishlistStore,
            cartStore
        }
    },
    data() {
        return {
            search: '',
            brands: []
        }
    },
    mounted() {
        this.getBrands()
    },
    methods: {
        submitForm() {
            this.$router.push({ name: 'shop', query: { name: this.search } })
            this.search = ''
        },
        getBrands() {
            axios.get('/api/products/brands')
                .then(response => { this.brands = response.data })
        }
    }
}
</script>

<style scoped>
#menu-toggle:checked+#menu {
    display: block;
}
</style>