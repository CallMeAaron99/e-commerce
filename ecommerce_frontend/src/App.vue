<template>
    <Navbar />
    <main>
        <RouterView />
    </main>
    <Toast />
</template>

<script>
import Toast from '@/components/Toast.vue'

import { useUserStore } from '@/stores/user'
import { useWishlistStore } from '@/stores/wishlist';
import { useCartStore } from '@/stores/cart';

import Navbar from '@/components/Navbar.vue';

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
    components: {
        Navbar,
        Toast
    },
    async beforeCreate() {

        await this.userStore.initStore()

        if (this.userStore.user.isAuthenticated) {
            this.wishlistStore.initStore()
        }
        this.cartStore.initStore()
    }
}
</script>
