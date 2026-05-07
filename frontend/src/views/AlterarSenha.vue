<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-4">
    <div class="bg-slate-900/90 backdrop-blur-sm border border-slate-700/50 p-8 rounded-2xl shadow-2xl w-full max-w-md mx-4 animate-fade-in">
      <div class="text-center mb-8">
        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-amber-500/25">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white">Alterar Senha</h1>
        <p class="text-slate-400 text-sm mt-1">Escolha uma senha forte e única</p>
      </div>

      <form @submit.prevent="handleAlterarSenha" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Senha Atual</label>
          <input
            v-model="senhaAtual"
            type="password"
            class="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 transition-all duration-200"
            placeholder="Sua senha atual"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Nova Senha</label>
          <input
            v-model="novaSenha"
            type="password"
            class="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 transition-all duration-200"
            placeholder="Mínimo 6 caracteres"
            required
            minlength="6"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-2">Confirmar Nova Senha</label>
          <input
            v-model="confirmacaoSenha"
            type="password"
            class="w-full px-4 py-3 bg-slate-800/50 border border-slate-600 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 transition-all duration-200"
            placeholder="Repita a nova senha"
            required
            minlength="6"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-gradient-to-r from-amber-600 to-orange-500 text-white py-3 px-4 rounded-xl font-medium hover:from-amber-500 hover:to-orange-400 focus:outline-none focus:ring-2 focus:ring-amber-500/50 transition-all duration-200 shadow-lg shadow-amber-500/25 disabled:opacity-60 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98]"
          :disabled="loading"
        >
          <span class="flex items-center justify-center gap-2">
            <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            {{ loading ? 'Alterando...' : 'Alterar Senha' }}
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const senhaAtual = ref('')
const novaSenha = ref('')
const confirmacaoSenha = ref('')
const erro = ref('')
const sucesso = ref('')
const loading = ref(false)

const handleAlterarSenha = async () => {
  erro.value = ''
  sucesso.value = ''

  if (novaSenha.value !== confirmacaoSenha.value) {
    erro.value = 'Confirmação de senha não confere'
    return
  }

  if (novaSenha.value.length < 6) {
    erro.value = 'Nova senha deve ter no mínimo 6 caracteres'
    return
  }

  if (senhaAtual.value === novaSenha.value) {
    erro.value = 'Nova senha deve ser diferente da senha atual'
    return
  }

  loading.value = true

  try {
    await api.post('/api/auth/alterar-senha', {
      senha_atual: senhaAtual.value,
      nova_senha: novaSenha.value,
      confirmacao_senha: confirmacaoSenha.value
    })
    sucesso.value = 'Senha alterada com sucesso!'
    senhaAtual.value = ''
    novaSenha.value = ''
    confirmacaoSenha.value = ''
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (error) {
    erro.value = error.response?.data?.erro || 'Erro ao alterar senha'
  } finally {
    loading.value = false
  }
}

const voltar = () => {
  router.push('/')
}
</script>
