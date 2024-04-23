<template>
    <div class="col-span-9 grid grid-cols-3 gap-4">

        <div class="shadow rounded bg-white px-4 pt-6 pb-8">
            <div class="flex items-center justify-between mb-4">
                <h3 class="font-medium text-gray-800 text-lg">账号信息</h3>
                <RouterLink :to="{ 'name' : 'edit_profile' }" class="text-primary">编辑</RouterLink>
            </div>
            <div class="space-y-1">
                <h4 class="text-gray-700 font-medium">{{ userStore.user.name }}</h4>
                <p class="text-gray-800">{{ userStore.user.email }}</p>
            </div>
        </div>

    </div>
</template>

<script>

import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },
}
</script>