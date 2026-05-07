import axios from 'axios'

// Sem baseURL para usar o proxy do Vite
const api = axios.create({})

// Função para definir/remover token no header global
export function setAuthHeader(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    console.log('✅ Token definido no header')
  } else {
    delete api.defaults.headers.common['Authorization']
    console.log('ℹ️ Token removido do header')
  }
}

// Interceptor de resposta: trata erro 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error('❌ Erro 401:', error.config.url)
    }
    return Promise.reject(error)
  }
)

export default api
