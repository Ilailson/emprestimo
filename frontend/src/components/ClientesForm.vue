<template>
  <div class="max-w-2xl mx-auto space-y-4">
    <div class="flex items-center gap-3">
      <button @click="$emit('cancelar')" class="p-2 -ml-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
      </button>
      <h1 class="text-xl font-bold text-white">{{ editando ? 'Editar Cliente' : 'Novo Cliente' }}</h1>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-6">
      <form @submit.prevent="salvar" class="space-y-4">
        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Nome Completo</label>
          <input v-model="form.nome" required placeholder="Digite o nome completo" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all min-h-[48px]">
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Telefone</label>
          <input v-model="form.telefone" required placeholder="(91) 00000-0000" @input="formatarTelefone" maxlength="14" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all min-h-[48px]">
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Endereço</label>
          <input v-model="form.endereco" placeholder="Endereço completo (opcional)" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all min-h-[48px]">
        </div>

        <div class="flex flex-col sm:flex-row gap-3 pt-2">
          <button v-if="!editando" type="button" @click="salvarComEmprestimo" class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-all font-medium shadow-lg shadow-blue-500/25 min-h-[48px]">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            Cadastrar e criar Empréstimo
          </button>
          <button v-if="editando" type="submit" class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-all font-medium shadow-lg shadow-blue-500/25 min-h-[48px]">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            Atualizar
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
  name: 'ClientesForm',
  props: {
    cliente: { type: Object, default: null }
  },
  emits: ['salvo', 'cancelar', 'criadoComEmprestimo'],
  data() {
    return {
      form: {
        nome: '',
        telefone: '',
        endereco: ''
      }
    }
  },
  computed: {
    editando() {
      return this.cliente !== null
    }
  },
  watch: {
    cliente: {
      immediate: true,
      handler(novo) {
        if (novo) {
          this.form = { nome: novo.nome, telefone: novo.telefone, endereco: novo.endereco }
        } else {
          this.form = { nome: '', telefone: '91', endereco: '' }
        }
      }
    }
  },
  methods: {
    formatarTelefone() {
      let tel = this.form.telefone.replace(/\D/g, '')
      if (tel.length > 2) {
        tel = '(' + tel.substring(0, 2) + ')' + tel.substring(2)
      }
      if (tel.length > 9) {
        tel = tel.substring(0, 9) + '-' + tel.substring(9, 13)
      }
      this.form.telefone = tel
    },
    async salvar() {
      try {
        if (this.editando) {
          await api.put(`/api/clientes/${this.cliente.id}`, this.form)
        } else {
          await api.post('/api/clientes', this.form)
        }
        this.$emit('salvo')
        this.limpar()
      } catch (err) {
        alert(err.response?.data?.erro || 'Erro ao salvar')
      }
    },
    limpar() {
      this.form = { nome: '', telefone: '', endereco: '' }
    },
    async salvarComEmprestimo() {
      try {
        const resp = await api.post('/api/clientes', this.form)
        this.$emit('criadoComEmprestimo', resp.data)
        this.limpar()
      } catch (err) {
        alert(err.response?.data?.erro || 'Erro ao salvar')
      }
    }
  }
}
</script>
