import axios from 'axios'
import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export const useWishlistStore = defineStore({
    id: 'wishlist',

    state: () => ({
        wishlist: [],
    }),

    actions: {
        initStore() {
            axios.get('/api/accounts/wishlists')
                .then(response => { this.wishlist = response.data })
        },
        addToWishlist(product) {
            const userStore = useUserStore()
            if (!userStore.user.isAuthenticated) return this.$router.push({ name: "login" })
            
            const toastStore = useToastStore()

            // Product exists in wishlist
            if (this.wishlist.find(wishlist => wishlist.product.id === product.id)) {
                toastStore.showToast(5000, '商品已收藏', 'bg-red-300')
                return
            }

            axios.post('/api/accounts/wishlists', { product: product.id })
                .then(response => {
                    this.wishlist.push({ id: response.data.id, product })
                    toastStore.showToast(5000, '商品加入收藏', 'bg-emerald-500')
                })

        },
        removeWishlist(index) {
            axios.delete(`/api/accounts/wishlists/${this.wishlist[index].id}`)
                .then(() => { this.wishlist.splice(index, 1) })
        },
        clearWishlist() {
            this.wishlist = []
        }
    }
})
