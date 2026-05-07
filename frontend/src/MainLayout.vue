<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <!-- Mobile Header -->
    <header class="lg:hidden fixed top-0 left-0 right-0 h-14 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-4 z-50">
      <button @click="sidebarAberta = !sidebarAberta" class="p-2 -ml-2 rounded-lg hover:bg-slate-800 transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>
      <h1 class="text-base font-semibold truncate">Sistema de Empréstimos</h1>
      <div class="w-8"></div>
    </header>

    <!-- Sidebar Overlay (mobile) -->
    <div v-if="sidebarAberta" @click="sidebarAberta = false" class="lg:hidden fixed inset-0 bg-black/50 z-40"></div>

    <!-- Sidebar -->
    <aside :class="[
      'fixed top-0 left-0 h-full w-64 bg-slate-900 border-r border-slate-800 z-50 transition-transform duration-300',
      sidebarAberta ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
    ]">
      <div class="p-4 border-b border-slate-800">
        <h2 class="text-lg font-bold flex items-center gap-2">
          <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span class="text-base">Empréstimos</span>
        </h2>
      </div>

      <nav class="p-3 space-y-1">
        <button @click="abaAtiva = 'clientes'; sidebarAberta = false" :class="[
          'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left',
          abaAtiva === 'clientes' ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
        ]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.357-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.357-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          <span class="text-sm font-medium">Clientes</span>
        </button>

        <button @click="abaAtiva = 'emprestimos'; sidebarAberta = false" :class="[
          'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left',
          abaAtiva === 'emprestimos' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/25' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
        ]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
          </svg>
          <span class="text-sm font-medium">Empréstimos</span>
        </button>

        <button @click="abaAtiva = 'pagamentos'; sidebarAberta = false" :class="[
          'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left',
          abaAtiva === 'pagamentos' ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/25' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
        ]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
          </svg>
          <span class="text-sm font-medium">Pagamentos</span>
        </button>

        <button @click="abaAtiva = 'pendentes'; sidebarAberta = false" :class="[
          'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left',
          abaAtiva === 'pendentes' ? 'bg-orange-600 text-white shadow-lg shadow-orange-500/25' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
        ]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M9 3h6l1 3h4a1 1 0 011 1v3a1 1 0 01-1 1h-1v8a2 2 0 01-2 2H7a2 2 0 01-2-2v-8H4a1 1 0 01-1-1V7a1 1 0 011-1h4l1-3z"/>
          </svg>
          <span class="text-sm font-medium">Pendentes</span>
        </button>

        <button @click="abaAtiva = 'dashboard'; sidebarAberta = false" :class="[
          'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left',
          abaAtiva === 'dashboard' ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/25' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
        ]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/>
          </svg>
          <span class="text-sm font-medium">Dashboard</span>
        </button>

        <button @click="abaAtiva = 'relatorios'; sidebarAberta = false" :class="[
  'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left',
  abaAtiva === 'relatorios' ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/25' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
]">
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
  </svg>
  <span class="text-sm font-medium">Relatórios</span>
