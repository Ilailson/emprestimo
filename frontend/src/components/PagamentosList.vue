<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <h1 class="text-xl sm:text-2xl font-bold text-white">Pagamentos</h1>
      <div class="flex gap-2">
        <button v-if="emprestimoId || clienteId" @click="$emit('voltar')" class="inline-flex items-center justify-center gap-2 px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-all border border-slate-700 min-h-[44px]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          <span class="hidden sm:inline">Voltar</span>
        </button>
        <button v-if="!emprestimoId" @click="$emit('novo')" class="hidden md:inline-flex items-center justify-center gap-2 px-4 py-3 bg-amber-500 hover:bg-amber-400 text-white rounded-lg transition-all font-medium min-h-[44px]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
          <span class="hidden sm:inline">Novo Pagamento</span>
        </button>
      </div>
    </div>

    <!-- Botão flutuante mobile -->
    <button v-if="!emprestimoId" @click="$emit('novo')" class="md:hidden fixed bottom-6 right-6 w-14 h-14 bg-amber-500 hover:bg-amber-400 text-white rounded-full shadow-lg shadow-amber-500/50 flex items-center justify-center z-40">
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
        class="w-full pl-10 pr-10 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-all min-h-[44px]"
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
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Cliente</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Valor</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Juros</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Tipo</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Data</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800">
            <tr v-for="pag in pagamentos" :key="pag.id" class="hover:bg-slate-800/50 transition-colors">
              <td class="px-4 py-3">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-400 font-semibold text-xs">
                    {{ pag.emprestimo_nome.charAt(0).toUpperCase() }}
                  </div>
                  <span class="text-white font-medium text-sm">{{ pag.emprestimo_nome }}</span>
                </div>
              </td>
              <td class="px-4 py-3">
                <span class="text-emerald-400 font-semibold">{{ formatarValorPrincipalExibicao(pag) }}</span>
              </td>
              <td class="px-4 py-3">
                <span class="text-amber-400 font-semibold">{{ formatarDinheiro(getValorJuros(pag)) }}</span>
              </td>
              <td class="px-4 py-3">
                <span v-if="getTipoPagamento(pag) === 'Juros'" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-400">
                  Juros
                </span>
                <span v-else-if="getTipoPagamento(pag) === 'Misto'" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-sky-500/20 text-sky-300">
                  Valor + Juros
                </span>
                <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400">
                  Principal
                </span>
              </td>
              <td class="px-4 py-3 text-slate-300 text-sm">{{ formatarData(pag.data) }}</td>
              <td class="px-4 py-3">
                <button @click="abrirModalExcluir(pag.id)" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 hover:text-red-300 rounded-lg transition-all text-sm font-medium border border-red-500/30">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Mobile: Cards -->
    <div class="md:hidden space-y-3">
      <div v-for="pag in pagamentos" :key="pag.id" class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="flex items-start gap-3">
          <div class="w-10 h-10 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-400 font-semibold flex-shrink-0">
            {{ pag.emprestimo_nome.charAt(0).toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-white font-medium truncate">{{ pag.emprestimo_nome }}</h3>
            <div class="flex items-center gap-2 mt-2">
              <span v-if="getTipoPagamento(pag) === 'Juros'" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-400">
                Juros
              </span>
              <span v-else-if="getTipoPagamento(pag) === 'Misto'" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-sky-500/20 text-sky-300">
                Valor + Juros
              </span>
              <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400">
                Principal
              </span>
            </div>
          </div>
          <span class="text-emerald-400 font-semibold text-lg">{{ formatarValorResumo(pag) }}</span>
        </div>

        <div class="flex items-center justify-between mt-4 pt-3 border-t border-slate-800">
          <p class="text-slate-400 text-sm">{{ formatarData(pag.data) }}</p>
          <button @click="abrirModalExcluir(pag.id)" class="inline-flex items-center gap-1.5 px-4 py-2.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 hover:text-red-300 rounded-lg transition-all text-sm font-medium border border-red-500/30 min-h-[44px]">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            Excluir
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="pagamentos.length === 0" class="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
      <svg class="w-12 h-12 mx-auto text-slate-600 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
      </svg>
      <p class="text-slate-500">Nenhum pagamento registrado</p>
      <p class="text-slate-600 text-sm mt-1">Clique em "Novo Pagamento" para registrar</p>
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
  name: 'PagamentosList',
  components: { Search, X },
  props: {
    clienteId: { type: Number, default: null },
    emprestimoId: { type: Number, default: null }
  },
  emits: ['novo', 'voltar'],
  data() {
    return {
      pagamentos: [],
      mensagem: '',
      mensagem_tipo: '',
      busca: '',
      debounceTimeout: null,
      mostrarModalExcluir: false,
      pagamentoParaExcluir: null
    }
  },
  mounted() {
    this.buscar()
  },
  watch: {
    clienteId() {
      this.buscar()
    },
    emprestimoId() {
      this.buscar()
    }
  },
  methods: {
    async buscar() {
      try {
        let url = '/api/pagamentos'
        if (this.emprestimoId) {
          url = `/api/emprestimos/${this.emprestimoId}/pagamentos`
        } else if (this.clienteId) {
          url = `/api/clientes/${this.clienteId}/pagamentos`
        }
        const params = {}
        if (this.busca && this.busca.trim()) {
          params.q = this.busca.trim()
        }
        const resp = await axios.get(url, { params })
        this.pagamentos = resp.data
      } catch (err) {
        this.exibirMensagem('Erro ao carregar pagamentos', 'error')
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
      this.pagamentoParaExcluir = id
      this.mostrarModalExcluir = true
    },
    fecharModalExcluir() {
      this.mostrarModalExcluir = false
      this.pagamentoParaExcluir = null
    },
    async confirmarExcluir() {
      if (!this.pagamentoParaExcluir) return
      try {
        await axios.delete(`/api/pagamentos/${this.pagamentoParaExcluir}`)
        this.exibirMensagem('Pagamento excluído com sucesso', 'success')
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
    toNumber(valor) {
      const numero = parseFloat(valor)
      return Number.isFinite(numero) ? numero : 0
    },
    getValorJuros(pag) {
      const juros = this.toNumber(pag.valor_juros)
      if (juros > 0) return juros
      return pag.is_juros ? this.toNumber(pag.valor) : 0
    },
    getValorPrincipal(pag) {
      if (typeof pag.valor_principal === 'number') {
        return this.toNumber(pag.valor_principal)
      }

      const valor = this.toNumber(pag.valor)
      const juros = this.toNumber(pag.valor_juros)
      if (pag.is_juros === true) return 0
      if (pag.is_juros === null && juros > 0) return valor
      if (juros > 0) {
        const principal = valor - juros
        return principal > 0 ? principal : 0
      }
      return valor
    },
    getTipoPagamento(pag) {
      const principal = this.getValorPrincipal(pag)
      const juros = this.getValorJuros(pag)
      if (principal > 0 && juros > 0) return 'Misto'
      if (juros > 0) return 'Juros'
      return 'Principal'
    },
    formatarValorPrincipalExibicao(pag) {
      const principal = this.getValorPrincipal(pag)
      if (principal <= 0) return '-'
      return this.formatarDinheiro(principal)
    },
    formatarValorResumo(pag) {
      const principal = this.getValorPrincipal(pag)
      const juros = this.getValorJuros(pag)
      if (principal > 0 && juros > 0) {
        return `${this.formatarDinheiro(principal)} + ${this.formatarDinheiro(juros)}`
      }
      if (juros > 0) return this.formatarDinheiro(juros)
      return this.formatarDinheiro(principal)
    },
    formatarDinheiro(valor) {
      if (!valor) return 'R$ 0,00'
      const numero = parseFloat(valor).toFixed(2)
      const partes = numero.split('.')
      partes[0] = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.')
      return 'R$ ' + partes.join(',')
    },
    formatarData(data) {
      if (!data) return '-'
      return new Date(data).toLocaleDateString('pt-BR')
    }
  }
}
</script>
