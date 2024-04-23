import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user';
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/sign-up',
      name: 'sign_up',
      component: () => import('../views/SignupView.vue')
    },
    , {
      path: '/reset_password',
      name: 'reset_password',
      component: () => import('../views/ResetPasswordView.vue'),
    }, {
      path: '/reset_password_done',
      name: 'reset_password_done',
      component: () => import('../views/ResetPasswordDoneView.vue'),
    }, {
      path: '/account',
      name: 'account',
      component: () => import('../views/AccountView.vue'),
      meta: {
        requiresAuth: true,
        breadcrumb: [
          { name: '账号管理' }
        ]
      },
      children: [{
        path: 'account-info',
        name: 'account_info',
        component: () => import('../components/AccountInfo.vue'),
      }, {
        path: 'edit-profile',
        name: 'edit_profile',
        component: () => import('../components/EditProfile.vue'),
      }, {
        path: 'address-list',
        name: 'address_list',
        component: () => import('../components/AddressList.vue'),
      }, {
        path: 'edit-password',
        name: 'edit_password',
        component: () => import('../components/EditPassword.vue'),
      }, {
        path: 'order',
        name: 'order',
        component: () => import('../components/Order.vue'),
      }, {
        path: 'wishlist',
        name: 'wishlist',
        component: () => import('../components/Wishlist.vue'),
      }, {
        path: '/address-edit/:id',
        name: 'address_edit',
        component: () => import('../components/AddressEditView.vue'),
        meta: {
          requiresAuth: true
        }
      }, {
        path: '/order/:id',
        name: 'order_detail',
        component: () => import('../components/OrderDetail.vue'),
      },]
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('../views/CheckoutView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/product/:id',
      name: 'product',
      component: () => import('../views/ProductView.vue'),
      meta: {
        breadcrumb: [
          { name: '商城', link: 'shop' },
          { name: '商品详情' }
        ]
      },
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/CartView.vue')
    },
    {
      path: '/shop',
      name: 'shop',
      component: () => import('../views/ShopView.vue'),
      meta: {
        breadcrumb: [
          { name: '商城' }
        ]
      },
    },
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.matched.some(record => record.meta.requiresAuth) && !userStore.user.isAuthenticated) {
    // Redirect to login page
    next({ name: 'login', query: { to: to.href } })
  } else {
    next()
  }
})

export default router