</button>
      </nav>

      <!-- Admin: Usuários -->
      <div v-if="authStore.isAdmin" class="p-3 border-t border-slate-800">
        <button @click="abaAtiva = 'usuarios'; sidebarAberta = false" :class="[
          'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left',
          abaAtiva === 'usuarios' ? 'bg-violet-600 text-white shadow-lg shadow-violet-500/25' : 'text-slate-400 hover:bg-violet-600/20 hover:text-violet-400'
        ]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
          </svg>
          <span class="text-sm font-medium">Usuários</span>
        </button>
      </div>

      <!-- Alterar Senha -->
      <div class="p-3 border-t border-slate-800">
        <button @click="irAlterarSenha" class="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left text-slate-400 hover:bg-amber-600/20 hover:text-amber-400">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
          <span class="text-sm font-medium">Alterar Senha</span>
        </button>
      </div>

      <!-- Logout Button -->
      <div class="p-3 border-t border-slate-800">
        <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left text-slate-400 hover:bg-red-600/20 hover:text-red-400">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          <span class="text-sm font-medium">Sair</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="lg:ml-64 pt-14 lg:pt-0 min-h-screen">
      <div class="p-4 lg:p-6 space-y-4 lg:space-y-6">
        <!-- Dashboard View -->
        <template v-if="abaAtiva === 'dashboard'">
          <DashboardMetrics @navigate="abaAtiva = $event" />
        </template>

        <!-- Clientes -->
        <template v-if="abaAtiva === 'clientes'">
          <ClientesList v-if="!mostrarFormCliente" @editar="editarCliente" @novo="novoCliente" @verEmprestimos="verEmprestimosCliente" />
          <ClientesForm
            v-else
            :cliente="clienteSelecionado"
            @salvo="aoSalvarCliente"
            @cancelar="cancelarFormCliente"
            @criadoComEmprestimo="aoCriarComEmprestimo"
          />
        </template>

        <!-- Empréstimos -->
        <template v-if="abaAtiva === 'emprestimos'">
          <EmprestimosList v-if="!mostrarFormEmprestimo" :cliente-id="filtroClienteId" @editar="editarEmprestimo" @novo="novoEmprestimo" @voltar="voltarEmprestimos" @fazerPagamento="fazerPagamentoEmprestimo" />
          <EmprestimosForm
            v-else
            :emprestimo="emprestimoSelecionado"
            :cliente-id="filtroClienteId"
            :clienteParaEmprestimo="clienteParaEmprestimo"
            @salvo="aoSalvarEmprestimo"
            @cancelar="cancelarFormEmprestimo"
          />
        </template>

        <!-- Pagamentos -->
        <template v-if="abaAtiva === 'pagamentos'">
          <PagamentosList v-if="!mostrarFormPagamento" :cliente-id="filtroClienteIdPagamentos" :emprestimo-id="filtroEmprestimoId" @novo="novoPagamento" @voltar="voltarPagamentos" />
          <PagamentosForm
            v-else
            :pagamento="pagamentoSelecionado"
            :cliente-id="filtroClienteIdPagamentos"
            :emprestimo-id="emprestimoIdParaPagamento"
            @salvo="aoSalvarPagamento"
            @cancelar="cancelarFormPagamento"
          />
        </template>

        <template v-if="abaAtiva === 'pendentes'">
          <PagamentosPendentes
            v-if="!mostrarFormPagamentoPendentes"
            :key="pendentesRefreshKey"
            @fazerPagamento="fazerPagamentoPendente"
          />
          <PagamentosForm
            v-else
            :emprestimo-id="emprestimoIdPagamentoPendente"
            :data-pagamento-padrao="dataPagamentoPendente"
            :bloquear-data-pagamento="true"
            @salvo="aoSalvarPagamentoPendente"
            @cancelar="cancelarFormPagamentoPendente"
          />
        </template>

        <!-- Usuários -->
        <template v-if="abaAtiva === 'usuarios'">
          <UsuariosList v-if="!mostrarFormUsuario" @novo="novoUsuario" @editar="editarUsuario" />
          <UsuariosForm
            v-else
            :usuario="usuarioSelecionado"
            @salvo="aoSalvarUsuario"
            @cancelar="cancelarFormUsuario"
          />
        </template>

        <!-- Relatórios -->
        <template v-if="abaAtiva === 'relatorios'">
          <RelatoriosList />
        </template>

        </div>
    </main>
    <InstallPrompt />
  </div>
</template>

<script>
import ClientesList from './components/ClientesList.vue'
import ClientesForm from './components/ClientesForm.vue'
import EmprestimosList from './components/EmprestimosList.vue'
import EmprestimosForm from './components/EmprestimosForm.vue'
import PagamentosList from './components/PagamentosList.vue'
import PagamentosForm from './components/PagamentosForm.vue'
import PagamentosPendentes from './components/PagamentosPendentes.vue'
import DashboardMetrics from './components/DashboardMetrics.vue'
import RelatoriosList from './components/RelatoriosList.vue'
import UsuariosList from './components/UsuariosList.vue'
import UsuariosForm from './components/UsuariosForm.vue'
import InstallPrompt from './components/InstallPrompt.vue'
import { useAuthStore } from './store/auth'

