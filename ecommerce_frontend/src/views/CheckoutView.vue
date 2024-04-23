<template>
    <Breadcrumb />

    <div class="container mx-auto">

        <div class="w-full bg-white border-t border-b border-gray-200 px-5 py-10 text-gray-800">
            <div class="w-full">
                <div class="-mx-3 md:flex items-start">
                    <div class="px-3 md:w-7/12 lg:pr-10">
                        <div class="w-full mx-auto text-gray-800 font-light mb-6 border-b border-gray-200 pb-6">

                            <div class="w-full flex items-center mb-3" v-for="item in cartStore.cart.items"
                                v-bind:key="item.id">
                                <div class="overflow-hidden rounded-lg size-16 bg-gray-50 border border-gray-200">
                                    <img :src="item.product.attachments[0].image" alt="">
                                </div>
                                <div class="flex-grow pl-3">
                                    <h6 class="font-semibold uppercase text-gray-600">{{ item.product.name }}</h6>
                                    <p class="text-gray-400">x {{ item.quantity }}</p>
                                </div>
                                <div>
                                    <span class="font-semibold text-gray-600 text-xl">￥{{ (item.product.price *
                                item.quantity).toFixed(2) }}</span>
                                </div>
                            </div>

                        </div>
                        <div class="mb-6 pb-6 border-b border-gray-200 text-gray-800">
                            <div class="w-full flex mb-3 items-center">
                                <div class="flex-grow">
                                    <span class="text-gray-600">小计</span>
                                </div>
                                <div class="pl-3">
                                    <span class="font-semibold">￥{{ (cartStore.cart.cartTotalPrice).toFixed(2) }}</span>
                                </div>
                            </div>
                            <div class="w-full flex items-center">
                                <div class="flex-grow">
                                    <span class="text-gray-600">运费</span>
                                </div>
                                <div class="pl-3">
                                    <span class="font-semibold">￥{{ order.shipping }}</span>
                                </div>
                            </div>
                        </div>
                        <div class="mb-6 pb-6 border-b border-gray-200 md:border-none text-gray-800 text-xl">
                            <div class="w-full flex items-center">
                                <div class="flex-grow">
                                    <span class="text-gray-600">合计</span>
                                </div>
                                <div class="pl-3">
                                    <span class="font-semibold">￥{{ (cartStore.cart.cartTotalPrice + order.shipping).toFixed(2)
                                        }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="px-3 md:w-5/12">
                        <div class="relative mb-6">
                            <div
                                class="flex flex-col items-center w-full mx-auto rounded-lg bg-white border border-gray-200 p-3 text-gray-800 font-light mb-2">
                                <template v-if="deliveryAddress">
                                    <div class="w-full flex mb-3 items-center">
                                        <div class="w-32">
                                            <span class="text-gray-600 font-semibold">收货人</span>
                                        </div>
                                        <div class="flex-grow pl-3 space-x-3">
                                            <span>{{ deliveryAddress.receiver }}</span>
                                            <span>{{ deliveryAddress.phone }}</span>
                                        </div>
                                    </div>
                                    <div class="w-full flex items-center">
                                        <div class="w-32">
                                            <span class="text-gray-600 font-semibold">收货地址</span>
                                        </div>
                                        <div class="flex-grow pl-3">
                                            <span class="truncate">{{ deliveryAddress.country }}, {{
                                deliveryAddress.province }}, {{ deliveryAddress.city }} {{
                                deliveryAddress.street }}</span>
                                        </div>
                                    </div>
                                </template>
                                <h4 v-else for="select" class="font-semibold py-2">选择一个收获地址</h4>
                                <button for="showMore" @click="showMore = !showMore"
                                    class="cursor-pointer outline-none focus:outline-none transition-all text-gray-300 hover:text-gray-600">
                                    <i class="fa-solid fa-caret-down"></i>
                                </button>
                            </div>
                            <div class="absolute overflow-hidden flex-col w-full rounded-lg bg-slate-100 border border-black p-2"
                                v-bind:class="showMore ? 'flex' : 'hidden'">
                                <div v-for="(address, index) in addresses" v-bind:key="address.id"
                                    @click="setAddress(index)"
                                    class="cursor-pointer w-full mx-auto rounded-lg bg-white border border-gray-200 p-3 text-gray-800 font-light group transition hover:bg-slate-300 mb-2">
                                    <div class="w-full flex mb-3 items-center">
                                        <div class="w-32">
                                            <span class="text-gray-600 font-semibold">收货人</span>
                                        </div>
                                        <div class="flex-grow pl-3 space-x-3">
                                            <span>{{ address.receiver }}</span>
                                            <span>{{ address.phone }}</span>
                                        </div>
                                    </div>
                                    <div class="w-full flex items-center">
                                        <div class="w-32">
                                            <span class="text-gray-600 font-semibold">收货地址</span>
                                        </div>
                                        <div class="flex-grow pl-3">
                                            <span class="truncate">{{ address.country }}, {{
                                address.province }}, {{ address.city }} {{
                                address.street }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div
                            class="w-full mx-auto rounded-lg bg-white border border-gray-200 text-gray-800 font-light mb-6">
                            <div class="w-full p-3 border-b border-gray-200">
                                <label for="type1" class="flex items-center cursor-pointer">
                                    <input type="radio" class="form-radio h-5 w-5 text-indigo-500" name="type"
                                        id="type1" value="1" v-model="order.payment_type" checked>
                                    <span class="ms-2 text-gray-600 font-semibold">信用卡 / 储蓄卡</span>
                                </label>
                                <div class="mt-5" v-show="order.payment_type === '1'">
                                    <div class="mb-3">
                                        <label class="text-gray-600 font-semibold text-sm mb-2 ml-1">持卡人姓名</label>
                                        <div>
                                            <input
                                                class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors"
                                                placeholder="张三" type="text" />
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <label class="text-gray-600 font-semibold text-sm mb-2 ml-1">卡号</label>
                                        <div>
                                            <input :value="formatCardNumber" @input="updateValue"
                                                class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors"
                                                placeholder="0000 0000 0000 0000" type="text" maxlength="19" />
                                        </div>
                                    </div>
                                    <div class="mb-3 -mx-2 flex items-end">
                                        <div class="px-2 w-1/4">
                                            <label class="text-gray-600 font-semibold text-sm mb-2 ml-1">卡有效期</label>
                                            <div>
                                                <select
                                                    class="form-select w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors cursor-pointer">
                                                    <option value="01">01 - 一月</option>
                                                    <option value="02">02 - 二月</option>
                                                    <option value="03">03 - 三月</option>
                                                    <option value="04">04 - 四月</option>
                                                    <option value="05">05 - 五月</option>
                                                    <option value="06">06 - 六月</option>
                                                    <option value="07">07 - 七月</option>
                                                    <option value="08">08 - 八月</option>
                                                    <option value="09">09 - 九月</option>
                                                    <option value="10">10 - 十月</option>
                                                    <option value="11">11 - 十一月</option>
                                                    <option value="12">12 - 十二月</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div class="px-2 w-1/4">
                                            <select
                                                class="form-select w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors cursor-pointer">
                                                <option value="2023">2023</option>
                                                <option value="2024">2024</option>
                                                <option value="2025">2025</option>
                                                <option value="2026">2026</option>
                                                <option value="2027">2027</option>
                                                <option value="2028">2028</option>
                                                <option value="2029">2029</option>
                                                <option value="2030">2030</option>
                                                <option value="2031">2031</option>
                                                <option value="2032">2032</option>
                                            </select>
                                        </div>
                                        <div class="px-2 w-1/4">
                                            <label class="text-gray-600 font-semibold text-sm mb-2 ml-1">CVV</label>
                                            <div>
                                                <input
                                                    class="w-full px-3 py-2 mb-1 border border-gray-200 rounded-md focus:outline-none focus:border-indigo-500 transition-colors"
                                                    placeholder="000" type="text" maxlength="3" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="w-full p-3">
                                <label for="type2" class="flex items-center cursor-pointer">
                                    <input type="radio" class="form-radio h-5 w-5 text-indigo-500" name="type"
                                        id="type2" value="2" v-model="order.payment_type">
                                    <span class="ms-2 text-gray-600 font-semibold">货到付款</span>
                                </label>
                            </div>
                        </div>
                        <div>
                            <button @click="checkout"
                                class="block w-full max-w-xs mx-auto bg-indigo-500 hover:bg-indigo-700 focus:bg-indigo-700 text-white rounded-lg px-3 py-2 font-semibold"><i
                                    class="mdi mdi-lock-outline mr-1"></i>确定支付</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useCartStore } from '../stores/cart'
import { useWishlistStore } from '../stores/wishlist'
import Breadcrumb from '../components/Breadcrumb.vue'

export default {
    name: 'CheckoutView',
    components: {
        Breadcrumb
    },
    setup() {
        const cartStore = useCartStore()
        const wishlistStore = useWishlistStore()

        return {
            cartStore,
            wishlistStore
        }
    },
    data() {
        return {
            order: {
                shipping: 4.99,
                payment_type: '1',
                address: '',
            },
            addresses: [],
            deliveryAddress: {},
            card: {
                name: '',
                cardNumber: '',
                year: '',
                month: '',
                cvv: ''
            },
            showMore: false
        }
    },
    mounted() {
        this.getAddresses()
    },
    methods: {
        checkout() {
            this.order.address = this.deliveryAddress.id
            this.order.payment_type = parseInt(this.order.payment_type)

            axios.post('/api/accounts/checkout', this.order)
                .then(response => {
                    this.cartStore.clearCart()
                    this.wishlistStore.initStore()
                    this.$router.push({ name: 'order' })
                })
        },
        getAddresses() {
            axios.get('/api/accounts/addresses')
                .then(response => {
                    this.addresses = response.data
                    this.deliveryAddress = this.addresses.find(address => address.is_default)
                })
        },
        setAddress(index) {
            this.deliveryAddress = this.addresses[index]
            this.showMore = false
        },
        updateValue(e) {
            this.card.cardNumber = e.target.value.replace(/\s/g, '');
        }
    },
    computed: {
        formatCardNumber() {
            return this.card.cardNumber ? this.card.cardNumber.match(/.{1,4}/g).join(' ') : '';
        }
    }
}

</script>