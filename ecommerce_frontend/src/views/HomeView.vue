<template>
    <section class="bg-white py-8">
        <div class="container mx-auto flex items-center flex-wrap pt-4 pb-12">
            <nav id="store" class="w-full z-30 top-0 px-6 py-1">
                <div class="w-full container mx-auto flex flex-wrap items-center justify-between mt-0 px-2 py-3">
                    <p class="uppercase tracking-wide no-underline hover:no-underline font-bold text-gray-800 text-xl">
                        最新产品</p>
                </div>
            </nav>
            <div class="w-full md:w-1/3 xl:w-1/4 p-6 flex flex-col" v-for="product in products" v-bind:key="product.id">
                <RouterLink :to="{ name: 'product', params: { id: product.id } }">
                    <img v-if="product.attachments.length > 0"
                        class="hover:grow hover:shadow-lg object-contain h-48 w-96" :src="product.attachments[0].image">
                    <img v-else class="hover:grow hover:shadow-lg object-contain h-48 w-96"
                        src="https://cdn.shopify.com/s/files/1/0533/2089/files/placeholder-images-image_large.png?v=1530129081">
                    <div class="pt-3 flex items-center justify-between">
                        <p class="">{{ product.name }}</p>
                    </div>
                    <template v-if="product.discount_price > 0">
                        <p class="text-xl text-primary font-semibold">￥{{ product.price }}</p>
                        <p class="text-base text-gray-400 line-through">￥{{ product.discount_price }}</p>
                    </template>
                    <template v-else>
                        <p class="text-xl text-gray-900">￥{{ product.price }}</p>
                    </template>
                </RouterLink>
            </div>

        </div>
    </section>
</template>

<script>
import axios from 'axios'

export default {
    name: 'HomeView',
    data() {
        return {
            products: [],
        }
    },
    mounted() {
        this.getProducts()
    },
    methods: {
        getProducts() {
            axios.get('/api/products?page_size=8')
                .then(response => { this.products = response.data.results })
        }
    }
}
</script>

<style scoped>
.hover\:grow {
    transition: all 0.3s;
    transform: scale(1);
}

.hover\:grow:hover {
    transform: scale(1.02);
}
</style>