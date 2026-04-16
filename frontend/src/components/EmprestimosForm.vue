<template>
  <div class="card">
    <h2>{{ editando ? 'Editar Empréstimo' : 'Novo Empréstimo' }}</h2>
    <form @submit.prevent="salvar">
      <div class="form-group">
        <label>Cliente</label>
        <select v-model="form.cliente_id" required>
          <option value="" disabled>Selecione um cliente</option>
          <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nome }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>Data do Empréstimo</label>
        <input v-model="form.data" type="date" required>
      </div>
      <div class="form-group">
        <label>Valor do Empréstimo (R$)</label>
        <input v-model="form.valor" type="number" step="0.01" min="1" required placeholder="1000.00">
      </div>
      <div class="form-group">
        <label>Taxa de Juros (% ao mês)</label>
        <input v-model="form.taxa_juros" type="number" step="0.1" min="0" max="100" required placeholder="5">
      </div>
      <div class="form-group" v-if="editando">
        <label>Status</label>
        <select v-model="form.status">
          <option value="em_aberto">Em Aberto</option>
          <option value="pago">Pago</option>
        </select>
      </div>
      <div class="info-box" v-if="previewTotal">
        <p><strong>Valor Total com Juros:</strong> {{ formatarDinheiro(previewTotal) }}</p>
        <p><strong>Tempo estimado:</strong> 1 mês</p>
      </div>
      <div class="actions">
        <button type="submit" class="btn btn-success">{{ editando ? 'Atualizar' : 'Cadastrar' }}</button>
        <button type="button" class="btn" @click="cancelar">Cancelar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EmprestimosForm',
  props: {
    emprestimo: { type: Object, default: null }
  },
  emits: ['salvo', 'cancelar'],
  data() {
    return {
      form: {
        cliente_id: '',
        data: new Date().toISOString().split('T')[0],
        valor: '',
        taxa_juros: '',
        status: 'em_aberto'
      },
      clientes: []
    }
  },
  computed: {
    editando() {
      return this.emprestimo !== null
    },
    previewTotal() {
      if (!this.form.valor || !this.form.taxa_juros) return null
      const valor = parseFloat(this.form.valor)
      const taxa = parseFloat(this.form.taxa_juros)
      return valor * (1 + taxa / 100)
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
            valor: novo.valor,
            taxa_juros: novo.taxa_juros,
            status: novo.status || 'em_aberto'
          }
        } else {
          this.form = {
            cliente_id: '',
            data: new Date().toISOString().split('T')[0],
            valor: '',
            taxa_juros: '',
            status: 'em_aberto'
          }
        }
      }
    }
  },
  mounted() {
    this.buscarClientes()
  },
  methods: {
    async buscarClientes() {
      try {
        const resp = await axios.get('/api/clientes')
        this.clientes = resp.data
      } catch (err) {
        console.error('Erro ao carregar clientes', err)
      }
    },
    async salvar() {
      try {
        if (this.editando) {
          await axios.put(`/api/emprestimos/${this.emprestimo.id}`, this.form)
        } else {
          await axios.post('/api/emprestimos', this.form)
        }
        this.$emit('salvo')
        this.limpar()
      } catch (err) {
        alert(err.response?.data?.erro || 'Erro ao salvar')
      }
    },
    limpar() {
      this.form = {
        cliente_id: '',
        data: new Date().toISOString().split('T')[0],
        valor: '',
        taxa_juros: '',
        status: 'em_aberto'
      }
    },
    cancelar() {
      this.$emit('cancelar')
    },
    formatarDinheiro(valor) {
      if (!valor) return 'R$ 0,00'
      return 'R$ ' + parseFloat(valor).toFixed(2).replace('.', ',')
    }
  }
}
</script>