export default {
  name: 'MainLayout',
  components: { ClientesList, ClientesForm, EmprestimosList, EmprestimosForm, PagamentosList, PagamentosForm, PagamentosPendentes, DashboardMetrics, InstallPrompt, RelatoriosList, UsuariosList, UsuariosForm },
  data() {
    return {
      abaAtiva: 'dashboard',
      clienteSelecionado: null,
      mostrarFormCliente: false,
      emprestimoSelecionado: null,
      mostrarFormEmprestimo: false,
      clienteParaEmprestimo: null,
      pagamentoSelecionado: null,
      mostrarFormPagamento: false,
      mostrarFormPagamentoPendentes: false,
      filtroClienteId: null,
      filtroClienteIdPagamentos: null,
      filtroEmprestimoId: null,
      emprestimoIdParaPagamento: null,
      emprestimoIdPagamentoPendente: null,
      dataPagamentoPendente: null,
      pendentesRefreshKey: 0,
      mostrarRelatorios: false,
      sidebarAberta: false,
      usuarioSelecionado: null,
      mostrarFormUsuario: false
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    }
  },
  methods: {
    irAlterarSenha() {
      this.$router.push('/alterar-senha')
    },
    novoUsuario() {
      this.usuarioSelecionado = null
      this.mostrarFormUsuario = true
      this.abaAtiva = 'usuarios'
    },
    editarUsuario(usuario) {
      this.usuarioSelecionado = usuario
      this.mostrarFormUsuario = true
      this.abaAtiva = 'usuarios'
    },
    aoSalvarUsuario() {
      this.usuarioSelecionado = null
      this.mostrarFormUsuario = false
      this.abaAtiva = 'usuarios'
    },
    cancelarFormUsuario() {
      this.usuarioSelecionado = null
      this.mostrarFormUsuario = false
    },
    handleLogout() {
      this.authStore.logout()
      window.location.href = '/login'
    },
    novoCliente() {
      this.clienteSelecionado = null
      this.mostrarFormCliente = true
      this.abaAtiva = 'clientes'
    },
    editarCliente(cliente) {
      this.clienteSelecionado = cliente
      this.mostrarFormCliente = true
      this.abaAtiva = 'clientes'
    },
    aoSalvarCliente() {
      this.clienteSelecionado = null
      this.mostrarFormCliente = false
      this.abaAtiva = 'clientes'
    },
    aoCriarComEmprestimo(cliente) {
      this.clienteSelecionado = null
      this.mostrarFormCliente = false
      this.abaAtiva = 'clientes'
      this.clienteParaEmprestimo = cliente
      this.mostrarFormEmprestimo = true
      this.abaAtiva = 'emprestimos'
    },
    novoEmprestimo(clienteId) {
      this.emprestimoSelecionado = null
      this.mostrarFormEmprestimo = true
      this.clienteParaEmprestimo = null
      if (clienteId) {
        this.filtroClienteId = clienteId
      }
      this.abaAtiva = 'emprestimos'
    },
    editarEmprestimo(emprestimo) {
      if (emprestimo.status === 'pago') {
        alert('Não é possível editar empréstimo pago')
        return
      }
      this.emprestimoSelecionado = emprestimo
      this.mostrarFormEmprestimo = true
      this.abaAtiva = 'emprestimos'
    },
    verEmprestimosCliente(cliente) {
      this.filtroClienteId = cliente.id
      this.abaAtiva = 'emprestimos'
    },
    fazerPagamentoEmprestimo(emprestimo) {
      if (emprestimo.status === 'pago') {
        alert('Empréstimo já está pago')
        return
      }
      this.emprestimoIdParaPagamento = emprestimo.id
      this.filtroEmprestimoId = emprestimo.id
      this.pagamentoSelecionado = null
      this.mostrarFormPagamento = true
      this.abaAtiva = 'pagamentos'
    },
    verPagamentosCliente(cliente) {
      this.filtroClienteIdPagamentos = cliente.id
      this.abaAtiva = 'pagamentos'
    },
    fazerPagamentoPendente(pendente) {
      this.pagamentoSelecionado = null
      this.emprestimoIdPagamentoPendente = pendente.emprestimo_id
      this.dataPagamentoPendente = pendente.data_referencia
      this.mostrarFormPagamentoPendentes = true
      this.abaAtiva = 'pendentes'
    },
    aoSalvarEmprestimo() {
      const voltarParaClientes = this.clienteParaEmprestimo !== null
      this.emprestimoSelecionado = null
      this.mostrarFormEmprestimo = false
      this.clienteParaEmprestimo = null
      this.abaAtiva = voltarParaClientes ? 'clientes' : 'emprestimos'
    },
    novoPagamento() {
      this.pagamentoSelecionado = null
      this.mostrarFormPagamento = true
      this.emprestimoIdParaPagamento = this.filtroEmprestimoId
      this.abaAtiva = 'pagamentos'
    },
    voltarPagamentos() {
      this.mostrarFormPagamento = false
      if (this.filtroEmprestimoId) {
        this.filtroEmprestimoId = null
        this.abaAtiva = 'emprestimos'
      } else if (this.filtroClienteIdPagamentos) {
        this.filtroClienteIdPagamentos = null
        this.abaAtiva = 'clientes'
      } else {
        this.abaAtiva = 'clientes'
      }
    },
    voltarEmprestimos() {
      this.filtroClienteId = null
      this.abaAtiva = 'clientes'
    },
    editarPagamento(pagamento) {
      this.pagamentoSelecionado = pagamento
      this.mostrarFormPagamento = true
      this.abaAtiva = 'pagamentos'
    },
    aoSalvarPagamento() {
      this.pagamentoSelecionado = null
      this.mostrarFormPagamento = false
      this.emprestimoIdParaPagamento = null
      this.abaAtiva = 'pagamentos'
    },
    aoSalvarPagamentoPendente() {
      this.mostrarFormPagamentoPendentes = false
      this.emprestimoIdPagamentoPendente = null
      this.dataPagamentoPendente = null
      this.pendentesRefreshKey += 1
      this.abaAtiva = 'pendentes'
    },
    cancelarFormCliente() {
      this.clienteSelecionado = null
      this.mostrarFormCliente = false
    },
    cancelarFormEmprestimo() {
      this.emprestimoSelecionado = null
      this.mostrarFormEmprestimo = false
    },
    cancelarFormPagamento() {
      this.pagamentoSelecionado = null
      this.mostrarFormPagamento = false
    },
    cancelarFormPagamentoPendente() {
      this.mostrarFormPagamentoPendentes = false
      this.emprestimoIdPagamentoPendente = null
      this.dataPagamentoPendente = null
      this.abaAtiva = 'pendentes'
    },
  }
}
</script>
