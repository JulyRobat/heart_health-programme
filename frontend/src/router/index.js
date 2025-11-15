import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/chat'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/Chat.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/emotion',
      name: 'emotion',
      component: () => import('@/views/Emotion.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/knowledge',
      name: 'knowledge',
      component: () => import('@/views/Knowledge.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/emergency',
      name: 'emergency',
      component: () => import('@/views/Emergency.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/chat')
  } else {
    next()
  }
})

export default router