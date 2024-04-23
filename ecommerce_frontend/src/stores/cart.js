import axios from 'axios'

import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export const useCartStore = defineStore({
    id: 'cart',

    state: () => ({
        cart: {
            items: [],
            cartTotalLength: 0,
            cartTotalPrice: 0
        },
    }),

    actions: {
        initStore() {
            const userStore = useUserStore()

            if (userStore.user.isAuthenticated) {
                axios.get('/api/accounts/cart')
                    .then(response => {
                        this.cart.items = response.data
                        const cartInited = JSON.parse(localStorage.getItem('cartInited'))

                        if (!cartInited) {
                            if (localStorage.getItem('cart')) {
                                // Add local cart items to server
                                const local_cart = JSON.parse(localStorage.getItem('cart'))

                                for (const item of local_cart.items)
                                    this.addToCart(item, false)
                            } else {
                                // Set local cart as user's cart
                                this.cart.cartTotalLength = this.cart.items.reduce((acc, curVal) => acc += curVal.quantity, 0)
                                this.cart.cartTotalPrice = this.cart.items.reduce((acc, curVal) => acc += curVal.quantity * curVal.product.price, 0)
                                localStorage.setItem('cart', JSON.stringify(this.cart))
                            }
                        }
                        localStorage.setItem('cartInited', "true")
                    })
            }

            if (localStorage.getItem('cart')) {
                this.cart = JSON.parse(localStorage.getItem('cart'))
            }
        },
        updateCart(item) {
            const userStore = useUserStore()

            if (userStore.user.isAuthenticated) {
                axios.post('/api/accounts/cart', { product: item.product.id, quantity: item.quantity })
                    .then(response => { item.id = response.data.id })
            }
            return item;
        },
        addToCart(item, toast = true) {
            const toastStore = useToastStore()
            const index = this.cart.items.findIndex(i => i.product.id === item.product.id)

            if (index !== -1) {
                // Adding existing cart product
                this.updateQuantity(index, this.cart.items[index].quantity + item.quantity);
            } else {
                const updatedItem = this.updateCart(item);
                this.cart.items.push(updatedItem);
            }

            this.cart.cartTotalLength = this.cart.items.reduce((acc, curVal) => acc += curVal.quantity, 0)
            this.cart.cartTotalPrice = this.cart.items.reduce((acc, curVal) => acc += curVal.quantity * curVal.product.price, 0)
            localStorage.setItem('cart', JSON.stringify(this.cart))

            if (toast)
                toastStore.showToast(5000, '商品加入购物车', 'bg-emerald-500')
        },
        removeCart(index) {
            const userStore = useUserStore()

            if (userStore.user.isAuthenticated) {
                // Remove server cart
                axios.delete(`/api/accounts/cart/${this.cart.items[index].id}`)
            }

            this.cart.items.splice(index, 1)
            this.cart.cartTotalLength = this.cart.items.reduce((acc, curVal) => acc += curVal.quantity, 0)
            this.cart.cartTotalPrice = this.cart.items.reduce((acc, curVal) => acc += curVal.quantity * curVal.product.price, 0)
            localStorage.setItem('cart', JSON.stringify(this.cart))
        },
        updateQuantity(index, quantity) {

            if (quantity > this.cart.items[index].product.stock) {
                this.cart.items[index].quantity = this.cart.items[index].product.stock
                return
            }

            if (quantity < 1) {
                this.cart.items[index].quantity = 1
                return
            }

            const userStore = useUserStore()

            if (userStore.user.isAuthenticated) {
                // Update server cart
                axios.put(`/api/accounts/cart/${this.cart.items[index].id}`, { product: this.cart.items[index].product.id, quantity })
            }

            this.cart.items[index].quantity = quantity
            this.cart.cartTotalLength = this.cart.items.reduce((acc, curVal) => acc += curVal.quantity, 0)
            this.cart.cartTotalPrice = this.cart.items.reduce((acc, curVal) => acc += curVal.quantity * curVal.product.price, 0)
            localStorage.setItem('cart', JSON.stringify(this.cart))
        },
        clearCart() {
            this.cart.items = []
            this.cart.cartTotalLength = 0
            this.cartTotalPrice = 0
            localStorage.setItem('cart', "")
            localStorage.setItem('cartInited', "false")
        }
    }
})
