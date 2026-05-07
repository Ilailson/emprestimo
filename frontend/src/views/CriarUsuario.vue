<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4">
    <div class="bg-slate-900/90 backdrop-blur-sm border border-slate-700/50 p-8 rounded-2xl shadow-2xl w-full max-w-md mx-4 animate-fade-in">
      <div class="text-center mb-8">
        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-violet-500/25">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white">Criar Usuário</h1>
        <p class="text-slate-400 text-sm mt-1">Apenas administradores podem criar usuários</p>
      </div>

      <form @submit.prevent="handleCriarUsuario" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Nome</label>
          <input
            v-model="nome"
            type="text"
            class="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 transition-all duration-200"
            placeholder="Nome completo"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Login</label>
          <input
            v-model="login"
            type="text"
            class="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 transition-all duration-200"
            placeholder="Nome de usuário"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Senha</label>
          <input
            v-model="senha"
            type="password"
            class="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 transition-all duration-200"
            placeholder="Mínimo 6 caracteres"
            required
            minlength="6"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Tipo de Acesso</label>
          <select
            v-model="role"
            class="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white focus:outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 transition-all duration-200"
          >
            <option value="user">Usuário</option>
            <option value="admin">Administrador</option>
          </select>
        </div>

        <button
          type="submit"
          class="w-full bg-gradient-to-r from-violet-600 to-purple-500 text-white py-3 px-4 rounded-xl font-medium hover:from-violet-500 hover:to-purple-400 focus:outline-none focus:ring-2 focus:ring-violet-500/50 transition-all duration-200 shadow-lg shadow-violet-500/25 disabled:opacity-60 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98]"
          :disabled="loading"
        >
          <span class="flex items-center justify-center gap-2">
            <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            {{ loading ? 'Criando...' : 'Criar Usuário' }}
          </span>
        </button>

        <div v-if="erro" class="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
          <p class="text-red-400 text-sm text-center">{{ erro }}</p>
        </div>

        <div v-if="sucesso" class="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
          <p class="text-emerald-400 text-sm text-center">{{ sucesso }}</p>
        </div>
      </form>

      <div class="mt-6 text-center">
        <button @click="voltar" class="text-slate-500 hover:text-slate-300 text-sm transition-colors duration-200">
          ← Voltar ao painel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()
const nome = ref('')
const login = ref('')
const senha = ref('')
const role = ref('user')
const erro = ref('')
const sucesso = ref('')
const loading = ref(false)

onMounted(() => {
  if (!authStore.isAdmin) {
    router.push('/')
  }
})

const handleCriarUsuario = async () => {
  erro.value = ''
  sucesso.value = ''

  if (senha.value.length < 6) {
    erro.value = 'Senha deve ter no mínimo 6 caracteres'
    return
  }

  loading.value = true

  try {
    const response = await api.post('/api/auth/usuarios', {
      nome: nome.value,
      login: login.value,
      senha: senha.value,
      role: role.value
    })
    sucesso.value = `Usuário "${response.data.usuario.login}" criado com sucesso!`
    nome.value = ''
    login.value = ''
    senha.value = ''
    role.value = 'user'
  } catch (error) {
    erro.value = error.response?.data?.erro || 'Erro ao criar usuário'
  } finally {
    loading.value = false
  }
}

const voltar = () => {
  router.push('/')
}
</script>
