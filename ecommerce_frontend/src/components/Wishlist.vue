<template>
    <div class="col-span-9 space-y-4">

        <template v-if="wishlistStore.wishlist.length > 0">
            <div class="flex items-center justify-between border gap-6 p-4 border-gray-200 rounded"
                v-for="(wishlist, index) in wishlistStore.wishlist" v-bind:key="wishlist.id">
                <div class="w-28">
                    <img :src="wishlist.product.attachments[0].image" alt="product" class="w-full">
                </div>
                <div class="w-1/3">
                    <RouterLink :to="{ name: 'product', params: { id: wishlist.product.id } }">
                        <h4 class="uppercase font-medium text-xl mb-2 text-gray-800 hover:text-primary transition">
                            {{ wishlist.product.name }}</h4>
                    </RouterLink>
                    <p class="text-gray-500 text-sm">库存情况：
                        <span class="text-green-600" v-if="wishlist.product.stock > 0">{{ wishlist.product.stock }} 件</span>
                        <span class="text-red-600" v-else>缺货</span>
                    </p>
                </div>
                <div class="text-primary text-lg font-semibold" v-if="wishlist.product.discount_price > 0">￥{{
            wishlist.product.discount_price }}</div>
                <div class="text-primary text-lg font-semibold" v-else>￥{{ wishlist.product.price }}</div>
                <button @click="cartStore.addToCart({ product: wishlist.product, quantity: 1 })"
                    v-if="wishlist.product.stock > 0"
                    class="px-6 py-2 text-center text-sm text-white bg-primary border border-primary rounded hover:bg-transparent hover:text-primary transition uppercase font-roboto font-medium">添加到购物车</button>
                <button v-else
                    class="cursor-not-allowed px-6 py-2 text-center text-sm text-white bg-red-400 border border-red-400 rounded transition uppercase font-roboto font-medium"
                    disabled>添加到购物车</button>
                <button @click="wishlistStore.removeWishlist(index)"
                    class="text-gray-600 cursor-pointer hover:text-primary">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </template>
        <h1 class="mb-10 text-center text-2xl font-bold" v-else>无商品收藏</h1>
    </div>
</template>


<script>
import { useWishlistStore } from '../stores/wishlist'
import { useCartStore } from '@/stores/cart';

export default {
    name: 'Wishlist',
    setup() {

        const wishlistStore = useWishlistStore()
        const cartStore = useCartStore()

        return {
            wishlistStore,
            cartStore
        }
    },
}
</script>