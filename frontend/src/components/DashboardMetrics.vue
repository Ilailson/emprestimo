<template>
  <div class="space-y-4 lg:space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
      <h1 class="text-xl lg:text-2xl font-bold text-white">Dashboard</h1>
      <p class="text-slate-400 text-xs sm:text-sm">{{ dataAtual }}</p>
    </div>

    <!-- Metrics Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-blue-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10 group cursor-pointer" @click="$emit('navigate', 'clientes')">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-slate-400 text-sm font-medium mb-2">Total de Clientes</p>
            <p class="text-3xl font-bold text-white group-hover:text-blue-400 transition-colors">{{ metricas.clientes }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center group-hover:bg-blue-500/30 transition-colors">
            <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.357-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.357-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2 text-sm">
          <span class="text-emerald-400 flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
            </svg>
            Ativos
          </span>
          <span class="text-slate-500">|</span>
          <span class="text-slate-400">Ver detalhes →</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-emerald-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/10 group cursor-pointer" @click="$emit('navigate', 'emprestimos')">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-slate-400 text-sm font-medium mb-2">Empréstimos Ativos</p>
            <p class="text-3xl font-bold text-white group-hover:text-emerald-400 transition-colors">{{ metricas.emprestimos }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center group-hover:bg-emerald-500/30 transition-colors">
            <svg class="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2 text-sm">
          <span class="text-amber-400 flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Em aberto
          </span>
          <span class="text-slate-500">|</span>
          <span class="text-slate-400">Ver detalhes →</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-amber-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-amber-500/10 group cursor-pointer" @click="$emit('navigate', 'pagamentos')">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-slate-400 text-sm font-medium mb-2">Total Recebido</p>
            <p class="text-3xl font-bold text-white group-hover:text-amber-400 transition-colors">{{ formatarDinheiro(metricas.totalRecebido) }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center group-hover:bg-amber-500/30 transition-colors">
            <svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2 text-sm">
          <span class="text-emerald-400 flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            {{ metricas.totalPagamentos }} pagamentos
          </span>
          <span class="text-slate-500">|</span>
          <span class="text-slate-400">Ver detalhes →</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-orange-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-orange-500/10 group cursor-pointer" @click="$emit('navigate', 'pagamentos')">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-slate-400 text-sm font-medium mb-2">Total Juros Recebidos</p>
            <p class="text-3xl font-bold text-white group-hover:text-orange-400 transition-colors">{{ formatarDinheiro(metricas.totalJuros) }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-orange-500/20 flex items-center justify-center group-hover:bg-orange-500/30 transition-colors">
            <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2 text-sm">
          <span class="text-orange-400 flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Soma dos juros
          </span>
          <span class="text-slate-500">|</span>
          <span class="text-slate-400">Ver detalhes →</span>
        </div>
      </div>

      <div class="bg-gradient-to-br from-blue-600 to-blue-700 border border-blue-500/50 rounded-xl p-5 hover:shadow-lg hover:shadow-blue-500/25 transition-all duration-300 group cursor-pointer">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-blue-200 text-sm font-medium mb-2">Valor Total Emprestado</p>
            <p class="text-3xl font-bold text-white">{{ formatarDinheiro(metricas.valorTotal) }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center group-hover:bg-white/30 transition-colors">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center gap-2 text-sm">
          <span class="text-blue-200">Saldo devedor</span>
          <span class="text-blue-300 font-semibold">{{ formatarDinheiro(metricas.saldoDevedor) }}</span>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Emprestimos Recentes -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div class="p-5 border-b border-slate-800">
          <h3 class="text-lg font-semibold text-white flex items-center gap-2">
            <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Empréstimos Recentes
          </h3>
        </div>
        <div class="divide-y divide-slate-800">
          <div v-for="emp in recentEmprestimos" :key="emp.id" class="p-4 hover:bg-slate-800/50 transition-colors">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-white font-medium">{{ emp.cliente_nome }}</p>
                <p class="text-slate-400 text-sm">{{ formatarData(emp.data) }}</p>
              </div>
              <div class="text-right">
                <p class="text-white font-semibold">{{ formatarDinheiro(emp.valor_original) }}</p>
                <p class="text-slate-400 text-sm">{{ emp.taxa_juros }}% ao mês</p>
              </div>
            </div>
          </div>
          <div v-if="recentEmprestimos.length === 0" class="p-8 text-center text-slate-500">
            Nenhum empréstimo recente
          </div>
        </div>
      </div>

      <!-- Ultimos Pagamentos -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div class="p-5 border-b border-slate-800">
          <h3 class="text-lg font-semibold text-white flex items-center gap-2">
            <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Últimos Pagamentos
          </h3>
        </div>
        <div class="divide-y divide-slate-800">
          <div v-for="pag in recentPagamentos" :key="pag.id" class="p-4 hover:bg-slate-800/50 transition-colors">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-white font-medium">{{ pag.emprestimo_nome }}</p>
                <p class="text-slate-400 text-sm">{{ formatarData(pag.data) }}</p>
              </div>
              <div class="text-right">
                <p class="text-emerald-400 font-semibold">+ {{ formatarDinheiro(pag.valor) }}</p>
                <span :class="['text-xs px-2 py-0.5 rounded-full', pag.is_juros ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400']">
                  {{ pag.is_juros ? 'Juros' : 'Principal' }}
                </span>
              </div>
            </div>
          </div>
          <div v-if="recentPagamentos.length === 0" class="p-8 text-center text-slate-500">
            Nenhum pagamento recente
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DashboardMetrics',
  emits: ['navigate'],
  data() {
    return {
      metricas: {
        clientes: 0,
        emprestimos: 0,
        totalRecebido: 0,
        totalPagamentos: 0,
        valorTotal: 0,
        saldoDevedor: 0,
        totalJuros: 0
      },
      recentEmprestimos: [],
      recentPagamentos: []
    }
  },
  computed: {
    dataAtual() {
      return new Date().toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
    }
  },
  mounted() {
    this.buscarDados()
  },
  methods: {
    async buscarDados() {
      try {
        const [clientes, emprestimos, pagamentos] = await Promise.all([
          axios.get('/api/clientes'),
          axios.get('/api/emprestimos'),
          axios.get('/api/pagamentos')
        ])

        this.metricas.clientes = clientes.data.length
 
        const ativos = emprestimos.data.filter(e => e.status !== 'pago')
        this.metricas.emprestimos = ativos.length
        this.metricas.valorTotal = emprestimos.data.reduce((acc, e) => acc + (e.valor_original || 0), 0)
        this.metricas.saldoDevedor = emprestimos.data.reduce((acc, e) => acc + (e.saldo_devedor || 0), 0)
        this.metricas.totalPagamentos = pagamentos.data.length
        this.metricas.totalRecebido = pagamentos.data.reduce((acc, p) => acc + (p.valor || 0), 0)
        this.metricas.totalJuros = pagamentos.data.reduce((acc, p) => acc + parseFloat(p.valor_juros || 0), 0)

        this.recentEmprestimos = emprestimos.data.slice(0, 5)
        this.recentPagamentos = pagamentos.data.slice(0, 5)
      } catch (err) {
        console.error('Erro ao carregar dados do dashboard', err)
      }
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