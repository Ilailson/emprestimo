<template>
  <div class="card">
    <div class="header-list">
      <h2>Pagamentos</h2>
      <button class="btn btn-primary" @click="$emit('novo')">+ Novo Pagamento</button>
    </div>

    <div v-if="mensagem" :class="mensagem_tipo">{{ mensagem }}</div>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Cliente</th>
          <th>Valor</th>
          <th>Tipo</th>
          <th>Data</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pag in pagamentos" :key="pag.id">
          <td>{{ pag.id }}</td>
          <td>{{ pag.emprestimo_nome }}</td>
          <td>{{ formatarDinheiro(pag.valor) }}</td>
          <td>
            <span v-if="pag.is_juros" class="badge badge-warning">Juros</span>
            <span v-else class="badge badge-success">Valor e juros</span>
          </td>
          <td>{{ formatarData(pag.data) }}</td>
          <td class="actions">
            <button class="btn btn-danger btn-sm" @click="excluir(pag.id)">Excluir</button>
          </td>
        </tr>
        <tr v-if="pagamentos.length === 0">
          <td colspan="6" style="text-align: center">Nenhum pagamento registrado</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PagamentosList',
  emits: ['novo'],
  data() {
    return {
      pagamentos: [],
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
        const resp = await axios.get('/api/pagamentos')
        this.pagamentos = resp.data
      } catch (err) {
        this.exibirMensagem('Erro ao carregar pagamentos', 'error')
      }
    },
    async excluir(id) {
      if (!confirm('Tem certeza que deseja excluir este pagamento?')) return
      try {
        await axios.delete(`/api/pagamentos/${id}`)
        this.exibirMensagem('Pagamento excluído com sucesso', 'success')
        this.buscar()
      } catch (err) {
        this.exibirMensagem(err.response?.data?.erro || 'Erro ao excluir', 'error')
      }
    },
    exibirMensagem(texto, tipo) {
      this.mensagem = texto
      this.mensagem_tipo = tipo
      setTimeout(() => { this.mensagem = '' }, 3000)
    },
    verDetalhes(pag) {
      const tipo = pag.is_juros ? 'Juros' : 'Principal'
      alert(`Pagamento #${pag.id}\nCliente: ${pag.emprestimo_nome}\nValor: R$ ${pag.valor}\nTipo: ${tipo}\nData: ${this.formatarData(pag.data)}`)
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
