<template>
    <div class="h-screen bg-gray-100 pt-20">
        <h1 class="mb-10 text-center text-2xl font-bold">购物车</h1>
        <template v-if="cartStore.cart.cartTotalLength > 0">
            <div class="mx-auto max-w-5xl justify-center px-6 md:flex md:space-x-6 xl:px-0">
                <div class="rounded-lg md:w-2/3">
                    <div class="justify-between mb-6 rounded-lg bg-white p-6 shadow-md sm:flex sm:justify-start"
                        v-for="(item, index) in cartStore.cart.items" v-bind:key="item.product.id">
                        <img :src="item.product.attachments[0].image" alt="product-image"
                            class="w-full rounded-lg sm:w-40" />
                        <div class="sm:ml-4 sm:flex sm:w-full sm:justify-between">
                            <RouterLink :to="{ name: 'product', params: { id: item.product.id } }">
                                <div class="mt-5 sm:mt-0">
                                    <h2 class="text-lg font-bold hover:text-primary transition">{{ item.product.name }}
                                    </h2>
                                    <p class="text-gray-500 text-sm">库存情况：
                                        <span class="text-green-600" v-if="item.product.stock > 0">{{ item.product.stock }} 件</span>
                                        <span class="text-red-600" v-else>缺货</span>
                                    </p>
                                </div>
                            </RouterLink>
                            <div class="mt-4 flex justify-between sm:space-y-6 sm:mt-0 sm:block sm:space-x-6">
                                <div class="flex items-center border-gray-100">
                                    <button @click="cartStore.updateQuantity(index, item.quantity - 1)"
                                        class="cursor-pointer rounded-l bg-gray-100 py-1 px-3.5 duration-100 hover:bg-blue-500 hover:text-blue-50">
                                        - </button>
                                    <input class="h-8 w-8 border bg-white text-center text-xs outline-none"
                                        type="number" v-model.value="item.quantity"
                                        @change="cartStore.updateQuantity(index, item.quantity)" min="0" />
                                    <button @click="cartStore.updateQuantity(index, item.quantity + 1)"
                                        class="cursor-pointer rounded-r bg-gray-100 py-1 px-3 duration-100 hover:bg-blue-500 hover:text-blue-50">
                                        + </button>
                                </div>
                                <div class="flex items-center space-x-4">
                                    <p class="text-sm">￥{{ (item.product.price * item.quantity).toFixed(2) }}</p>
                                    <button @click="cartStore.removeCart(index)"
                                        class="text-gray-600 cursor-pointer hover:text-primary">
                                        <i class="fa-solid fa-trash"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
                <!-- Sub total -->
                <div class="mt-6 h-full rounded-lg border bg-white p-6 shadow-md md:mt-0 md:w-1/3">
                    <div class="mb-2 flex justify-between">
                        <p class="text-gray-700">小计</p>
                        <p class="text-gray-700">￥{{ (cartStore.cart.cartTotalPrice).toFixed(2) }}</p>
                    </div>
                    <div class="flex justify-between">
                        <p class="text-gray-700">运费</p>
                        <p class="text-gray-700">￥{{ shippingFee }}</p>
                    </div>
                    <hr class="my-4" />
                    <div class="flex justify-between">
                        <p class="text-lg font-bold">合计</p>
                        <div class="">
                            <p class="mb-1 text-lg font-bold">￥{{ (cartStore.cart.cartTotalPrice + shippingFee).toFixed(2) }}</p>
                        </div>
                    </div>
                    <RouterLink
                        class="block w-full py-1 px-4 text-center text-white bg-primary border border-primary rounded-md hover:bg-transparent hover:text-primary transition font-medium"
                        :to="{ name : 'checkout' }">结算</RouterLink>
                </div>
            </div>
        </template>
        <h1 class="mb-10 text-center text-2xl font-bold" v-else>购物车无商品</h1>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import { useCartStore } from '../stores/cart'

export default {
    name: 'CartView',
    setup() {
        const cartStore = useCartStore()
        return {
            cartStore
        }
    },
    data() {
        return {
            shippingFee: 4.99
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