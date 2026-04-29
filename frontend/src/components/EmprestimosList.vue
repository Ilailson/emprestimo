<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <h1 class="text-xl sm:text-2xl font-bold text-white">Empréstimos</h1>
      <div class="flex gap-2">
        <button v-if="clienteId" @click="$emit('voltar')" class="inline-flex items-center justify-center gap-2 px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-all border border-slate-700 min-h-[44px]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          <span class="hidden sm:inline">Voltar</span>
        </button>
        <!-- Botão desktop -->
        <button @click="$emit('novo', clienteId)" class="hidden md:inline-flex items-center justify-center gap-2 px-4 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-all font-medium min-h-[44px]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
          <span class="hidden sm:inline">Novo Empréstimo</span>
        </button>
      </div>
    </div>

    <!-- Botão flutuante mobile -->
    <button @click="$emit('novo', clienteId)" class="md:hidden fixed bottom-20 right-6 w-14 h-14 bg-emerald-600 hover:bg-emerald-500 text-white rounded-full shadow-lg shadow-emerald-500/50 flex items-center justify-center z-40">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
      </svg>
    </button>

    <!-- Busca e Filtro -->
    <div class="flex flex-col sm:flex-row gap-3">
      <div class="relative flex-1">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
        <input 
          v-model="busca" 
          @input="onInputBusca"
          type="text" 
          placeholder="Buscar cliente..." 
          class="w-full pl-10 pr-10 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[44px]"
        />
        <button v-if="busca" @click="limparBusca" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white p-1">
          <X class="w-5 h-5" />
        </button>
      </div>
      <select 
        v-model="statusFilter" 
        @change="onStatusChange"
        class="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[44px]"
      >
        <option value="">Todos</option>
        <option value="em_aberto">Em Aberto</option>
        <option value="pago">Pago</option>
        <option value="atrasado">Atrasado</option>
      </select>
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
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Cliente</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Valor</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Taxa</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Saldo</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Juros</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Venc.</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Status</th>
              <th class="px-3 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800">
            <tr v-for="emp in emprestimos" :key="emp.id" :class="['transition-colors', getStatusClass(emp)]">
              <td class="px-3 py-3">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-semibold text-xs">
                    {{ emp.cliente_nome.charAt(0).toUpperCase() }}
                  </div>
                  <span class="text-white font-medium text-sm truncate max-w-[120px]">{{ emp.cliente_nome }}</span>
                </div>
              </td>
              <td class="px-3 py-3">
                <span class="text-white font-semibold text-sm">{{ formatarDinheiro(emp.valor_original) }}</span>
              </td>
              <td class="px-3 py-3">
                <span class="px-2 py-0.5 bg-slate-800 text-amber-400 rounded text-xs font-medium">{{ emp.taxa_juros }}%</span>
              </td>
              <td class="px-3 py-3">
                <span :class="['font-semibold text-sm', emp.saldo_devedor > 0 ? 'text-amber-400' : 'text-emerald-400']">
                  {{ formatarDinheiro(emp.saldo_devedor) }}
                </span>
              </td>
              <td class="px-3 py-3">
                <span class="text-amber-400 font-semibold text-sm">{{ formatarDinheiro(emp.juros) }}</span>
              </td>
              <td class="px-3 py-3 text-slate-300 text-sm">{{ formatarData(emp.data_vencimento) }}</td>
              <td class="px-3 py-3">
                <span :class="['inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold', getStatusBadge(emp)]">
                  {{ getStatusLabel(emp) }}
                </span>
              </td>
              <td class="px-3 py-3">
                <div class="flex items-center gap-1">
                  <button 
                    @click="$emit('fazerPagamento', emp)" 
                    :disabled="isPago(emp)"
                    :class="isPago(emp) 
                      ? 'p-1.5 text-slate-600 bg-slate-800/30 rounded cursor-not-allowed opacity-50' 
                      : 'p-1.5 text-emerald-400 hover:text-emerald-300 hover:bg-emerald-500/10 rounded-lg transition-all'"
                    title="Pagar"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
                    </svg>
                  </button>
                  <button 
                    @click="$emit('editar', emp)" 
                    :disabled="isPago(emp)"
                    :class="isPago(emp) 
                      ? 'p-1.5 text-slate-600 bg-slate-800/30 rounded cursor-not-allowed opacity-50' 
                      : 'p-1.5 text-slate-400 hover:text-blue-400 hover:bg-blue-500/10 rounded-lg transition-all'"
                    title="Editar"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                    </svg>
                  </button>
                  <button 
                    @click="abrirModalExcluir(emp.id)" 
                    :disabled="isPago(emp)"
                    :class="isPago(emp) 
                      ? 'p-1.5 text-slate-600 bg-slate-800/30 rounded cursor-not-allowed opacity-50' 
                      : 'p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all'"
                    title="Excluir"
                  >
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
      <div v-for="emp in emprestimos" :key="emp.id" :class="['bg-slate-900 border rounded-xl p-4', getStatusClass(emp) === 'bg-red-500/10' ? 'border-red-500/30' : 'border-slate-800']">
        <div class="flex items-start justify-between gap-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-semibold flex-shrink-0">
              {{ emp.cliente_nome.charAt(0).toUpperCase() }}
            </div>
            <div>
              <h3 class="text-white font-medium">{{ emp.cliente_nome }}</h3>
              <span :class="['inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold mt-1', getStatusBadge(emp)]">
                {{ getStatusLabel(emp) }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="grid grid-cols-2 gap-3 mt-4 pt-3 border-t border-slate-800">
          <div>
            <p class="text-slate-500 text-xs">Valor</p>
            <p class="text-white font-semibold">{{ formatarDinheiro(emp.valor_original) }}</p>
          </div>
          <div>
            <p class="text-slate-500 text-xs">Taxa</p>
            <p class="text-amber-400 font-semibold">{{ emp.taxa_juros }}%</p>
          </div>
          <div>
            <p class="text-slate-500 text-xs">Saldo</p>
            <p :class="['font-semibold', emp.saldo_devedor > 0 ? 'text-amber-400' : 'text-emerald-400']">
              {{ formatarDinheiro(emp.saldo_devedor) }}
            </p>
          </div>
          <div>
            <p class="text-slate-500 text-xs">Vencimento</p>
            <p class="text-slate-300 text-sm">{{ formatarData(emp.data_vencimento) }}</p>
          </div>
        </div>

        <div class="flex gap-2 mt-4 pt-3 border-t border-slate-800">
          <button 
            @click="$emit('fazerPagamento', emp)" 
            :disabled="isPago(emp)"
            :class="isPago(emp) 
              ? 'flex-1 py-2.5 bg-slate-800/50 text-slate-500 rounded-lg text-sm font-medium cursor-not-allowed opacity-50' 
              : 'flex-1 py-2.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 rounded-lg text-sm font-medium border border-emerald-500/30'"
          >
            Pagar
          </button>
          <button 
            @click="$emit('editar', emp)" 
            :disabled="isPago(emp)"
            :class="isPago(emp) 
              ? 'p-2.5 text-slate-600 bg-slate-800/30 rounded-lg cursor-not-allowed opacity-50' 
              : 'p-2.5 text-slate-400 hover:text-blue-400 hover:bg-blue-500/10 rounded-lg transition-all'"
            title="Editar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
            </svg>
          </button>
          <button 
            @click="abrirModalExcluir(emp.id)" 
            :disabled="isPago(emp)"
            :class="isPago(emp) 
              ? 'p-2.5 text-slate-600 bg-slate-800/30 rounded-lg cursor-not-allowed opacity-50' 
              : 'p-2.5 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all'"
            title="Excluir"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="emprestimos.length === 0" class="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
      <svg class="w-12 h-12 mx-auto text-slate-600 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
      </svg>
      <p class="text-slate-500">Nenhum empréstimo cadastrado</p>
      <p class="text-slate-600 text-sm mt-1">Clique em "Novo Empréstimo" para começar</p>
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
  name: 'EmprestimosList',
  components: { Search, X },
  props: {
    clienteId: { type: Number, default: null }
  },
  emits: ['editar', 'novo', 'voltar', 'fazerPagamento'],
  data() {
    return {
      emprestimos: [],
      busca: '',
      statusFilter: '',
      debounceTimeout: null,
      mensagem: '',
      mensagem_tipo: '',
      mostrarModalExcluir: false,
      emprestimoParaExcluir: null
    }
  },
  mounted() {
    this.buscar()
  },
  watch: {
    clienteId() {
      this.buscar()
    }
  },
  methods: {
    async buscar() {
      try {
        let url = '/api/emprestimos'
        if (this.clienteId) {
          url = `/api/clientes/${this.clienteId}/emprestimos`
        }
        const params = {}
        if (this.busca && this.busca.trim()) {
          params.q = this.busca.trim()
        }
        if (this.statusFilter && this.statusFilter.trim()) {
          params.status = this.statusFilter.trim()
        }
        
        const resp = await axios.get(url, { params })
        this.emprestimos = resp.data
      } catch (err) {
        this.exibirMensagem('Erro ao carregar empréstimos', 'error')
      }
    },
    onInputBusca() {
      clearTimeout(this.debounceTimeout)
      this.debounceTimeout = setTimeout(() => {
        this.buscar()
      }, 300)
    },
    onStatusChange() {
      this.buscar()
    },
    async limparBusca() {
      this.busca = ''
      clearTimeout(this.debounceTimeout)
      await this.buscar()
    },
    abrirModalExcluir(id) {
      this.emprestimoParaExcluir = id
      this.mostrarModalExcluir = true
    },
    fecharModalExcluir() {
      this.mostrarModalExcluir = false
      this.emprestimoParaExcluir = null
    },
    async confirmarExcluir() {
      if (!this.emprestimoParaExcluir) return
      const emp = this.emprestimos.find(e => e.id === this.emprestimoParaExcluir)
      if (emp?.status === 'pago') {
        this.exibirMensagem('Não é possível excluir empréstimo pago', 'error')
        this.fecharModalExcluir()
        return
      }
      try {
        await axios.delete(`/api/emprestimos/${this.emprestimoParaExcluir}`)
        this.exibirMensagem('Empréstimo excluído com sucesso', 'success')
        this.buscar()
      } catch (err) {
        this.exibirMensagem(err.response?.data?.erro || 'Erro ao excluir. Entre em contato com o suporte.', 'error')
      } finally {
        this.fecharModalExcluir()
      }
    },
    getStatusClass(emp) {
      if (emp.status === 'pago') return 'bg-emerald-500/5 border-emerald-500/30'
      const devedor = emp.saldo_devedor || 0
      if (devedor > 0 && emp.data_vencimento) {
        const dataVencto = new Date(emp.data_vencimento)
        if (new Date() > dataVencto) return 'bg-red-500/10 border-red-500/30'
      }
      return 'bg-slate-900 border-slate-800'
    },
    isPago(emp) {
      return emp.status === 'pago'
    },
    getStatusBadge(emp) {
      if (emp.status === 'pago') return 'bg-emerald-500/20 text-emerald-400'
      const devedor = emp.saldo_devedor || 0
      if (devedor > 0 && emp.data_vencimento) {
        const dataVencto = new Date(emp.data_vencimento)
        if (new Date() > dataVencto) return 'bg-red-500/20 text-red-400'
      }
      return 'bg-amber-500/20 text-amber-400'
    },
    getStatusLabel(emp) {
      if (emp.status === 'pago') return 'Pago'
      const devedor = emp.saldo_devedor || 0
      if (devedor > 0 && emp.data_vencimento) {
        const dataVencto = new Date(emp.data_vencimento)
        if (new Date() > dataVencto) return 'Atrasado'
      }
      return 'Em Aberto'
    },
    exibirMensagem(texto, tipo) {
      this.mensagem = texto
      this.mensagem_tipo = tipo
      setTimeout(() => { this.mensagem = '' }, 3000)
    },
    formatarDinheiro(valor) {
      if (!valor) return 'R$ 0,00'
      return 'R$ ' + parseFloat(valor).toFixed(2).replace('.', ',')
    },
    formatarData(data) {
      if (!data) return '-'
      return new Date(data).toLocaleDateString('pt-BR')
    }
  }
}
</script>