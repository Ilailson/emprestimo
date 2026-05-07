import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/alterar-senha',
    name: 'AlterarSenha',
    component: () => import('@/views/AlterarSenha.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/MainLayout.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // Importação dinâmica para evitar dependência circular
  import('@/store/auth').then(module => {
    const authStore = module.useAuthStore()
    
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      next('/login')
    } else {
      next()
    }
  }).catch(() => {
    next('/login')
  })
})

export default router
