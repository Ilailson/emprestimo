<template>
  <div class="container">
    <h1>Sistema de Empréstimos</h1>
    <div class="tabs">
      <button class="tab" :class="{ active: abaAtiva === 'listar' }" @click="abaAtiva = 'listar'">Clientes</button>
    </div>

    <!-- Listagem de Clientes -->
    <ClientesList v-if="abaAtiva === 'listar'" @editar="editarCliente" @novo="novoCliente" />

    <!-- Formulário de Cliente -->
    <ClientesForm 
      v-if="abaAtiva === 'form'" 
      :cliente="clienteSelecionado" 
      @salvo="aoSalvar" 
      @cancelar="abaAtiva = 'listar'" 
    />
  </div>
</template>

<script>
import ClientesList from './components/ClientesList.vue'
import ClientesForm from './components/ClientesForm.vue'

export default {
  name: 'App',
  components: { ClientesList, ClientesForm },
  data() {
    return {
      abaAtiva: 'listar',
      clienteSelecionado: null
    }
  },
  methods: {
    novoCliente() {
      this.clienteSelecionado = null
      this.abaAtiva = 'form'
    },
    editarCliente(cliente) {
      this.clienteSelecionado = cliente
      this.abaAtiva = 'form'
    },
    aoSalvar() {
      this.clienteSelecionado = null
      this.abaAtiva = 'listar'
    }
  }
}
</script>