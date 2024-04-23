<template>
    <Breadcrumb />

    <div class="container mx-auto grid grid-cols-2 gap-6">
        <div>
            <img :src="product.attachments[activeImg].image" alt="product" class="object-contain h-[24rem] w-[36rem]">
            <div class="grid grid-cols-5 gap-4 mt-4">
                <img v-for="(attachment, i) in product.attachments" v-bind:key="attachment.id" :src="attachment.image"
                    alt="product" class="object-contain h-48 w-96 cursor-pointer border"
                    :class="{ 'border-primary': i === activeImg }" @click="onImgClick(i)">
            </div>
        </div>
        <h2 class="text-3xl font-medium uppercase mb-2 text-red-600" v-if="product.is_deleted">商品已下架</h2>
        <div v-else>
            <h2 class="text-3xl font-medium uppercase mb-2">{{ product.name }}</h2>

            <div class="space-y-2">
                <p class="text-gray-800 font-semibold space-x-2">
                    <span>库存情况：</span>
                    <span class="text-green-600" v-if="product.stock > 0">{{ product.stock }} 件</span>
                    <span class="text-red-600" v-else>缺货</span>
                </p>
                <p class="text-gray-800 font-semibold space-x-2">
                    <span>销量：</span>
                    <span class="text-red-600">{{ product.sales }} 件</span>
                </p>
                <p class="space-x-2">
                    <span class="text-gray-800 font-semibold">品牌：</span>
                    <span class="text-gray-600">{{ product.brand.name }}</span>
                </p>
                <p class="space-x-2">
                    <span class="text-gray-800 font-semibold">类型：</span>
                    <span class="text-gray-600">{{ product.category.name }}</span>
                </p>
            </div>
            <div class="flex items-baseline mb-1 space-x-2 font-roboto mt-4">
                <template v-if="product.discount_price > 0">
                    <p class="text-xl text-primary font-semibold">￥{{ product.price }}</p>
                    <p class="text-base text-gray-400 line-through">￥{{ product.discount_price }}</p>
                </template>
                <template v-else>
                    <p class="text-xl text-gray-900">￥{{ product.price }}</p>
                </template>
            </div>

            <p class="mt-4 text-gray-600">{{ product.description }}</p>

            <div class="mt-4">
                <h3 class="text-sm text-gray-800 uppercase mb-1">数量</h3>
                <div class="flex border border-gray-300 text-gray-600 divide-x divide-gray-300 w-max">
                    <button @click="quantity--"
                        class="cursor-pointer rounded-l bg-gray-100 py-1 px-3.5 duration-100 hover:bg-blue-500 hover:text-blue-50">
                        - </button>
                    <input class="h-8 w-8 border bg-white text-center text-xs outline-none" type="number"
                        v-model.value="quantity" min="1" />
                    <button @click="quantity++"
                        class="cursor-pointer rounded-r bg-gray-100 py-1 px-3 duration-100 hover:bg-blue-500 hover:text-blue-50">
                        +
                    </button>
                </div>
            </div>

            <div class="mt-6 flex gap-3 border-b border-gray-200 pb-5 pt-5">
                <button @click="cartStore.addToCart({ product, quantity })" v-if="product.stock > 0"
                    class="bg-primary border border-primary text-white px-8 py-2 font-medium rounded uppercase flex items-center gap-2 hover:bg-transparent hover:text-primary transition">
                    <i class="fa-solid fa-bag-shopping"></i> 加入购物车
                </button>
                <button @click="wishlistStore.addToWishlist(product)"
                    class="border border-gray-300 text-gray-600 px-8 py-2 font-medium rounded uppercase flex items-center gap-2 hover:text-primary transition">
                    <i class="fa-solid fa-heart"></i> 收藏
                </button>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios'

import Breadcrumb from '../components/Breadcrumb.vue'
import { useWishlistStore } from '../stores/wishlist'
import { useCartStore } from '@/stores/cart';

export default {
    name: 'ProductView',
    setup() {
        const wishlistStore = useWishlistStore()
        const cartStore = useCartStore()

        return {
            wishlistStore,
            cartStore
        }
    },
    components: {
        Breadcrumb
    },
    data() {
        return {
            product: {
                id: '',
                brand: {},
                category: {},
                attachments: [{
                    id: ''
                }]
            },
            quantity: 1,
            activeImg: 0
        }
    },
    mounted() {
        this.getProduct()
    },
    watch: {
        'quantity': {
            handler: function () {
                if (this.quantity > this.product.stock) {
                    this.quantity = this.product.stock
                    return
                }

                if (this.quantity < 1) {
                    this.quantity = 1
                }
            },
        },
    },
    methods: {
        getProduct() {
            axios.get(`/api/products/${this.$route.params.id}`)
                .then(response => { this.product = response.data })
        },
        decrementQuantity() {
            if (this.quantity > 1) {
                this.quantity--;
            }
        },
        incrementQuantity() {
            this.quantity++;
        },
        onImgClick(i) {
            this.activeImg = i
        }
    }
}

</script>

<style scoped>
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
</style>