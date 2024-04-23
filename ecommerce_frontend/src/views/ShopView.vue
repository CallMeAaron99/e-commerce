<template>
    <Breadcrumb />

    <div class="container mx-auto grid md:grid-cols-4 grid-cols-2 gap-6 pt-4 pb-16 items-start">
        <!-- ./sidebar -->
        <div class="col-span-1 bg-white px-4 pb-6 shadow rounded overflow-hiddenb hidden md:block">
            <div class="divide-y divide-gray-200 space-y-5">
                <div>
                    <h3 class="text-xl text-gray-800 mb-3 uppercase font-medium">分类</h3>
                    <div class="space-y-2">
                        <div class="flex items-center" v-for="category in categories" v-bind:key="category.id">
                            <input type="checkbox" :value="category.id" v-model="checkedCategories"
                                :disabled="category.product_count === 0"
                                class="text-primary focus:ring-0 rounded-sm cursor-pointer">
                            <label for="cat-1" class="text-gray-600 ml-3 cusror-pointer">{{ category.name }}</label>
                            <div class="ml-auto text-gray-600 text-sm" v-if="category.product_count > 0">({{
                            category.product_count }})</div>
                        </div>
                    </div>
                </div>
                <div class="pt-4">
                    <h3 class="text-xl text-gray-800 mb-3 uppercase font-medium">品牌</h3>
                    <div class="space-y-2">
                        <div class="flex items-center" v-for="brand in brands" v-bind:key="brand.id">
                            <input type="checkbox" :value="brand.id" v-model="checkedBrands"
                                :disabled="brand.product_count === 0"
                                class="text-primary focus:ring-0 rounded-sm cursor-pointer">
                            <label for="brand-1" class="text-gray-600 ml-3 cusror-pointer">{{ brand.name }}</label>
                            <div class="ml-auto text-gray-600 text-sm" v-if="brand.product_count > 0">({{
                            brand.product_count }})</div>
                        </div>
                    </div>
                </div>
                <div class="pt-4">
                    <h3 class="text-xl text-gray-800 mb-3 uppercase font-medium">价格</h3>
                    <div class="mt-4 flex items-center">
                        <input type="text" name="min" id="min" v-model="minPrice"
                            class="w-full border-gray-300 focus:border-primary rounded focus:ring-0 px-3 py-1 text-gray-600 shadow-sm"
                            placeholder="最低">
                        <span class="mx-3 text-gray-500">-</span>
                        <input type="text" name="max" id="max" v-model="maxPrice"
                            class="w-full border-gray-300 focus:border-primary rounded focus:ring-0 px-3 py-1 text-gray-600 shadow-sm"
                            placeholder="最高">
                        <button
                            class="w-full ms-3 py-1 text-center border rounded bg-sky-200 hover:bg-sky-300 transition"
                            @click="onPriceClick">搜索</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- products -->
        <div class="col-span-3">
            <div class="flex items-center mb-4">
                <select v-model="selectedOrdering"
                    class="w-44 text-sm text-gray-600 py-3 px-4 border-gray-300 shadow-sm rounded focus:ring-primary focus:border-primary">
                    <option value="-created_at">最新商品</option>
                    <option value="price">价格从低到高</option>
                    <option value="-price">价格从高到低</option>
                </select>

            </div>

            <div class="grid md:grid-cols-3 grid-cols-2 gap-6">

                <div class="bg-white shadow rounded overflow-hidden group" v-for="product in product.results"
                    v-bind:key="product.id">
                    <div class="relative">
                        <img :src="product.attachments[0].image" alt="product" class="object-contain h-48 w-96">
                        <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center 
                        justify-center gap-2 opacity-0 group-hover:opacity-100 transition">
                            <RouterLink :to="{ name: 'product', params: { id: product.id } }"
                                class="text-white text-lg w-9 h-8 rounded-full bg-primary flex items-center justify-center hover:bg-gray-800 transition"
                                title="view product">
                                <i class="fa-solid fa-magnifying-glass"></i>
                            </RouterLink>
                            <button @click="wishlistStore.addToWishlist(product)"
                                class="text-white text-lg w-9 h-8 rounded-full bg-primary flex items-center justify-center hover:bg-gray-800 transition"
                                title="add to wishlist">
                                <i class="fa-solid fa-heart"></i>
                            </button>
                        </div>
                    </div>
                    <div class="pt-4 pb-3 px-4">
                        <RouterLink :to="{ name: 'product', params: { id: product.id } }">
                            <h4 class="uppercase font-medium text-xl mb-2 text-gray-800 hover:text-primary transition truncate">
                                {{ product.name }}</h4>
                        </RouterLink>
                        <div class="flex items-baseline mb-1 space-x-2">
                            <template v-if="product.discount_price > 0">
                                <p class="text-xl text-primary font-semibold">￥{{ product.price }}</p>
                                <p class="text-base text-gray-400 line-through">￥{{ product.discount_price }}</p>
                            </template>
                            <template v-else>
                                <p class="text-xl text-gray-900">￥{{ product.price }}</p>
                            </template>
                        </div>

                    </div>
                    <button @click="cartStore.addToCart({ product: product, quantity: 1 })" v-if="product.stock > 0"
                        class="block w-full py-1 text-center text-white bg-primary border border-primary rounded-b hover:bg-transparent hover:text-primary transition">加入购物车</button>
                </div>

            </div>

            <div class="flex flex-col items-center mt-3">
                <!-- Help text -->
                <!-- <span class="text-sm text-gray-700 ">
                    显示 <span class="font-semibold text-gray-900 ">{{ product.count }}</span> 个商品中的 <span
                        class="font-semibold text-gray-900 ">1</span> 至 <span
                        class="font-semibold text-gray-900 ">10</span>
                </span> -->
                <!-- Buttons -->
                <div class="inline-flex mt-2 xs:mt-0 space-x-3">
                    <button :disabled="product.previous === null" @click="refreshProducts(product.previous)"
                        v-bind:class="{ 'opacity-50 cursor-not-allowed': product.previous === null }"
                        class="flex items-center justify-center px-4 h-10 text-base font-medium text-white bg-gray-800 rounded hover:bg-gray-900">
                        上一页
                    </button>
                    <button :disabled="product.next === null" @click="refreshProducts(product.next)"
                        v-bind:class="{ 'opacity-50 cursor-not-allowed': product.next === null }"
                        class="flex items-center justify-center px-4 h-10 text-base font-medium text-white bg-gray-800 border-0 border-s border-gray-700 rounded hover:bg-gray-900">
                        下一页
                    </button>
                </div>
            </div>

        </div>
        <!-- ./products -->
    </div>
