<template>
  <div class="max-w-2xl mx-auto space-y-4">
    <div class="flex items-center gap-3">
      <button @click="$emit('cancelar')" class="p-2 -ml-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
      </button>
      <h1 class="text-xl font-bold text-white">Registrar Pagamento</h1>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-6">
      <form @submit.prevent="salvar" class="space-y-4">
        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Empréstimo</label>
          <select v-model="form.emprestimo_id" required :disabled="editando || emprestimoId" @change="onEmprestimoChange" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-all min-h-[48px] disabled:opacity-50">
            <option value="" disabled>Selecione um empréstimo</option>
            <option v-for="emp in empFiltrados" :key="emp.id" :value="emp.id">
              {{ emp.cliente_nome }} - R$ {{ formatarDinheiro(emp.saldo_devedor) }}
            </option>
          </select>
        </div>

        <div v-if="emprestimoSelecionado" class="bg-slate-800/50 border border-slate-700 rounded-lg p-3 space-y-2">
          <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Informações do Empréstimo</h3>
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <p class="text-slate-500 text-xs">Cliente</p>
              <p class="text-white font-medium">{{ emprestimoSelecionado.cliente_nome }}</p>
            </div>
            <div>
              <p class="text-slate-500 text-xs">Saldo Devedor</p>
              <p class="text-amber-400 font-semibold">{{ formatarDinheiro(emprestimoSelecionado.saldo_devedor) }}</p>
            </div>
            <div>
              <p class="text-slate-500 text-xs">Valor Original</p>
              <p class="text-white">{{ formatarDinheiro(emprestimoSelecionado.valor_original) }}</p>
            </div>
            <div>
              <p class="text-slate-500 text-xs">Juros Acumulados ({{ emprestimoSelecionado.meses_atraso || 0 }} meses)</p>
              <p class="text-red-400 font-medium">{{ formatarDinheiro(getJurosAcumulados()) }}</p>
            </div>
          </div>
        </div>

        <div v-if="emprestimoSelecionado" class="space-y-3">
          <h3 class="text-sm font-semibold text-slate-300">Forma de Pagamento</h3>
           
          <label class="flex items-start gap-3 p-3 bg-slate-800/50 border border-slate-700 rounded-lg cursor-pointer" :class="pagarJuros ? 'border-amber-500 bg-amber-500/5' : ''">
            <input type="checkbox" v-model="pagarJuros" class="w-5 h-5 mt-0.5 rounded border-slate-600 text-amber-500 focus:ring-amber-500 focus:ring-offset-slate-900">
            <div>
              <p class="text-white font-medium">Pagar Juros</p>
              <p class="text-slate-400 text-sm">Juros {{ valorJurosPadrao ? 'do mês' : 'acumulados' }} ({{ emprestimoSelecionado.meses_atraso || 0 }} meses): {{ formatarDinheiro(getJurosAcumulados()) }}</p>
            </div>
          </label>

          <label class="flex items-start gap-3 p-3 bg-slate-800/50 border border-slate-700 rounded-lg cursor-pointer" :class="pagarSaldo ? 'border-amber-500 bg-amber-500/5' : ''">
            <input type="checkbox" v-model="pagarSaldo" class="w-5 h-5 mt-0.5 rounded border-slate-600 text-amber-500 focus:ring-amber-500 focus:ring-offset-slate-900">
            <div>
              <p class="text-white font-medium">Pagar Saldo Devedor</p>
              <p class="text-slate-400 text-sm">Saldo: {{ formatarDinheiro(emprestimoSelecionado.saldo_devedor) }}</p>
            </div>
          </label>

          <div v-if="pagarSaldo" class="pl-8 space-y-2">
            <label class="text-sm font-medium text-slate-300">Valor a pagar no saldo</label>
            <input v-model="form.valor_saldo" type="number" step="0.01" min="0" :max="emprestimoSelecionado.saldo_devedor" placeholder="0.00" class="w-full px-3 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-all min-h-[48px]">
            <div class="flex gap-2">
              <button type="button" @click="sugerirValor(50)" class="flex-1 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm transition-all border border-slate-700">50%</button>
              <button type="button" @click="sugerirValor(100)" class="flex-1 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm transition-all border border-slate-700">100%</button>
            </div>
          </div>
        </div>

        <div v-if="emprestimoSelecionado && valorTotal > 0" class="bg-gradient-to-r from-amber-500 to-amber-600 rounded-lg p-4 text-center">
          <p class="text-amber-100 text-xs font-medium">Total a Pagar</p>
          <p class="text-2xl font-bold text-white">{{ formatarDinheiro(valorTotal) }}</p>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Data do Pagamento</label>
          <input v-model="form.data" type="date" required :disabled="bloquearDataPagamento" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-all min-h-[48px] disabled:opacity-50">
        </div>

        <div class="flex flex-col sm:flex-row gap-3 pt-2">
          <button type="submit" class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 bg-amber-500 hover:bg-amber-400 text-white rounded-lg transition-all font-medium shadow-lg shadow-amber-500/25 min-h-[48px]">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
            Confirmar Pagamento
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
  name: 'PagamentosForm',
  props: {
    pagamento: { type: Object, default: null },
    clienteId: { type: Number, default: null },
    emprestimoId: { type: Number, default: null },
    dataPagamentoPadrao: { type: String, default: null },
    valorJurosPadrao: { type: Number, default: null },
    bloquearDataPagamento: { type: Boolean, default: false }
  },
  emits: ['salvo', 'cancelar'],
  data() {
    return {
      form: {
        emprestimo_id: '',
        valor_saldo: '',
        data: new Date().toISOString().split('T')[0]
      },
      emprestimos: [],
      emprestimoSelecionado: null,
      pagarJuros: false,
      pagarSaldo: false
    }
  },
  computed: {
    editando() {
      return this.pagamento !== null
    },
    valorTotal() {
      let total = 0
      if (this.pagarJuros && this.emprestimoSelecionado) {
        if (this.valorJurosPadrao) {
          total += this.valorJurosPadrao
        } else {
          total += this.emprestimoSelecionado.juros_acumulados || 0
        }
      }
      if (this.pagarSaldo && this.form.valor_saldo) {
        total += parseFloat(this.form.valor_saldo)
      }
      return total
    },
    empFiltrados() {
      return this.emprestimos.filter(emp => emp.saldo_devedor && emp.saldo_devedor > 0)
    }
  },
  watch: {
    pagamento: {
      immediate: true,
      handler(novo) {
        if (novo) {
          this.form = {
            emprestimo_id: novo.emprestimo_id,
            valor_saldo: '',
            data: novo.data ? novo.data.split('T')[0] : this.getDataPadrao()
          }
        } else {
          this.form = {
            emprestimo_id: '',
            valor_saldo: '',
            data: this.getDataPadrao()
          }
        }
      }
    },
    dataPagamentoPadrao(novo) {
      if (!this.editando && novo) {
        this.form.data = novo
      }
    }
  },
  mounted() {
    this.buscarEmprestimos()
  },
  methods: {
    getDataPadrao() {
      return this.dataPagamentoPadrao || new Date().toISOString().split('T')[0]
    },
    getJurosAcumulados() {
      if (!this.emprestimoSelecionado) return 0
      if (this.valorJurosPadrao) return this.valorJurosPadrao
      const juros = this.emprestimoSelecionado.juros_acumulados
      if (typeof juros === 'number' && juros > 0) return juros
      return this.emprestimoSelecionado.juros || 0
    },
    async buscarEmprestimos() {
      try {
        let url = '/api/emprestimos'
        if (this.clienteId) {
          url = `/api/clientes/${this.clienteId}/emprestimos`
        }
        const resp = await api.get(url)
        this.emprestimos = resp.data
        
        if (this.emprestimoId) {
          this.form.emprestimo_id = this.emprestimoId
          this.emprestimoSelecionado = this.emprestimos.find(e => e.id === this.emprestimoId)
          if (this.valorJurosPadrao || (this.emprestimoSelecionado && (this.emprestimoSelecionado.juros_acumulados || 0) > 0)) {
            this.pagarJuros = true
          }
        } else if (this.form.emprestimo_id) {
          this.emprestimoSelecionado = this.emprestimos.find(e => e.id === parseInt(this.form.emprestimo_id))
        }
      } catch (err) {
        console.error('Erro ao carregar empréstimos', err)
      }
    },
    onEmprestimoChange() {
      this.emprestimoSelecionado = this.emprestimos.find(e => e.id === parseInt(this.form.emprestimo_id))
      this.pagarJuros = false
      this.pagarSaldo = false
      this.form.valor_saldo = ''
      if (this.valorJurosPadrao || (this.emprestimoSelecionado && (this.emprestimoSelecionado.juros_acumulados || 0) > 0)) {
        this.pagarJuros = true
      }
    },
    sugerirValor(porcentagem) {
      if (this.emprestimoSelecionado) {
        const valor = (porcentagem / 100) * this.emprestimoSelecionado.saldo_devedor
        this.form.valor_saldo = valor.toFixed(2)
      }
    },
    async salvar() {
      try {
        if (!this.form.emprestimo_id) {
          alert('Selecione um empréstimo')
          return
        }

        let valorFinal = 0
        if (this.pagarJuros && this.emprestimoSelecionado) {
          if (this.valorJurosPadrao) {
            valorFinal += this.valorJurosPadrao
          } else {
            valorFinal += this.emprestimoSelecionado.juros_acumulados || 0
          }
        }
        if (this.pagarSaldo && this.form.valor_saldo) {
          valorFinal += parseFloat(this.form.valor_saldo)
        }

        if (valorFinal <= 0) {
          alert('Informe um valor maior que zero')
          return
        }

        const dataToSend = {
          valor: valorFinal,
          pagar_juros: this.valorJurosPadrao ? false : this.pagarJuros,
          pagar_saldo: this.pagarSaldo ? parseFloat(this.form.valor_saldo || 0) : 0,
          data: this.form.data
        }

        if (this.editando) {
          await api.put(`/api/pagamentos/${this.pagamento.id}`, dataToSend)
        } else {
          dataToSend.emprestimo_id = parseInt(this.form.emprestimo_id)
          await api.post('/api/pagamentos', dataToSend)
        }
        this.$emit('salvo')
        this.limpar()
      } catch (err) {
        alert(err.response?.data?.erro || 'Erro ao salvar pagamento')
      }
    },
    limpar() {
      this.form = {
        emprestimo_id: '',
        valor_saldo: '',
        data: this.getDataPadrao()
      }
      this.emprestimoSelecionado = null
      this.pagarJuros = false
      this.pagarSaldo = false
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
