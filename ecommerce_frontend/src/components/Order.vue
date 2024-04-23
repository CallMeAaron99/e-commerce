<template>
    <div class="col-span-9 flex flex-wrap">
        <div class="flex-auto block py-8 pt-6 px-9">
            <div class="overflow-x-auto">
                <table class="w-full my-0 align-middle text-dark border-neutral-200">
                    <thead class="align-bottom">
                        <tr class="font-semibold text-[0.95rem] text-secondary-dark">
                            <th class="pb-3 text-start min-w-[175px]">订单商品</th>
                            <th class="pb-3 min-w-[100px]">收货人</th>
                            <th class="pb-3 min-w-[175px]">收货地址</th>
                            <th class="pb-3 min-w-[100px]">状态</th>
                            <th class="pb-3 min-w-[175px]">下单时间</th>
                            <th class="pb-3 text-end min-w-[50px]">详情</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b border-dashed last:border-b-0" v-for="order in orders"
                            v-bind:key="order.id">
                            <td class="p-3 pl-0" v-if="order.items[0]">
                                <div class="flex items-center">
                                    <div class="relative inline-block shrink-0 me-3">
                                        <img :src="order.items[0].product.attachments[0].image"
                                            class="w-[50px] h-[50px] inline-block shrink-0" alt="">
                                    </div>
                                    <div class="flex flex-col justify-start">
                                        <RouterLink :to="{ name: 'order_detail', params: { id: order.id } }"
                                            class="mb-1 font-semibold transition-colors duration-200 ease-in-out text-lg/normal text-secondary-inverse hover:text-primary">
                                            {{
                            order.items[0].product.name }}</RouterLink>
                                    </div>
                                </div>
                            </td>
                            <td class="p-3 pr-2 text-center">
                                <span class="font-semibold text-light-inverse text-md/normal">{{ order.receiver
                                    }}</span>
                            </td>
                            <td class="p-3 pr-0">
                                <span
                                    class="truncate text-center align-baseline inline-flex px-2 py-1 mr-auto items-center font-semibold text-base/none text-success bg-success-light rounded-lg">
                                    {{ order.country }}, {{ order.province }}, {{ order.city }} {{ order.street
                                    }}</span>
                            </td>
                            <td class="p-3 pr-0">
                                <span
                                    class="text-center align-baseline inline-flex px-4 py-3 mr-auto items-center font-semibold text-[.95rem] leading-none text-primary bg-primary-light rounded-lg">
                                    {{ order.status }}</span>
                            </td>
                            <td class="p-3 pr-0">
                                <span class="font-semibold text-light-inverse text-md/normal">{{ order.created_at
                                    }}</span>
                            </td>
                            <td class="p-3 pr-0 text-end">
                                <RouterLink :to="{ name: 'order_detail', params: { id: order.id } }"
                                    class="ml-auto relative text-secondary-dark bg-light-dark hover:text-primary flex items-center h-[25px] w-[25px] text-base font-medium leading-normal text-center align-middle cursor-pointer rounded-2xl transition-colors duration-200 ease-in-out shadow-none border-0 justify-center">
                                    <span class="flex items-center justify-center p-0 m-0 leading-none shrink-0 ">
                                        <i class="fa-solid fa-chevron-right"></i>
                                    </span>
                                </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Order',
    data() {
        return {
            orders: []
        }
    },
    mounted() {
        this.getOrders()
    },
    methods: {
        getOrders() {
            axios.get('/api/accounts/orders')
                .then(response => { this.orders = response.data })
        }
    }
}
</script>