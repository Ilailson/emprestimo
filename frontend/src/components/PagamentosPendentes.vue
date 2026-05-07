<template>
  <div class="space-y-4">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Pagamentos Pendentes</h1>
        <p class="text-slate-400 text-sm">Exibe pendências do mês atual e meses anteriores.</p>
      </div>
      <button
        @click="buscar"
        :disabled="carregando"
        class="inline-flex items-center justify-center gap-2 px-4 py-3 bg-slate-800 hover:bg-slate-700 disabled:opacity-60 disabled:cursor-not-allowed text-slate-300 rounded-lg transition-all border border-slate-700 min-h-[44px]"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        Atualizar
      </button>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p class="text-slate-500 text-xs uppercase tracking-wider">Pendências</p>
        <p class="text-white text-2xl font-bold mt-1">{{ pendentesFiltrados.length }}</p>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p class="text-slate-500 text-xs uppercase tracking-wider">Clientes</p>
        <p class="text-white text-2xl font-bold mt-1">{{ totalClientesFiltrados }}</p>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <p class="text-slate-500 text-xs uppercase tracking-wider">Mês Atual</p>
        <p class="text-white text-2xl font-bold mt-1">{{ pendentesMesAtual }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-3">
      <div class="relative lg:col-span-2">
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
      <select
        v-model="clienteFiltro"
        class="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-all min-h-[44px]"
      >
        <option value="">Todos os clientes</option>
        <option v-for="cli in clientesComPendencia" :key="cli.id" :value="String(cli.id)">
          {{ cli.nome }}
        </option>
      </select>
    </div>

    <div
      v-if="mensagem"
      :class="['p-4 rounded-lg text-sm flex items-center gap-3', mensagem_tipo === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20']"
    >
      <svg v-if="mensagem_tipo === 'error'" class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <svg v-else class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <span class="break-words">{{ mensagem }}</span>
    </div>

    <div v-if="carregando" class="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-slate-400">
      Carregando pendências...
    </div>

    <div v-else-if="pendentesFiltrados.length > 0" class="space-y-3">
      <div class="hidden md:block bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-800 bg-slate-800/50">
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Cliente</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Mês Ref.</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Vencimento</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Juros Mês</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Saldo</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800">
              <tr v-for="item in pendentesFiltrados" :key="item.id" class="hover:bg-slate-800/50 transition-colors">
                <td class="px-4 py-3">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-400 font-semibold text-xs">
                      {{ item.cliente_nome.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <p class="text-white font-medium text-sm">{{ item.cliente_nome }}</p>
                      <p class="text-slate-500 text-xs">{{ item.cliente_telefone || 'Sem telefone' }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-4 py-3 text-slate-300 text-sm">{{ item.mes_referencia }}</td>
                <td class="px-4 py-3 text-slate-300 text-sm">{{ formatarData(item.data_referencia) }}</td>
                <td class="px-4 py-3 text-amber-400 font-semibold">{{ formatarDinheiro(item.valor_juros_mensal) }}</td>
                <td class="px-4 py-3 text-emerald-400 font-semibold">{{ formatarDinheiro(item.saldo_devedor) }}</td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2">
                    <button
                      @click="abrirFormPagamento(item)"
                      class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 rounded-lg transition-all text-sm font-medium border border-amber-500/30"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
                      </svg>
                      Pagar
                    </button>
                    <button
                      @click="abrirWhatsApp(item)"
                      class="inline-flex items-center justify-center p-2 bg-green-500/10 hover:bg-green-500/20 text-green-400 rounded-lg transition-all border border-green-500/30"
                      title="WhatsApp"
                    >
                      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.272-.099-.47-.148-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.149-.174.198-.297.297-.497.099-.198.05-.371-.025-.521-.074-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479s1.065 2.876 1.213 3.074c.148.198 2.095 3.2 5.077 4.487.709.306 1.262.489 1.694.626.712.226 1.36.193 1.872.117.571-.085 1.758-.719 2.005-1.432.247-.713.247-1.324.173-1.432-.074-.099-.272-.148-.57-.247z"/>
                        <path d="M12.003 21.638c1.879 0 3.729-.552 5.313-1.594l1.742 1.742a1.06 1.06 0 001.502-1.502l-1.742-1.742A9.64 9.64 0 0021.638 12c0-5.302-4.336-9.638-9.638-9.638S2.362 6.698 2.362 12s4.336 9.638 9.638 9.638zm0-17.276c4.158 0 7.638 3.48 7.638 7.638s-3.48 7.638-7.638 7.638-7.638-3.48-7.638-7.638S7.845 4.362 12.003 4.362z"/>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="md:hidden space-y-3">
        <div v-for="item in pendentesFiltrados" :key="item.id" class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div class="flex items-start gap-3">
            <div class="w-10 h-10 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-400 font-semibold flex-shrink-0">
              {{ item.cliente_nome.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-white font-medium truncate">{{ item.cliente_nome }}</h3>
              <p class="text-slate-400 text-sm">{{ item.mes_referencia }} • {{ formatarData(item.data_referencia) }}</p>
              <p class="text-slate-500 text-xs mt-1">{{ item.cliente_telefone || 'Sem telefone' }}</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2 mt-3 text-sm">
            <div>
              <p class="text-slate-500 text-xs">Juros Mês</p>
              <p class="text-amber-400 font-semibold">{{ formatarDinheiro(item.valor_juros_mensal) }}</p>
            </div>
            <div>
              <p class="text-slate-500 text-xs">Saldo</p>
              <p class="text-emerald-400 font-semibold">{{ formatarDinheiro(item.saldo_devedor) }}</p>
            </div>
          </div>

          <div class="flex gap-2 mt-4 pt-3 border-t border-slate-800">
            <button
              @click="abrirFormPagamento(item)"
              class="flex-1 py-2.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 rounded-lg text-sm font-medium border border-amber-500/30"
            >
              Pagar
            </button>
            <button
              @click="abrirWhatsApp(item)"
              class="p-2.5 text-green-400 hover:text-green-300 hover:bg-green-500/10 rounded-lg transition-all"
              title="WhatsApp"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.272-.099-.47-.148-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.149-.174.198-.297.297-.497.099-.198.05-.371-.025-.521-.074-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479s1.065 2.876 1.213 3.074c.148.198 2.095 3.2 5.077 4.487.709.306 1.262.489 1.694.626.712.226 1.36.193 1.872.117.571-.085 1.758-.719 2.005-1.432.247-.713.247-1.324.173-1.432-.074-.099-.272-.148-.57-.247z"/>
                <path d="M12.003 21.638c1.879 0 3.729-.552 5.313-1.594l1.742 1.742a1.06 1.06 0 001.502-1.502l-1.742-1.742A9.64 9.64 0 0021.638 12c0-5.302-4.336-9.638-9.638-9.638S2.362 6.698 2.362 12s4.336 9.638 9.638 9.638zm0-17.276c4.158 0 7.638 3.48 7.638 7.638s-3.48 7.638-7.638 7.638-7.638-3.48-7.638-7.638S7.845 4.362 12.003 4.362z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
      <svg class="w-12 h-12 mx-auto text-slate-600 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-3-3v6m9-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p class="text-slate-500">Nenhum pagamento pendente encontrado</p>
      <p class="text-slate-600 text-sm mt-1">Clientes estão em dia até o mês atual.</p>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'
import { Search, X } from 'lucide-vue-next'

export default {
  name: 'PagamentosPendentes',
  components: { Search, X },
  emits: ['fazerPagamento'],
  data() {
    return {
      pendentes: [],
      carregando: false,
      busca: '',
      buscaAplicada: '',
      clienteFiltro: '',
      debounceTimeout: null,
      mensagem: '',
      mensagem_tipo: ''
    }
  },
  computed: {
    mesAtualKey() {
      const agora = new Date()
      const mes = String(agora.getMonth() + 1).padStart(2, '0')
      return `${agora.getFullYear()}-${mes}`
    },
    clientesComPendencia() {
      const mapa = new Map()
      this.pendentes.forEach((item) => {
        if (!mapa.has(item.cliente_id)) {
          mapa.set(item.cliente_id, { id: item.cliente_id, nome: item.cliente_nome })
        }
      })
      return Array.from(mapa.values()).sort((a, b) => a.nome.localeCompare(b.nome))
    },
    pendentesFiltrados() {
      const termo = this.buscaAplicada.trim().toLowerCase()
      return this.pendentes.filter((item) => {
        if (this.clienteFiltro && String(item.cliente_id) !== this.clienteFiltro) {
          return false
        }
        if (!termo) return true
        return (
          item.cliente_nome.toLowerCase().includes(termo) ||
          (item.cliente_telefone || '').toLowerCase().includes(termo) ||
          item.mes_referencia.toLowerCase().includes(termo)
        )
      })
    },
    totalClientesFiltrados() {
      const ids = new Set(this.pendentesFiltrados.map((item) => item.cliente_id))
      return ids.size
    },
    pendentesMesAtual() {
      return this.pendentesFiltrados.filter((item) => item.mes_key === this.mesAtualKey).length
    }
  },
  mounted() {
    this.buscar()
  },
  methods: {
    onInputBusca() {
      clearTimeout(this.debounceTimeout)
      this.debounceTimeout = setTimeout(() => {
        this.buscaAplicada = this.busca
      }, 300)
    },
    limparBusca() {
      this.busca = ''
      this.buscaAplicada = ''
      clearTimeout(this.debounceTimeout)
    },
    parseDataLocal(valor) {
      if (!valor) return null
      const dataIso = String(valor).split('T')[0]
      const [ano, mes, dia] = dataIso.split('-').map(Number)
      if (!ano || !mes || !dia) return null
      return new Date(ano, mes - 1, dia)
    },
    toISODate(data) {
      const ano = data.getFullYear()
      const mes = String(data.getMonth() + 1).padStart(2, '0')
      const dia = String(data.getDate()).padStart(2, '0')
      return `${ano}-${mes}-${dia}`
    },
    getMonthKey(data) {
      const mes = String(data.getMonth() + 1).padStart(2, '0')
      return `${data.getFullYear()}-${mes}`
    },
    montarMesesEntre(inicio, fim) {
      const meses = []
      let ano = inicio.getFullYear()
      let mes = inicio.getMonth()
      while (ano < fim.getFullYear() || (ano === fim.getFullYear() && mes <= fim.getMonth())) {
        meses.push(`${ano}-${String(mes + 1).padStart(2, '0')}`)
        mes += 1
        if (mes > 11) {
          mes = 0
          ano += 1
        }
      }
      return meses
    },
    criarDataReferencia(diaBase, mesKey) {
      const [ano, mes] = mesKey.split('-').map(Number)
      const ultimoDiaMes = new Date(ano, mes, 0).getDate()
      const dia = Math.min(diaBase, ultimoDiaMes)
      return new Date(ano, mes - 1, dia)
    },
    formatarMesReferencia(mesKey) {
      const [ano, mes] = mesKey.split('-').map(Number)
      const nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
      return `${nomes[mes - 1]}/${ano}`
    },
    async buscar() {
      this.carregando = true
      try {
        const [respEmprestimos, respPagamentos] = await Promise.all([
          api.get('/api/emprestimos'),
          api.get('/api/pagamentos')
        ])

        const fimMesAtual = new Date()
        fimMesAtual.setHours(0, 0, 0, 0)
        fimMesAtual.setDate(1)
        fimMesAtual.setMonth(fimMesAtual.getMonth() + 1)
        fimMesAtual.setDate(0)

        const pagamentosPorEmprestimoMes = new Map()
        respPagamentos.data.forEach((pag) => {
          const dataPag = this.parseDataLocal(pag.data)
          if (!dataPag || dataPag > fimMesAtual) return
          const keyMes = this.getMonthKey(dataPag)
          const keyEmp = pag.emprestimo_id
          if (!pagamentosPorEmprestimoMes.has(keyEmp)) {
            pagamentosPorEmprestimoMes.set(keyEmp, new Set())
          }
          pagamentosPorEmprestimoMes.get(keyEmp).add(keyMes)
        })

        const pendencias = []
        respEmprestimos.data.forEach((emp) => {
          if (!emp || emp.status === 'pago') return
          if ((emp.saldo_devedor || 0) <= 0) return

          const dataVencimento = this.parseDataLocal(emp.data_vencimento)
          if (!dataVencimento || dataVencimento > fimMesAtual) return

          const mesesEsperados = this.montarMesesEntre(dataVencimento, fimMesAtual)
          const mesesPagos = pagamentosPorEmprestimoMes.get(emp.id) || new Set()

          mesesEsperados.forEach((mesKey) => {
            if (mesesPagos.has(mesKey)) return
            const dataRef = this.criarDataReferencia(dataVencimento.getDate(), mesKey)
            pendencias.push({
              id: `${emp.id}-${mesKey}`,
              emprestimo_id: emp.id,
              cliente_id: emp.cliente_id,
              cliente_nome: emp.cliente_nome || 'Cliente',
              cliente_telefone: emp.cliente_telefone || '',
              mes_key: mesKey,
              mes_referencia: this.formatarMesReferencia(mesKey),
              data_referencia: this.toISODate(dataRef),
              saldo_devedor: emp.saldo_devedor || 0,
              valor_juros_mensal: emp.juros || 0
            })
          })
        })

        pendencias.sort((a, b) => {
          if (a.mes_key !== b.mes_key) return a.mes_key.localeCompare(b.mes_key)
          return a.cliente_nome.localeCompare(b.cliente_nome)
        })

        this.pendentes = pendencias
      } catch (err) {
        this.exibirMensagem('Erro ao carregar pagamentos pendentes', 'error')
      } finally {
        this.carregando = false
      }
    },
    abrirFormPagamento(item) {
      this.$emit('fazerPagamento', {
        emprestimo_id: item.emprestimo_id,
        data_referencia: item.data_referencia
      })
    },
    abrirWhatsApp(item) {
      if (!item.cliente_telefone) {
        this.exibirMensagem('Cliente sem telefone cadastrado', 'error')
        return
      }
      let telefone = item.cliente_telefone.replace(/\D/g, '')
      if (!telefone.startsWith('55')) {
        telefone = '55' + telefone
      }
      const texto = `Ola ${item.cliente_nome}, pagamento pendente de ${item.mes_referencia} com vencimento em ${this.formatarData(item.data_referencia)}.`
      const url = `https://wa.me/${telefone}?text=${encodeURIComponent(texto)}`
      window.open(url, '_blank')
    },
    exibirMensagem(texto, tipo) {
      this.mensagem = texto
      this.mensagem_tipo = tipo
      setTimeout(() => {
        this.mensagem = ''
      }, 3500)
    },
    formatarData(data) {
      if (!data) return '-'
      const dt = this.parseDataLocal(data)
      if (!dt) return '-'
      return dt.toLocaleDateString('pt-BR')
    },
    formatarDinheiro(valor) {
      if (!valor) return 'R$ 0,00'
      const numero = parseFloat(valor).toFixed(2)
      const partes = numero.split('.')
      partes[0] = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.')
      return 'R$ ' + partes.join(',')
    }
  }
}
</script>
