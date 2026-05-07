<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <h1 class="text-xl sm:text-2xl font-bold text-white">Relatórios</h1>
    </div>
    <!-- Seleção de Cliente -->
    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
      <h2 class="text-lg font-semibold text-white">Selecionar Cliente</h2>

      <!-- Busca com Autocomplete -->
      <div class="relative">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
        <input
          v-model="buscaCliente"
          @input="onInputBusca"
          type="text"
          placeholder="Buscar cliente por nome..."
          class="w-full pl-10 pr-10 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all min-h-[44px]"
        />
        <button v-if="buscaCliente" @click="limparBusca" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white p-1">
          <X class="w-5 h-5" />
        </button>

        <!-- Dropdown de resultados -->
        <div v-if="clientesFiltrados.length > 0 && buscaCliente" class="absolute z-10 w-full mt-1 bg-slate-800 border border-slate-700 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          <div
            v-for="cliente in clientesFiltrados"
            :key="cliente.id"
            @click="selecionarCliente(cliente)"
            class="px-4 py-3 hover:bg-slate-700 cursor-pointer border-b border-slate-700 last:border-b-0 transition-colors"
          >
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 font-semibold text-xs">
                {{ cliente.nome.charAt(0).toUpperCase() }}
              </div>
              <div>
                <p class="text-white font-medium">{{ cliente.nome }}</p>
                <p class="text-slate-400 text-sm">{{ cliente.telefone }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Cliente Selecionado -->
      <div v-if="clienteSelecionado" class="bg-slate-800 rounded-lg p-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 font-semibold">
            {{ clienteSelecionado.nome.charAt(0).toUpperCase() }}
          </div>
          <div>
            <p class="text-white font-medium">{{ clienteSelecionado.nome }}</p>
            <p class="text-slate-400 text-sm">{{ clienteSelecionado.telefone }}</p>
          </div>
        </div>
        <button @click="limparSelecao" class="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-all">
          <X class="w-5 h-5" />
        </button>
      </div>
    </div>
    <!-- Relatórios (visível apenas quando cliente selecionado) -->
    <template v-if="clienteSelecionado">
      <!-- Botões de Gerar Relatório -->
      <div class="flex flex-col sm:flex-row gap-3">
        <button @click="gerarRelatorio('juros')" :disabled="carregando" class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 bg-amber-600 hover:bg-amber-500 text-white rounded-lg transition-all font-medium disabled:opacity-50 min-h-[44px]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 0v6m0-6L9 13M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Relatório de Juros Pagos
        </button>

      </div>
      <!-- Loading -->
      <div v-if="carregando" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
        <p class="text-slate-400 mt-2">Gerando relatório...</p>
      </div>
      <!-- Relatório de Juros -->
      <div v-if="relatorioJuros" id="relatorio-juros" class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-bold text-white">Relatório de Juros Pagos</h2>
          <div class="flex gap-2">
            <button @click="imprimirRelatorio('relatorio-juros')" class="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-all" title="Imprimir">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-16v4m0 0H8m9-4v4"/>
              </svg>
            </button>
            <button @click="exportarPDF('relatorio-juros', 'relatorio-juros')" class="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-all" title="Exportar PDF">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </button>
          </div>
        </div>
        <!-- Resumo -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-slate-800 rounded-lg p-4">
            <p class="text-slate-400 text-sm">Cliente</p>
            <p class="text-white font-semibold text-lg">{{ relatorioJuros.cliente.nome }}</p>
          </div>
          <div class="bg-slate-800 rounded-lg p-4">
            <p class="text-slate-400 text-sm">Valor Total Emprestado</p>
            <p class="text-blue-400 font-semibold text-lg">{{ formatarDinheiro(relatorioJuros.valor_total_emprestado) }}</p>
          </div>
          <div class="bg-slate-800 rounded-lg p-4 border-2 border-red-500/50">
            <p class="text-slate-400 text-sm">Saldo Devedor Atual</p>
            <p class="text-red-500 font-semibold text-lg">{{ formatarDinheiro(relatorioJuros.saldo_devedor_total) }}</p>
          </div>
          <div class="bg-slate-800 rounded-lg p-4">
            <p class="text-slate-400 text-sm">Total de Juros Pagos</p>
            <p class="text-amber-400 font-semibold text-lg">{{ formatarDinheiro(relatorioJuros.total_juros_pagos) }}</p>
          </div>
          <div class="bg-slate-800 rounded-lg p-4">
            <p class="text-slate-400 text-sm">Total Pago do Saldo Devedor</p>
            <p class="text-emerald-400 font-semibold text-lg">{{ formatarDinheiro(relatorioJuros.total_principal_pago) }}</p>
          </div>
          <div class="bg-slate-800 rounded-lg p-4">
            <p class="text-slate-400 text-sm">Total Pago Saldo Devedor + Juros </p>
            <p class="text-purple-400 font-semibold text-lg">{{ formatarDinheiro(relatorioJuros.total_geral_pago) }}</p>
          </div>
          <div class="bg-slate-800 rounded-lg p-4">
            <p class="text-slate-400 text-sm">Qtd. Empréstimos / Pagamentos</p>
            <p class="text-white font-semibold text-lg">{{ relatorioJuros.quantidade_emprestimos }} / {{ relatorioJuros.quantidade_pagamentos }}</p>
          </div>
        </div>
        <!-- Tabela de Pagamentos -->
        <div class="bg-slate-800 rounded-lg overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-slate-700 bg-slate-700/50">
                  <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase">Data Do Pagamento</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase">Saldo Devedor Pago</th>
                  <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase">Juros Pago</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-700">
                <tr v-for="pag in relatorioJuros.pagamentos" :key="pag.id" class="hover:bg-slate-700/50 transition-colors">
                  <td class="px-4 py-3 text-slate-300 text-sm">{{ formatarData(pag.data) }}</td>
                  <td class="px-4 py-3 text-emerald-400 font-medium">{{ formatarDinheiro(pag.principal) }}</td>
                  <td class="px-4 py-3 text-amber-400 font-medium">{{ formatarDinheiro(pag.juros) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

    </template>
    <!-- Empty State -->
    <div v-if="!clienteSelecionado" class="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
      <svg class="w-12 h-12 mx-auto text-slate-600 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
      <p class="text-slate-500">Selecione um cliente para gerar relatórios</p>
      <p class="text-slate-600 text-sm mt-1">Use a busca acima para encontrar um cliente</p>
    </div>
  </div>
</template>
<script>
import api from '@/services/api'
import { Search, X } from 'lucide-vue-next'
import html2pdf from 'html2pdf.js'
export default {
  name: 'RelatoriosList',
  components: { Search, X },
  data() {
    return {
      buscaCliente: '',
      clientes: [],
      clientesFiltrados: [],
      clienteSelecionado: null,
      carregando: false,
      relatorioJuros: null,
      debounceTimeout: null
    }
  },
  mounted() {
    this.buscarClientes()
  },
  methods: {
    async buscarClientes() {
      try {
        const resp = await api.get('/api/clientes')
        this.clientes = resp.data
      } catch (err) {
        console.error('Erro ao carregar clientes:', err)
      }
    },
    onInputBusca() {
      clearTimeout(this.debounceTimeout)
      this.debounceTimeout = setTimeout(() => {
        this.filtrarClientes()
      }, 300)
    },
    filtrarClientes() {
      if (!this.buscaCliente.trim()) {
        this.clientesFiltrados = []
        return
      }
      const termo = this.buscaCliente.toLowerCase()
      this.clientesFiltrados = this.clientes.filter(c =>
        c.nome.toLowerCase().includes(termo) ||
        c.telefone.includes(termo)
      ).slice(0, 10)
    },
    selecionarCliente(cliente) {
      this.clienteSelecionado = cliente
      this.buscaCliente = cliente.nome
      this.clientesFiltrados = []
      this.relatorioJuros = null
    },
    limparBusca() {
      this.buscaCliente = ''
      this.clientesFiltrados = []
    },
    limparSelecao() {
      this.clienteSelecionado = null
      this.buscaCliente = ''
      this.relatorioJuros = null
    },
    async gerarRelatorio(tipo) {
      if (!this.clienteSelecionado) return

      this.carregando = true
      try {
        if (tipo === 'juros') {
          const resp = await api.get(`/api/clientes/${this.clienteSelecionado.id}/relatorio-juros`)
          this.relatorioJuros = resp.data

        }
      } catch (err) {
        console.error('Erro ao gerar relatório:', err)
        alert('Erro ao gerar relatório. Tente novamente.')
      } finally {
        this.carregando = false
      }
    },
    imprimirRelatorio(elementId) {
      const conteudo = document.getElementById(elementId).innerHTML
      const janelaImpressao = window.open('', '', 'height=600,width=800')
      janelaImpressao.document.write(`
        <html>
          <head>
            <title>Relatório</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; }
              table { width: 100%; border-collapse: collapse; margin-top: 20px; }
              th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
              th { background-color: #f5f5f5; }
            </style>
          </head>
          <body>${conteudo}</body>
        </html>
      `)
      janelaImpressao.document.close()
      janelaImpressao.focus()
      janelaImpressao.print()
    },
   exportarPDF(elementId, nomeArquivo) {
  const element = document.getElementById(elementId)
  const opt = {
    margin: 1,
    filename: `${nomeArquivo}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
  }
  html2pdf().set(opt).from(element).save()
},
    formatarDinheiro(valor) {
      if (!valor && valor !== 0) return 'R$ 0,00'
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
