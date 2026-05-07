import { defineStore } from 'pinia'
import api, { setAuthHeader } from '@/services/api'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false
  }),

  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/api/auth/login', credentials)
        this.accessToken = response.data.access_token
        this.refreshToken = response.data.refresh_token
        this.user = response.data.user
        this.isAuthenticated = true
        // Define o token no header
        setAuthHeader(response.data.access_token)
        console.log('✅ Login realizado, token definido')
        return response.data
      } catch (error) {
        console.error('❌ Erro no login:', error)
        throw error
      }
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      this.isAuthenticated = false
      // Remove o token do header
      setAuthHeader(null)
      console.log('ℹ️ Logout realizado')
      // Usa o router para redirecionar
      const router = useRouter()
      if (router) {
        router.push('/login')
      }
    },

    async refreshAccessToken() {
      try {
        const response = await api.post('/api/auth/refresh', {}, {
          headers: { Authorization: `Bearer ${this.refreshToken}` }
        })
        this.accessToken = response.data.access_token
        // Atualiza o token no header
        setAuthHeader(response.data.access_token)
        return this.accessToken
      } catch (error) {
        this.logout()
        throw error
      }
    }
  },

  getters: {
    isAdmin: (state) => state.user?.role === 'admin'
  }
})
