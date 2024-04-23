<template>
    <div class="col-span-9">
        <div class="flex justify-start item-start space-y-2 flex-col">
            <h1 class="text-1xl lg:text-2xl font-semibold leading-3 lg:leading-5 text-gray-800">订单ID #{{ order.id }}
            </h1>
            <p class="text-base font-medium leading-6 text-gray-600">{{ order.created_at }}</p>
        </div>
        <div
            class="mt-10 flex flex-col xl:flex-row jusitfy-center items-stretch w-full xl:space-x-8 space-y-4 md:space-y-6 xl:space-y-0">
            <div class="flex flex-col justify-start items-start w-full space-y-4 md:space-y-6 xl:space-y-8">
                <div class="flex flex-col justify-start items-start bg-gray-50 px-4 py-4 md:py-6 md:p-6 xl:p-8 w-full">
                    <p class="text-lg md:text-xl font-semibold leading-6 xl:leading-5 text-gray-800">
                        订单商品</p>
                    <div v-for="item in order.items" v-bind:key="item.product.id"
                        class="mt-4 md:mt-6 flex flex-col md:flex-row justify-start items-start md:items-center md:space-x-6 xl:space-x-8 w-full">
                        <div class="pb-4 md:pb-8 w-full md:w-40">
                            <img class="w-full hidden md:block" :src="item.product.attachments[0].image"
                                alt="product" />
                            <img class="w-full md:hidden" :src="item.product.attachments[0].image" alt="product" />
                        </div>
                        <div
                            class="border-b border-gray-200 md:flex-row flex-col flex justify-between items-start w-full pb-8 space-y-4 md:space-y-0">
                            <div class="w-full flex flex-col justify-start items-start space-y-8">
                                <h3 class="text-xl xl:text-2xl font-semibold leading-6 text-gray-800">
                                    {{ item.product.name }}</h3>
                                <div class="flex justify-start items-start flex-col space-y-2">
                                    <p class="text-sm leading-none text-gray-800"><span class=" text-gray-300">品牌:
                                        </span>{{ item.product.brand.name }}</p>
                                    <p class="text-sm leading-none text-gray-800"><span class=" text-gray-300">类型:
                                        </span>{{ item.product.category.name }}</p>
                                </div>
                            </div>
                            <div class="flex justify-between space-x-8 items-start w-full">
                                <p class="text-base xl:text-lg leading-6">￥{{ item.price }}</p>
                                <p class="text-base xl:text-lg leading-6 text-gray-800">X {{ item.quantity }}</p>
                                <p class="text-base xl:text-lg font-semibold leading-6 text-gray-800">
                                    ￥{{ (item.price * item.quantity).toFixed(2) }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div
                    class="flex justify-center flex-col md:flex-row flex-col items-stretch w-full space-y-4 md:space-y-0 md:space-x-6 xl:space-x-8">
                    <div class="flex flex-col px-4 py-6 md:p-6 xl:p-8 w-full bg-gray-50 space-y-6">
                        <h3 class="text-xl font-semibold leading-5 text-gray-800">订单总价</h3>
                        <div
                            class="flex justify-center items-center w-full space-y-4 flex-col border-gray-200 border-b pb-4">
                            <div class="flex justify-between w-full">
                                <p class="text-base leading-4 text-gray-800">小计</p>
                                <p class="text-base leading-4 text-gray-600">￥{{ order.sub_total }}</p>
                            </div>
                            <div class="flex justify-between items-center w-full">
                                <p class="text-base leading-4 text-gray-800">运费</p>
                                <p class="text-base leading-4 text-gray-600">￥{{ order.shipping }}</p>
                            </div>
                        </div>
                        <div class="flex justify-between items-center w-full">
                            <p class="text-base font-semibold leading-4 text-gray-800">合计</p>
                            <p class="text-base font-semibold leading-4 text-gray-600">￥{{ order.total }}</p>
                        </div>
                    </div>
                    <div class="flex flex-col justify-center px-4 py-6 md:p-6 xl:p-8 w-full bg-gray-50 space-y-6">
                        <h3 class="text-xl font-semibold leading-5 text-gray-800">{{ order.status }}</h3>
                        <div class="flex justify-between items-start w-full">
                            <div class="flex justify-center items-center space-x-4">
                                <div class="flex flex-col justify-start items-center">
                                    <p class="text-lg leading-6 font-semibold text-gray-800">XYZ物流<br /><span
                                            class="font-normal" v-if="order.status !== '已取消'">预计明天送达</span></p>
                                </div>
                            </div>
                            <p class="text-lg font-semibold leading-6 text-gray-800">￥{{ order.shipping }}</p>
                        </div>
                        <div class="w-full flex justify-center items-center">
                            <button
                                class="hover:bg-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-800 py-5 w-96 md:w-full bg-gray-800 text-base font-medium leading-4 text-white">物流详情</button>
                        </div>
                    </div>
                </div>
            </div>
            <div
                class="bg-gray-50 w-full xl:w-96 flex justify-between items-center md:items-start px-4 py-6 md:p-6 xl:p-8 flex-col">
                <h3 class="text-xl font-semibold leading-5 text-gray-800">收货人</h3>
                <div
                    class="flex flex-col md:flex-row xl:flex-col justify-start items-stretch h-full w-full md:space-x-6 lg:space-x-8 xl:space-x-0">
                    <div class="flex flex-col justify-start items-start flex-shrink-0">
                        <div
                            class="flex justify-center w-full md:justify-start items-center space-x-4 py-8 border-b border-gray-200">
                            <div class="flex justify-start items-start flex-col space-y-2">
                                <p class="text-base font-semibold leading-4 text-left text-gray-800">
                                    {{ order.receiver }}</p>
                                <p class="text-sm leading-5 text-gray-600">{{ order.phone }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="flex justify-between xl:h-full items-stretch w-full flex-col mt-6 md:mt-0">
                        <div
                            class="flex justify-center md:justify-start xl:flex-col flex-col md:space-x-6 lg:space-x-8 xl:space-x-0 space-y-4 xl:space-y-12 md:space-y-0 md:flex-row items-center md:items-start">
                            <div
                                class="flex justify-center md:justify-start items-center md:items-start flex-col space-y-4 xl:mt-8">
                                <p class="text-base font-semibold leading-4 text-center md:text-left text-gray-800">
                                    收获地址</p>
                                <p
                                    class="w-48 lg:w-full xl:w-48 text-center md:text-left text-sm leading-5 text-gray-600">
                                    {{ order.country }}, {{ order.province }}, {{ order.city }} {{ order.street
                                    }}</p>
                            </div>
                        </div>
                        <div class="flex w-full justify-center items-center md:justify-start md:items-start">
                            <button @click="cancelOrder" v-if="order.status !== '已取消'"
                                class="mt-6 md:mt-0 py-5 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-800 border border-gray-800 font-medium w-96 2xl:w-full text-base font-medium leading-4 text-gray-800">取消订单</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    name: 'OrderDetail',
    data() {
        return {
            order: {}
        }
    },
    mounted() {
        this.getOrder()
    },
    methods: {
        getOrder() {
            axios.get(`/api/accounts/orders/${this.$route.params.id}`)
                .then(response => { this.order = response.data })
        },
        cancelOrder() {
            axios.put(`/api/accounts/order_cancel/${this.$route.params.id}`)
                .then(() => { this.$router.push({ name: 'order' }) })
        }
    }
}
</script>