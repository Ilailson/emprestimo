<template>
  <div class="max-w-2xl mx-auto space-y-4">
    <div class="flex items-center gap-3">
      <button @click="$emit('cancelar')" class="p-2 -ml-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
      </button>
      <h1 class="text-xl font-bold text-white">{{ editando ? 'Editar Empréstimo' : 'Novo Empréstimo' }}</h1>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-6">
      <form @submit.prevent="salvar" class="space-y-4">
        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Cliente</label>
          <select v-model="form.cliente_id" required :disabled="clienteId || clienteParaEmprestimo" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[48px] disabled:opacity-50">
            <option value="" disabled>Selecione um cliente</option>
            <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nome }}</option>
          </select>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-300">Data do Empréstimo</label>
            <input v-model="form.data" type="date" required class="w-full px-3 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[48px]">
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-300">Data de Vencimento</label>
            <input v-model="form.data_vencimento" type="date" class="w-full px-3 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[48px]">
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div v-if="editando" class="space-y-2">
            <label class="text-sm font-medium text-slate-300">Saldo Devedor (R$)</label>
            <input v-model="form.saldo_devedor" type="number" step="0.01" min="0" required placeholder="1000.00" class="w-full px-3 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[48px]">
          </div>
          <div v-else class="space-y-2">
            <label class="text-sm font-medium text-slate-300">Valor (R$)</label>
            <input v-model="form.valor" type="number" step="0.01" min="1" required placeholder="1000.00" class="w-full px-3 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[48px]">
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-300">Taxa (% ao mês)</label>
            <input v-model="form.taxa_juros" type="number" step="0.1" min="0" max="100" required placeholder="5" class="w-full px-3 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[48px]">
          </div>
        </div>

        <div v-if="!editando" class="space-y-2">
          <label class="text-sm font-medium text-slate-300">Status</label>
          <select v-model="form.status" class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all min-h-[48px]">
            <option value="em_aberto">Em Aberto</option>
            <option value="pago">Pago</option>
          </select>
        </div>

        <div v-if="previewTotal" class="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3 space-y-1">
          <div class="flex items-center justify-between">
            <span class="text-emerald-400 text-sm">Valor Total:</span>
            <span class="text-lg font-bold text-white">{{ formatarDinheiro(previewTotal) }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-slate-400 text-xs">Juros:</span>
            <span class="text-amber-400 font-medium text-sm">{{ formatarDinheiro(previewTotal - valorBase) }}</span>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row gap-3 pt-2">
          <button type="submit" class="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-all font-medium shadow-lg shadow-emerald-500/25 min-h-[48px]">
            <svg v-if="editando" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            {{ editando ? 'Atualizar' : 'Cadastrar' }}
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
import axios from 'axios'

export default {
  name: 'EmprestimosForm',
  props: {
    emprestimo: { type: Object, default: null },
    clienteId: { type: Number, default: null },
    clienteParaEmprestimo: { type: Object, default: null }
  },
  emits: ['salvo', 'cancelar'],
  data() {
    return {
      form: {
        cliente_id: '',
        data: new Date().toISOString().split('T')[0],
        data_vencimento: '',
        valor: '',
        saldo_devedor: '',
        taxa_juros: '30',
        status: 'em_aberto'
      },
      clientes: []
    }
  },
  computed: {
    editando() {
      return this.emprestimo !== null
    },
    valorBase() {
      return this.editando ? this.form.saldo_devedor : this.form.valor
    },
    previewTotal() {
      if (!this.form.taxa_juros) return null
      const valorBase = this.editando ? this.form.saldo_devedor : this.form.valor
      if (!valorBase) return null
      const saldo = parseFloat(valorBase)
      const taxa = parseFloat(this.form.taxa_juros)
      const juros = saldo * (taxa / 100)
      return saldo + juros
    }
  },
  watch: {
    emprestimo: {
      immediate: true,
      handler(novo) {
        if (novo) {
          this.form = {
            cliente_id: novo.cliente_id,
            data: novo.data ? novo.data.split('T')[0] : new Date().toISOString().split('T')[0],
            data_vencimento: novo.data_vencimento ? novo.data_vencimento.split('T')[0] : '',
            valor: novo.valor_original || novo.valor,
            saldo_devedor: novo.saldo_devedor,
            taxa_juros: novo.taxa_juros,
            status: novo.status || 'em_aberto'
          }
        } else {
          this.resetarForm()
        }
      }
    },
    'form.data'(novaData) {
      if (!this.editando && novaData) {
        this.form.data_vencimento = this.calcularDataVencimento(novaData)
      }
    }
  },
  mounted() {
    this.buscarClientes()
    if (!this.emprestimo) {
      this.form.data_vencimento = this.calcularDataVencimento(this.form.data)
    }
  },
  methods: {
    calcularDataVencimento(dataEmprestimo) {
      const [ano, mes] = dataEmprestimo.split('-').map(Number)
      let novoMes = mes + 1
      let novoAno = ano
      if (novoMes > 12) {
        novoMes = 1
        novoAno = novoAno + 1
      }
      const dia = 5
      const dataVencimento = new Date(novoAno, novoMes - 1, dia)
      return dataVencimento.toISOString().split('T')[0]
    },
    async buscarClientes() {
      try {
        const resp = await axios.get('/api/clientes')
        this.clientes = resp.data
        if (this.clienteParaEmprestimo) {
          this.form.cliente_id = this.clienteParaEmprestimo.id
        } else if (this.clienteId) {
          this.form.cliente_id = this.clienteId
        }
      } catch (err) {
        console.error('Erro ao carregar clientes', err)
      }
    },
    resetarForm() {
      const dataHoje = new Date().toISOString().split('T')[0]
      const dataVencimento = this.calcularDataVencimento(dataHoje)
      this.form = {
        cliente_id: '',
        data: dataHoje,
        data_vencimento: dataVencimento,
        valor: '',
        saldo_devedor: '',
        taxa_juros: '30',
        status: 'em_aberto'
      }
    },
    async salvar() {
      try {
        if (!this.form.cliente_id || !this.form.taxa_juros) {
          alert('Preencha todos os campos obrigatórios')
          return
        }
        const valorCampo = this.editando ? this.form.saldo_devedor : this.form.valor
        if (!valorCampo) {
          alert('Preencha o valor')
          return
        }
        const dataToSend = {
          ...this.form,
          cliente_id: parseInt(this.form.cliente_id),
          valor: this.editando ? undefined : parseFloat(this.form.valor),
          saldo_devedor: this.editando ? parseFloat(this.form.saldo_devedor) : undefined,
          taxa_juros: parseFloat(this.form.taxa_juros)
        }
        if (this.editando) {
          await axios.put(`/api/emprestimos/${this.emprestimo.id}`, dataToSend)
        } else {
          await axios.post('/api/emprestimos', dataToSend)
        }
        this.$emit('salvo')
      } catch (err) {
        alert(err.response?.data?.erro || 'Erro ao salvar')
      }
    },
    formatarDinheiro(valor) {
      if (!valor) return 'R$ 0,00'
      return 'R$ ' + parseFloat(valor).toFixed(2).replace('.', ',')
    }
  }
}
</script>