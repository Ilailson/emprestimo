<template>
  <div class="card">
    <h2>{{ editando ? 'Editar Pagamento' : 'Registrar Pagamento' }}</h2>
    <form @submit.prevent="salvar">
      <div class="form-group">
        <label>Empréstimo</label>
        <select v-model="form.emprestimo_id" required :disabled="editando" @change="onEmprestimoChange">
          <option value="" disabled>Selecione um empréstimo</option>
          <option v-for="emp in emprestimos" :key="emp.id" :value="emp.id">
            {{ emp.cliente_nome }} - R$ {{ formatarDinheiro(emp.saldo_devedor) }} (Devedor)
          </option>
        </select>
      </div>

      <div class="info-box" v-if="emprestimoSelecionado">
        <p><strong>Cliente:</strong> {{ emprestimoSelecionado.cliente_nome }}</p>
        <p><strong>Valor Original:</strong> {{ formatarDinheiro(emprestimoSelecionado.valor_original) }}</p>
        <p><strong>Saldo Devedor:</strong> {{ formatarDinheiro(emprestimoSelecionado.saldo_devedor) }}</p>
        <p><strong>Juros do Mês:</strong> {{ formatarDinheiro(emprestimoSelecionado.juros) }}</p>
        <p><strong>Total com Juros:</strong> {{ formatarDinheiro(emprestimoSelecionado.valor_total) }}</p>
        <p><strong>Total Pago:</strong> {{ formatarDinheiro(emprestimoSelecionado.total_pago) }}</p>
      </div>

      <div class="pagamento-opcoes" v-if="emprestimoSelecionado">
        <h3>Escolha como pagar:</h3>

        <div class="opcao-pagamento">
          <label class="opcao-label">
            <input type="checkbox" v-model="pagarJuros" @change="atualizarValorTotal">
            Pagar Juros: R$ {{ formatarDinheiro(emprestimoSelecionado.juros) }}
          </label>
        </div>

        <div class="opcao-pagamento">
          <label class="opcao-label">
            <input type="checkbox" v-model="pagarSaldo" @change="atualizarValorTotal">
            Pagar Saldo Devedor
          </label>
          <div class="sub-opcao" v-if="pagarSaldo">
            <label>
              Valor a pagar no saldo:
              <input v-model="form.valor_saldo" type="number" step="0.01" min="0"
                     :max="emprestimoSelecionado.saldo_devedor"
                     placeholder="0.00"
                     @input="atualizarValorTotal">
            </label>
            <div class="valor-sugestoes">
              <button type="button" class="btn btn-sm" @click="sugerirValor(50)">50%</button>
              <button type="button" class="btn btn-sm" @click="sugerirValor(100)">100%</button>
            </div>
          </div>
        </div>
      </div>

      <div class="total-pagamento" v-if="emprestimoSelecionado">
        <h3>Total a Pagar: R$ {{ formatarDinheiro(valorTotal) }}</h3>
      </div>

      <div class="form-group">
        <label>Data do Pagamento</label>
        <input v-model="form.data" type="date" required>
      </div>

      <div class="actions">
        <button type="submit" class="btn btn-success">{{ editando ? 'Atualizar' : 'Registrar Pagamento' }}</button>
        <button type="button" class="btn" @click="$emit('cancelar')">Cancelar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PagamentosForm',
  props: {
    pagamento: { type: Object, default: null },
    clienteId: { type: Number, default: null },
    emprestimoId: { type: Number, default: null }
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
        total += this.emprestimoSelecionado.juros
      }
      if (this.pagarSaldo && this.form.valor_saldo) {
        total += parseFloat(this.form.valor_saldo)
      }
      return total
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
            data: novo.data ? novo.data.split('T')[0] : new Date().toISOString().split('T')[0]
          }
        } else {
          this.form = {
            emprestimo_id: '',
            valor_saldo: '',
            data: new Date().toISOString().split('T')[0]
          }
        }
      }
    }
  },
  mounted() {
    this.buscarEmprestimos()
  },
  methods: {
    async buscarEmprestimos() {
      try {
        let url = '/api/emprestimos'
        if (this.clienteId) {
          url = `/api/clientes/${this.clienteId}/emprestimos`
        }
        const resp = await axios.get(url)
        this.emprestimos = resp.data
        
        if (this.emprestimoId) {
          this.form.emprestimo_id = this.emprestimoId
          this.emprestimoSelecionado = this.emprestimos.find(e => e.id === this.emprestimoId)
          if (this.emprestimoSelecionado && this.emprestimoSelecionado.juros) {
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
      if (this.emprestimoSelecionado && this.emprestimoSelecionado.juros) {
        this.pagarJuros = true
      }
    },
    atualizarValorTotal() {
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
          valorFinal += this.emprestimoSelecionado.juros
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
          pagar_juros: this.pagarJuros,
          pagar_saldo: this.pagarSaldo ? parseFloat(this.form.valor_saldo || 0) : 0
        }

        if (this.editando) {
          await axios.put(`/api/pagamentos/${this.pagamento.id}`, dataToSend)
        } else {
          dataToSend.emprestimo_id = parseInt(this.form.emprestimo_id)
          await axios.post('/api/pagamentos', dataToSend)
        }
        this.$emit('salvo')
        this.limpar()
      } catch (err) {
        console.error('Erro ao salvar:', err)
        alert(err.response?.data?.erro || 'Erro ao salvar pagamento')
      }
    },
    limpar() {
      this.form = {
        emprestimo_id: '',
        valor_saldo: '',
        data: new Date().toISOString().split('T')[0]
      }
      this.emprestimoSelecionado = null
      this.pagarJuros = false
      this.pagarSaldo = false
    },
    formatarDinheiro(valor) {
      if (!valor) return '0,00'
      return parseFloat(valor).toFixed(2).replace('.', ',')
    }
  }
}
</script>

<style scoped>
.pagamento-opcoes {
  margin: 15px 0;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 5px;
}

.pagamento-opcoes h3 {
  margin-bottom: 10px;
  font-size: 14px;
}

.opcao-pagamento {
  margin: 10px 0;
  padding: 10px;
  background: white;
  border-radius: 5px;
}

.opcao-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.opcao-label input[type="checkbox"] {
  width: auto;
}

.sub-opcao {
  margin-top: 10px;
  margin-left: 25px;
}

.sub-opcao input {
  margin-left: 10px;
}

.valor-sugestoes {
  margin-top: 5px;
  display: flex;
  gap: 5px;
}

.total-pagamento {
  text-align: center;
  padding: 15px;
  background: #4CAF50;
  color: white;
  border-radius: 5px;
  margin: 15px 0;
}

.total-pagamento h3 {
  margin: 0;
}
</style>