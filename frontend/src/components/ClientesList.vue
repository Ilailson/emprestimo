<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <h1 class="text-xl sm:text-2xl font-bold text-white">Clientes</h1>
      <button @click="$emit('novo')" class="hidden md:inline-flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-all duration-200 font-medium shadow-lg shadow-blue-500/25 min-h-[44px]">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
        </svg>
        <span class="sm:inline">Novo Cliente</span>
      </button>
    </div>

    <!-- Botão flutuante mobile -->
    <button @click="$emit('novo')" class="md:hidden fixed bottom-6 right-6 w-14 h-14 bg-blue-600 hover:bg-blue-500 text-white rounded-full shadow-lg shadow-blue-500/50 flex items-center justify-center z-40">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
      </svg>
    </button>

    <!-- Busca -->
    <div class="relative">
      <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
      <input
        v-model="busca"
        @input="onInputBusca"
        type="text"
        placeholder="Buscar cliente..."
        class="w-full pl-10 pr-10 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all min-h-[44px]"
      />
      <button v-if="busca" @click="limparBusca" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white p-1">
        <X class="w-5 h-5" />
      </button>
    </div>

    <!-- Mensagem -->
    <div v-if="mensagem" :class="['p-4 rounded-lg text-sm flex items-center gap-3', mensagem_tipo === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20']">
      <svg v-if="mensagem_tipo === 'error'" class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <svg v-else class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <span class="break-words">{{ mensagem }}</span>
    </div>

    <!-- Desktop: Tabela -->
    <div class="hidden md:block bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-slate-800 bg-slate-800/50">
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Nome</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Telefone</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Endereço</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800">
             <tr v-for="cliente in clientes" :key="cliente.id" class="hover:bg-slate-800/50 transition-colors">
               <td class="px-3 py-3">
                 <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 font-semibold text-xs">
                      {{ cliente.nome.charAt(0).toUpperCase() }}
                    </div>
                    <span class="text-white font-medium">{{ cliente.nome }}</span>
                 </div>
               </td>
                <td class="px-3 py-3 text-slate-300">{{ formatarTelefone(cliente.telefone) }}</td>
                <td class="px-3 py-3 text-slate-400">{{ cliente.endereco || '-' }}</td>
               <td class="px-3 py-3">
                <div class="flex items-center gap-1">
                    <button @click="$emit('verEmprestimos', cliente)" class="p-1.5 text-emerald-400 hover:text-emerald-300 hover:bg-emerald-500/10 rounded-lg transition-all" title="Empréstimos">
                     <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                       <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                     </svg>
                   </button>
                    <button @click="$emit('editar', cliente)" class="p-1.5 text-slate-400 hover:text-blue-400 hover:bg-blue-500/10 rounded-lg transition-all" title="Editar">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                    </svg>
                  </button>
                   <button @click="abrirModalExcluir(cliente.id)" class="p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all" title="Excluir">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Mobile: Cards -->
    <div class="md:hidden space-y-3">
      <div v-for="cliente in clientes" :key="cliente.id" class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex items-start gap-3">
          <div class="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 font-semibold flex-shrink-0">
            {{ cliente.nome.charAt(0).toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-white font-medium truncate">{{ cliente.nome }}</h3>
            <p class="text-slate-400 text-sm">{{ formatarTelefone(cliente.telefone) }}</p>
            <p class="text-slate-500 text-sm truncate">{{ cliente.endereco || '-' }}</p>
          </div>
        </div>
        <div class="flex flex-wrap gap-2 mt-3 pt-3 border-t border-slate-800">
          <button @click="$emit('verEmprestimos', cliente)" class="flex-1 min-w-[100px] inline-flex items-center justify-center gap-1.5 px-3 py-2.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 rounded-lg transition-all text-sm font-medium border border-emerald-500/30 transform hover:scale-[1.02] active:scale-[0.98]">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
            Empréstimo
          </button>
          <button @click="$emit('editar', cliente)" class="p-2.5 text-slate-400 hover:text-blue-400 hover:bg-blue-500/10 rounded-lg transition-all transform hover:scale-110 active:scale-95" title="Editar">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
            </svg>
          </button>
          <button @click="abrirModalExcluir(cliente.id)" class="p-2.5 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all transform hover:scale-110 active:scale-95" title="Excluir">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="clientes.length === 0" class="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
      <svg class="w-12 h-12 mx-auto text-slate-600 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.357-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.357-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
      </svg>
      <p class="text-slate-500">Nenhum cliente cadastrado</p>
      <p class="text-slate-600 text-sm mt-1">Clique em "Novo Cliente" para começar</p>
    </div>

    <!-- Modal de Confirmação -->
    <div v-if="mostrarModalExcluir" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="fecharModalExcluir"></div>
      <div class="relative bg-slate-800 border border-slate-700 rounded-xl p-6 w-full max-w-md shadow-2xl">
        <div class="text-center">
          <div class="w-12 h-12 rounded-full bg-red-500/20 flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-white mb-2">Tem certeza absoluta?</h3>
          <p class="text-slate-400 mb-6">Essa ação não pode ser desfeita. Isso excluirá permanentemente os dados do nosso servidor.</p>
          <div class="flex gap-3 justify-center">
            <button @click="fecharModalExcluir" class="px-6 py-3 text-slate-300 hover:text-white hover:bg-slate-700 rounded-lg transition-all font-medium min-h-[44px]">
              Cancelar
            </button>
            <button @click="confirmarExcluir" class="px-6 py-3 bg-red-600 hover:bg-red-500 text-white rounded-lg transition-all font-medium min-h-[44px]">
              Continuar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { Search, X } from 'lucide-vue-next'

export default {
  name: 'ClientesList',
  components: { Search, X },
  emits: ['editar', 'novo', 'verEmprestimos'],
  data() {
    return {
      clientes: [],
      busca: '',
      carregando: false,
      mensagem: '',
      mensagem_tipo: '',
      debounceTimeout: null,
      mostrarModalExcluir: false,
      clienteParaExcluir: null
    }
  },
  mounted() {
    this.buscar()
  },
  methods: {
    async buscar() {
      this.carregando = true
      try {
        const params = {}
        if (this.busca.trim()) {
          params.q = this.busca.trim()
        }
        const resp = await axios.get('/api/clientes', { params })
        this.clientes = resp.data
      } catch (err) {
        this.exibirMensagem('Erro ao carregar clientes', 'error')
      } finally {
        this.carregando = false
      }
    },
    onInputBusca() {
      clearTimeout(this.debounceTimeout)
      this.debounceTimeout = setTimeout(() => {
        this.buscar()
      }, 300)
    },
    async limparBusca() {
      this.busca = ''
      clearTimeout(this.debounceTimeout)
      await this.buscar()
    },
    abrirModalExcluir(id) {
      this.clienteParaExcluir = id
      this.mostrarModalExcluir = true
    },
    fecharModalExcluir() {
      this.mostrarModalExcluir = false
      this.clienteParaExcluir = null
    },
    async confirmarExcluir() {
      if (!this.clienteParaExcluir) return
      try {
        await axios.delete(`/api/clientes/${this.clienteParaExcluir}`)
        this.exibirMensagem('Cliente excluído com sucesso', 'success')
        this.buscar()
      } catch (err) {
        this.exibirMensagem(err.response?.data?.erro || 'Cliente tem empréstimos ativos', 'error')
      } finally {
        this.fecharModalExcluir()
      }
    },
    exibirMensagem(texto, tipo) {
      this.mensagem = texto
      this.mensagem_tipo = tipo
      setTimeout(() => { this.mensagem = '' }, 3000)
    },
    formatarTelefone(tel) {
      if (!tel) return '-'
      tel = tel.replace(/\D/g, '')
      if (tel.length > 2) {
        tel = '(' + tel.substring(0, 2) + ')' + tel.substring(2)
      }
      if (tel.length > 9) {
        tel = tel.substring(0, 9) + '-' + tel.substring(9, 13)
      }
      return tel
    }
  }
}
</script>
