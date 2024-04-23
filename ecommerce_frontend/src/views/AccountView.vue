<template>
    <Breadcrumb />

    <div class="container mx-auto grid grid-cols-12 items-start gap-6 pt-4 pb-16">

        <!-- sidebar -->
        <div class="col-span-3">
            <div class="px-4 py-3 shadow flex items-center gap-4">
                <div class="flex-shrink-0">
                    <img :src="userStore.user.avatar" alt="profile"
                        class="rounded-full w-14 h-14 border border-gray-200 p-1 object-cover">
                </div>
                <div class="flex-grow">
                    <p class="text-gray-600">欢迎，</p>
                    <h4 class="text-gray-800 font-medium">{{ userStore.user.name }}</h4>
                </div>
            </div>

            <div class="mt-6 bg-white shadow rounded p-4 divide-y divide-gray-200 space-y-4 text-gray-600">
                <div class="space-y-1 pl-8">
                    <RouterLink :to="{ 'name' : 'account_info' }" v-bind:class="{ 'text-primary': $route.name === 'account_info' }" 
                        class="relative hover:text-primary block font-medium capitalize transition">
                        <span class="absolute -left-8 top-0 text-base">
                            <i class="fa-regular fa-address-card"></i>
                        </span>
                        账号管理
                    </RouterLink>
                    <RouterLink :to="{ 'name' : 'edit_profile' }" v-bind:class="{ 'text-primary': $route.name === 'edit_profile' }" 
                        class="relative hover:text-primary block capitalize transition">
                        账号信息
                    </RouterLink>
                    <RouterLink :to="{ 'name' : 'edit_password' }" v-bind:class="{ 'text-primary': $route.name === 'edit_password' }"
                        class="relative hover:text-primary block capitalize transition">
                        修改密码
                    </RouterLink>
                    <RouterLink :to="{ 'name' : 'address_list' }" v-bind:class="{ 'text-primary': $route.name === 'address_list' }"
                        class="relative hover:text-primary block capitalize transition">
                        地址管理
                    </RouterLink>
                </div>

                <div class="space-y-1 pl-8 pt-4">
                    <RouterLink :to="{ 'name' : 'order' }" v-bind:class="{ 'text-primary': $route.name === 'order' }"
                        class="relative hover:text-primary block font-medium capitalize transition">
                        <span class="absolute -left-8 top-0 text-base">
                            <i class="fa-solid fa-box-archive"></i>
                        </span>
                        订单记录
                    </RouterLink>
                </div>
                <div class="space-y-1 pl-8 pt-4">
                    <RouterLink :to="{ 'name' : 'wishlist' }" v-bind:class="{ 'text-primary': $route.name === 'wishlist' }"
                        class="relative hover:text-primary block font-medium capitalize transition">
                        <span class="absolute -left-8 top-0 text-base">
                            <i class="fa-regular fa-heart"></i>
                        </span>
                        收藏
                    </RouterLink>
                </div>

                <div class="space-y-1 pl-8 pt-4">
                    <button @click="logout" class="relative hover:text-primary block font-medium capitalize transition">
                        <span class="absolute -left-8 top-0 text-base">
                            <i class="fa-regular fa-arrow-right-from-bracket"></i>
                        </span>
                        退出登录
                    </button>
                </div>

            </div>
        </div>
        <!-- ./sidebar -->

        <RouterView />
    </div>
</template>

<script>
import { useUserStore } from '@/stores/user'
import { useWishlistStore } from '@/stores/wishlist';
import { useCartStore } from '@/stores/cart';

import Breadcrumb from '../components/Breadcrumb.vue'

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
    name: 'AccountView',
    components: {
        Breadcrumb
    },
    methods: {
        logout() {
            this.userStore.removeToken()
            this.wishlistStore.clearWishlist()
            this.cartStore.clearCart()
            this.$router.push({ name: 'login' })
        }
    }
}

</script>