</template>

<script>
import axios from 'axios'

import Breadcrumb from '../components/Breadcrumb.vue'
import { useWishlistStore } from '@/stores/wishlist';
import { useCartStore } from '@/stores/cart';

export default {
    name: 'ShopView',
    components: {
        Breadcrumb
    },
    setup() {
        const wishlistStore = useWishlistStore()
        const cartStore = useCartStore()

        return {
            wishlistStore,
            cartStore
        }
    },
    data() {
        return {
            product: {},
            categories: [],
            brands: [],
            checkedCategories: [],
            checkedBrands: [],
            minPrice: '',
            maxPrice: '',
            selectedOrdering: '-created_at'
        }
    },
    watch: {
        '$route.query': {
            handler: function () {
                this.loadData()

                if (this.$route.query.category) {
                    this.checkedCategories = this.$route.query.category.split(',')
                }

                if (this.$route.query.brand) {
                    this.checkedBrands = this.$route.query.brand.split(',')
                }
            },
            deep: true,
            immediate: true
        },
        'checkedCategories': {
            handler: function () {
                this.$router.push({ query: { ...this.$route.query, category: this.checkedCategories.join(',') } })
            },
            deep: true
        },
        'checkedBrands': {
            handler: function () {
                this.$router.push({ query: { ...this.$route.query, brand: this.checkedBrands.join(',') } })
            },
            deep: true
        },
        'selectedOrdering': {
            handler: function () {
                this.$router.push({ query: { ...this.$route.query, ordering: this.selectedOrdering } })
            },
        }
    },
    methods: {
        loadData() {
            this.getProducts()
            this.getCategories()
            this.getBrands()
        },
        refreshProducts(url) {
            axios.get(url)
                .then(response => { this.product = response.data })
        },
        getProducts() {
            axios.get('/api/products', { params: this.$route.query })
                .then(response => { this.product = response.data })
        },
        getCategories() {
            axios.get('/api/products/categories', { params: this.$route.query })
                .then(response => { this.categories = response.data })
        },
        getBrands() {
            axios.get('/api/products/brands', { params: this.$route.query })
                .then(response => { this.brands = response.data })
        },
        onPriceClick() {
            this.$router.push({ query: { ...this.$route.query, min_price: this.minPrice, max_price: this.maxPrice } })
        }
    }
}

</script>