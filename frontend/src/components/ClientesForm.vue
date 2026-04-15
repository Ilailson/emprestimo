<template>
  <div class="card">
    <h2>{{ editando ? 'Editar Cliente' : 'Novo Cliente' }}</h2>
    <form @submit.prevent="salvar">
      <div class="form-group">
        <label>Nome</label>
        <input v-model="form.nome" required placeholder="Nome completo">
      </div>
      <div class="form-group">
        <label>Telefone</label>
        <input v-model="form.telefone" required placeholder="(00) 00000-0000" @input="formatarTelefone" maxlength="14">
      </div>
      <div class="form-group">
        <label>Endereço</label>
        <input v-model="form.endereco" placeholder="Endereço completo">
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
  name: 'ClientesForm',
  props: {
    cliente: { type: Object, default: null }
  },
  emits: ['salvo', 'cancelar'],
  data() {
    return {
      form: {
        nome: '',
        telefone: '',
        endereco: ''
      }
    }
  },
  computed: {
    editando() {
      return this.cliente !== null
    }
  },
  watch: {
    cliente: {
      immediate: true,
      handler(novo) {
        if (novo) {
          this.form = { nome: novo.nome, telefone: novo.telefone, endereco: novo.endereco }
        } else {
          this.form = { nome: '', telefone: '', endereco: '' }
        }
      }
    }
  },
  methods: {
    formatarTelefone() {
      let tel = this.form.telefone.replace(/\D/g, '')
      if (tel.length > 2) {
        tel = '(' + tel.substring(0, 2) + ')' + tel.substring(2)
      }
      if (tel.length > 9) {
        tel = tel.substring(0, 9) + '-' + tel.substring(9, 13)
      }
      this.form.telefone = tel
    },
    async salvar() {
      try {
        if (this.editando) {
          await axios.put(`/api/clientes/${this.cliente.id}`, this.form)
        } else {
          await axios.post('/api/clientes', this.form)
        }
        this.$emit('salvo')
        this.limpar()
      } catch (err) {
        alert(err.response?.data?.erro || 'Erro ao salvar')
      }
    },
    limpar() {
      this.form = { nome: '', telefone: '', endereco: '' }
    },
    cancelar() {
      this.$emit('cancelar')
    }
  }
}
</script>