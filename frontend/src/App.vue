<template>
  <div class="container">
    <h1>Sistema de Empréstimos</h1>
    <div class="tabs">
      <button class="tab" :class="{ active: abaAtiva === 'clientes' }" @click="abaAtiva = 'clientes'">Clientes</button>
      <button class="tab" :class="{ active: abaAtiva === 'emprestimos' }" @click="abaAtiva = 'emprestimos'">Empréstimos</button>
      <button class="tab" :class="{ active: abaAtiva === 'pagamentos' }" @click="abaAtiva = 'pagamentos'">Pagamentos</button>
    </div>

    <!-- Listagem de Clientes -->
    <ClientesList v-if="abaAtiva === 'clientes'" @editar="editarCliente" @novo="novoCliente" />

    <!-- Formulário de Cliente -->
    <ClientesForm 
      v-if="abaAtiva === 'form-cliente'" 
      :cliente="clienteSelecionado" 
      @salvo="aoSalvarCliente" 
      @cancelar="abaAtiva = 'clientes'"
      @criadoComEmprestimo="aoCriarComEmprestimo"
    />

    <!-- Listagem de Empréstimos -->
    <EmprestimosList v-if="abaAtiva === 'emprestimos'" @editar="editarEmprestimo" @novo="novoEmprestimo" />

    <!-- Formulário de Empréstimo -->
    <EmprestimosForm 
      v-if="abaAtiva === 'form-emprestimo'" 
      :emprestimo="emprestimoSelecionado" 
      :clienteParaEmprestimo="clienteParaEmprestimo"
      @salvo="aoSalvarEmprestimo" 
      @cancelar="abaAtiva = 'emprestimos'" 
    />

    <!-- Listagem de Pagamentos -->
    <PagamentosList v-if="abaAtiva === 'pagamentos'" @novo="novoPagamento" />

    <!-- Formulário de Pagamento -->
    <PagamentosForm 
      v-if="abaAtiva === 'form-pagamento'" 
      :pagamento="pagamentoSelecionado"
      @salvo="aoSalvarPagamento" 
      @cancelar="abaAtiva = 'pagamentos'" 
    />
  </div>
</template>

<script>
import ClientesList from './components/ClientesList.vue'
import ClientesForm from './components/ClientesForm.vue'
import EmprestimosList from './components/EmprestimosList.vue'
import EmprestimosForm from './components/EmprestimosForm.vue'
import PagamentosList from './components/PagamentosList.vue'
import PagamentosForm from './components/PagamentosForm.vue'

export default {
  name: 'App',
  components: { ClientesList, ClientesForm, EmprestimosList, EmprestimosForm, PagamentosList, PagamentosForm },
  data() {
    return {
      abaAtiva: 'clientes',
      clienteSelecionado: null,
      emprestimoSelecionado: null,
      clienteParaEmprestimo: null,
      pagamentoSelecionado: null
    }
  },
  methods: {
    novoCliente() {
      this.clienteSelecionado = null
      this.abaAtiva = 'form-cliente'
    },
    editarCliente(cliente) {
      this.clienteSelecionado = cliente
      this.abaAtiva = 'form-cliente'
    },
    aoSalvarCliente() {
      this.clienteSelecionado = null
      this.abaAtiva = 'clientes'
    },
    aoCriarComEmprestimo(cliente) {
      this.clienteSelecionado = null
      this.abaAtiva = 'clientes'
      this.clienteParaEmprestimo = cliente
      this.abaAtiva = 'form-emprestimo'
    },
    novoEmprestimo() {
      this.emprestimoSelecionado = null
      this.abaAtiva = 'form-emprestimo'
    },
    editarEmprestimo(emprestimo) {
      this.emprestimoSelecionado = emprestimo
      this.abaAtiva = 'form-emprestimo'
    },
    aoSalvarEmprestimo() {
      this.emprestimoSelecionado = null
      this.clienteParaEmprestimo = null
      this.abaAtiva = 'emprestimos'
    },
    novoPagamento() {
      this.pagamentoSelecionado = null
      this.abaAtiva = 'form-pagamento'
    },
    editarPagamento(pagamento) {
      this.pagamentoSelecionado = pagamento
      this.abaAtiva = 'form-pagamento'
    },
    aoSalvarPagamento() {
      this.pagamentoSelecionado = null
      this.abaAtiva = 'pagamentos'
    }
  }
}
</script>