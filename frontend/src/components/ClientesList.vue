<template>
  <div class="card">
    <div class="header-list">
      <h2>Lista de Clientes</h2>
      <button class="btn btn-primary" @click="$emit('novo')">+ Novo Cliente</button>
    </div>
    <div v-if="mensagem" :class="mensagem_tipo">{{ mensagem }}</div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nome</th>
          <th>Telefone</th>
          <th>Endereço</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cliente in clientes" :key="cliente.id">
            <td>{{ cliente.id }}</td>
            <td>{{ cliente.nome }}</td>
            <td>{{ formatarTelefone(cliente.telefone) }}</td>
            <td>{{ cliente.endereco || '-' }}</td>
            <td class="actions">
              <button class="btn btn-warning" @click="$emit('editar', cliente)">Editar</button>
              <button class="btn btn-danger" @click="excluir(cliente.id)">Excluir</button>
            </td>
        </tr>
        <tr v-if="clientes.length === 0">
          <td colspan="5" style="text-align: center">Nenhum cliente cadastrado</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ClientesList',
  emits: ['editar', 'novo'],
  data() {
    return {
      clientes: [],
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
        const resp = await axios.get('/api/clientes')
        this.clientes = resp.data
      } catch (err) {
        this.exibirMensagem('Erro ao carregar clientes', 'error')
      }
    },
    async excluir(id) {
      if (!confirm('Tem certeza que deseja excluir?')) return
      try {
        await axios.delete(`/api/clientes/${id}`)
        this.exibirMensagem('Cliente excluído com sucesso', 'success')
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
    formatarTelefone(tel) {
      if (!tel) return '-'
      tel = tel.replace(/\D/g, '')
      if (tel.length > 2) {
        tel = '(' + tel.substring(0, 2) + ')' + tel.substring(2)
      }
      if (tel.length > 9) {
        tel = tel.substring(0, 9) + '-' + tel.substring(9, 13)
      }
      return tel
    }
  }
}
</script>