<template>
  <div class="card">
    <div class="header-list">
      <h2>Lista de Empréstimos</h2>
      <button class="btn btn-primary" @click="$emit('novo')">+ Novo Empréstimo</button>
    </div>
    <div v-if="mensagem" :class="mensagem_tipo">{{ mensagem }}</div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Cliente</th>
          <th>Valor Original</th>
          <th>Taxa</th>
          <th>Saldo Devedor</th>
          <th>Total Pago</th>
          <th>Juros</th>
          <th>Total</th>
          <th>Data</th>
          <th>Vencimento</th>
          <th>Status</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="emp in emprestimos" :key="emp.id" :class="getStatusClass(emp)">
          <td>{{ emp.id }}</td>
          <td>{{ emp.cliente_nome }}</td>
          <td>{{ formatarDinheiro(emp.valor_original) }}</td>
          <td>{{ emp.taxa_juros }}%</td>
          <td>{{ formatarDinheiro(emp.saldo_devedor) }}</td>
          <td>{{ formatarDinheiro(emp.total_pago) }}</td>
          <td>{{ formatarDinheiro(emp.juros) }}</td>
          <td>{{ formatarDinheiro(emp.valor_total) }}</td>
          <td>{{ formatarData(emp.data) }}</td>
          <td>{{ formatarData(emp.data_vencimento) }}</td>
          <td>
            <span :class="'badge badge-' + getStatusBadge(emp)">
              {{ getStatusLabel(emp) }}
            </span>
          </td>
          <td class="actions">
            <button class="btn btn-sm" @click="verDetalhes(emp)">Ver</button>
            <button class="btn btn-warning btn-sm" @click="$emit('editar', emp)">Editar</button>
            <button class="btn btn-danger btn-sm" @click="excluir(emp.id)">Excluir</button>
          </td>
        </tr>
        <tr v-if="emprestimos.length === 0">
          <td colspan="11" style="text-align: center">Nenhum empréstimo cadastrado</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EmprestimosList',
  emits: ['editar', 'novo'],
  data() {
    return {
      emprestimos: [],
      mensagem: '',
      mensagem_tipo: ''
    }
  },
  mounted() {
    this.buscar()
  },
  methods: {
    async buscar() {
      try {
        const resp = await axios.get('/api/emprestimos')
        this.emprestimos = resp.data
      } catch (err) {
        this.exibirMensagem('Erro ao carregar empréstimos', 'error')
      }
    },
    async excluir(id) {
      if (!confirm('Tem certeza que deseja excluir?')) return
      try {
        await axios.delete(`/api/emprestimos/${id}`)
        this.exibirMensagem('Empréstimo excluído com sucesso', 'success')
        this.buscar()
      } catch (err) {
        this.exibirMensagem(err.response?.data?.erro || 'Erro ao excluir', 'error')
      }
    },
    verDetalhes(emp) {
      alert(`Cliente: ${emp.cliente_nome}\nValor Original: R$ ${emp.valor_original}\nTaxa: ${emp.taxa_juros}%\nSaldo Devedor: R$ ${emp.saldo_devedor}\nTotal Pago: R$ ${emp.total_pago}\nJuros: R$ ${emp.juros}\nTotal com Juros: R$ ${emp.valor_total}`)
    },
    getStatusClass(emp) {
      if (emp.status === 'pago') return 'row-pago'
      const devedor = emp.saldo_devedor || 0
      if (devedor > 0 && emp.data_vencimento) {
        const dataVencto = new Date(emp.data_vencimento)
        if (new Date() > dataVencto) return 'row-atrasado'
      }
      return ''
    },
    getStatusBadge(emp) {
      if (emp.status === 'pago') return 'success'
      const devedor = emp.saldo_devedor || 0
      if (devedor > 0 && emp.data_vencimento) {
        const dataVencto = new Date(emp.data_vencimento)
        if (new Date() > dataVencto) return 'danger'
      }
      return 'warning'
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