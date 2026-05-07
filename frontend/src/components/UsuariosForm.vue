<template>
  <div class="max-w-2xl mx-auto space-y-4">
    <div class="flex items-center gap-3">
      <button @click="$emit('cancelar')" class="p-2 -ml-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
      </button>
      <h1 class="text-xl font-bold text-white">{{ editando ? 'Editar Usuário' : 'Novo Usuário' }}</h1>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-6">
      <form @submit.prevent="salvar" class="space-y-4">
        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Nome</label>
          <input v-model="form.nome" required placeholder="Nome completo" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all min-h-[48px]">
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Login</label>
          <input v-model="form.login" required placeholder="Nome de usuário" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all min-h-[48px]">
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">
            Senha
            <span v-if="editando" class="text-slate-500 font-normal">(deixe em branco para manter)</span>
          </label>
          <input v-model="form.senha" type="password" :required="!editando" :minlength="editando ? 0 : 6" placeholder="Mínimo 6 caracteres" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all min-h-[48px]">
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Tipo de Acesso</label>
          <select v-model="form.role" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all min-h-[48px]">
            <option value="user">Usuário</option>
            <option value="admin">Administrador</option>
          </select>
        </div>

        <div v-if="erro" class="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
          <p class="text-red-400 text-sm">{{ erro }}</p>
        </div>

        <div class="flex flex-col sm:flex-row gap-3 pt-2">
          <button type="submit" class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 bg-violet-600 hover:bg-violet-500 text-white rounded-lg transition-all font-medium shadow-lg shadow-violet-500/25 min-h-[48px]">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            {{ editando ? 'Atualizar' : 'Criar Usuário' }}
          </button>
          <button type="button" @click="$emit('cancelar')" class="flex-1 px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-all border border-slate-700 min-h-[48px]">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'UsuariosForm',
  props: {
    usuario: { type: Object, default: null }
  },
  emits: ['salvo', 'cancelar'],
  data() {
    return {
      form: {
        nome: '',
        login: '',
        senha: '',
        role: 'user'
      },
      erro: ''
    }
  },
  computed: {
    editando() {
      return this.usuario !== null
    }
  },
  watch: {
    usuario: {
      immediate: true,
      handler(novo) {
        if (novo) {
          this.form = { nome: novo.nome, login: novo.login, senha: '', role: novo.role }
        } else {
          this.form = { nome: '', login: '', senha: '', role: 'user' }
        }
        this.erro = ''
      }
    }
  },
  methods: {
    async salvar() {
      this.erro = ''

      if (this.form.senha && this.form.senha.length < 6) {
        this.erro = 'Senha deve ter no mínimo 6 caracteres'
        return
      }

      try {
        if (this.editando) {
          await api.put(`/api/auth/usuarios/${this.usuario.id}`, this.form)
        } else {
          await api.post('/api/auth/usuarios', this.form)
        }
        this.$emit('salvo')
        this.limpar()
      } catch (err) {
        this.erro = err.response?.data?.erro || 'Erro ao salvar'
      }
    },
    limpar() {
      this.form = { nome: '', login: '', senha: '', role: 'user' }
      this.erro = ''
    }
  }
}
</script>
