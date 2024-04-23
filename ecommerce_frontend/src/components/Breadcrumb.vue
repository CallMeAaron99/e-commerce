<template>
    <div class="container mx-auto py-4 flex items-center gap-3">
        <RouterLink :to="{ 'name': 'home' }" class="text-primary text-base">
            <i class="fa-solid fa-house"></i>
        </RouterLink>

        <template v-for="(breadcrumb, index) in breadcrumbList" :key="index">
            <span class="text-sm text-gray-400">
                <i class="fa-solid fa-chevron-right"></i>
            </span>
            <button @click="routeTo(index)" class="text-gray-600 font-medium hover:text-primary transition">{{
            breadcrumb.name }}</button>
        </template>

    </div>
</template>

<script>
export default {
    data() {
        return {
            breadcrumbList: []
        }
    },
    mounted() {
        this.updateList()
    },
    watch: {
        '$route'() {
            this.updateList()
        }
    },
    methods: {
        routeTo(index) {
            if (this.breadcrumbList[index].link) {
                this.$router.push({ name: this.breadcrumbList[index].link })
            }
        },
        updateList() {
            if (this.$route.meta.breadcrumb)
                this.breadcrumbList = this.$route.meta.breadcrumb
        }
    }
}
</script>