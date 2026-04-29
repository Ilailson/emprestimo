# Arquitetura do Sistema de Empréstimos

## 1. Visão Geral

Sistema web para controle de empréstimos de dinheiro com cálculo de juros sobre saldo devedor.

### Tecnologias
- **Backend:** Python 3.x com Flask
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy
- **Frontend:** Vue.js 3 (Composition API)
- **Build Tool:** Vite

---

## 2. Arquitetura de Pastas

```
Emprestimo/
├── backend/
│   ├── app.py                      # Ponto de entrada Flask
│   ├── config.py                   # Configurações (DB, JWT)
│   ├── extensions.py               # Extensões SQLAlchemy
│   ├── requirements.txt            # Dependências Python
│   │
│   ├── models/                    # Modelos do banco
│   │   ├── __init__.py
│   │   ├── cliente.py            # Modelo Cliente
│   │   ├── emprestimo.py        # Modelo Emprestimo
│   │   └── pagamento.py          # Modelo Pagamento
│   │
│   ├── routes/                   # Rotas API REST
│   │   ├── __init__.py
│   │   ├── cliente_routes.py    # CRUD Clientes
│   │   ├── emprestimo_routes.py # CRUD Empréstimos
│   │   └── pagamento_routes.py   # CRUD Pagamentos
│   │
│   ├── migrate_*.py              # Scripts de migração
│   ├── seed/
│   │   └── seed.py              # Dados iniciais
│   └── venv/                     # Ambiente virtual
│
├── frontend/
│   ├── src/
│   │   ├── main.js              # Entry point Vue
│   │   ├── App.vue              # Componente raiz
│   │   ├── style.css            # Estilos globais
│   │   └── components/           # Componentes Vue
│   │       ├── ClientesList.vue
│   │       ├── ClientesForm.vue
│   │       ├── EmprestimosList.vue
│   │       ├── EmprestimosForm.vue
│   │       ├── PagamentosList.vue
│   │       └── PagamentosForm.vue
│   │
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── RELATORIO.md
```

---

## 3. Modelos de Dados

### 3.1 Cliente
```
clientes
├── id (PK)          INTEGER
├── nome             VARCHAR(100)     NOT NULL
├── telefone         VARCHAR(20)      NOT NULL
├── endereco         VARCHAR(200)
├── created_at       DATETIME
└── Relacionamentos:
    └── emprestimos (1:N)
```

### 3.2 Emprestimo
```
emprestimos
├── id (PK)              INTEGER
├── valor_original       FLOAT           NOT NULL
├── taxa_juros          FLOAT           NOT NULL
├── data                DATETIME
├── data_vencimento     DATETIME
├── data_ultimo_calculo DATETIME
├── saldo_devedor       FLOAT
├── total_pago          FLOAT           DEFAULT 0
├── status              VARCHAR(20)     DEFAULT 'em_aberto'
├── cliente_id (FK)     INTEGER         REFERENCES clientes(id)
└── Relacionamentos:
    ├── cliente (N:1)
    └── pagamentos (1:N)
```

### 3.3 Pagamento
```
pagamentos
├── id (PK)              INTEGER
├── valor                FLOAT           NOT NULL
├── valor_juros          FLOAT           DEFAULT 0
├── data                 DATETIME
├── is_juros             BOOLEAN         DEFAULT FALSE
├── emprestimo_id (FK)   INTEGER         REFERENCES emprestimos(id)
└── Relacionamentos:
    └── emprestimo (N:1)
```

---

## 4. API REST

### 4.1 Endpoints - Clientes

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/clientes` | Listar todos |
| POST | `/api/clientes` | Criar |
| GET | `/api/clientes/<id>` | Buscar por ID |
| PUT | `/api/clientes/<id>` | Atualizar |
| DELETE | `/api/clientes/<id>` | Excluir |

### 4.2 Endpoints - Empréstimos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/emprestimos` | Listar todos |
| GET | `/api/clientes/<id>/emprestimos` | Listar por cliente |
| POST | `/api/emprestimos` | Criar |
| GET | `/api/emprestimos/<id>` | Buscar por ID |
| PUT | `/api/emprestimos/<id>` | Atualizar |
| DELETE | `/api/emprestimos/<id>` | Excluir |

### 4.3 Endpoints - Pagamentos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/pagamentos` | Listar todos |
| GET | `/api/clientes/<id>/pagamentos` | Listar por cliente |
| GET | `/api/emprestimos/<id>/pagamentos` | Listar por empréstimo |
| POST | `/api/pagamentos` | Criar |
| GET | `/api/pagamentos/<id>` | Buscar por ID |
| PUT | `/api/pagamentos/<id>` | Atualizar |
| DELETE | `/api/pagamentos/<id>` | Excluir |

---

## 5. Regras de Negócio

### 5.1 Cálculo de Juros
```python
juros = saldo_devedor * (taxa_juros / 100)
valor_total = saldo_devedor + juros
```
- Juros calculados sobre **saldo devedor atual** (não sobre valor original)
- Atualizado a cada pagamento

### 5.2 Fluxo de Pagamento
```
1. Usuário seleciona empréstimo
2. Escolhe opção:
   - Pagar Juros (calcula automaticamente)
   - Pagar Saldo (valor自定义)
3. Sistema:
   - Abate principal do saldo_devedor
   - Adiciona principal ao total_pago
   - Registra valor_juros
   - Atualiza status se quitado
```

### 5.3 Exclusão de Pagamento
```
1. Calcula valor_principal = valor_total - valor_juros
2. Subtrai principal do total_pago
3. Adiciona principal ao saldo_devedor
4. Limita saldo ao valor_original
```

---

## 6. Frontend - Navegação

### 6.1 Fluxo Principal
```
┌─────────────┐
│  Clientes   │
└──────┬──────┘
       │
       ├──→ [Empréstimos] ──→ Lista filtrada por cliente
       │        │
       │        ├──→ [+ Novo] ──→ Form (cliente pré-selecionado)
       │        │
       │        └──→ [Pagar] ──→ Lista de pagamentos do empréstimo
       │
       └──→ [Pagamentos] ──→ Lista filtrada por cliente
                │
                └──→ [+ Novo] ──→ Form (empréstimo filtrado)
```

### 6.2 Componentes

| Componente | Responsabilidade |
|------------|------------------|
| ClientesList | Lista, busca, ações (editar, excluir, ver empréstimos, ver pagamentos) |
| ClientesForm | Criar/editar cliente |
| EmprestimosList | Lista filtrada, ações (ver, pagar, editar, excluir) |
| EmprestimosForm | Criar/editar empréstimo com preview de juros |
| PagamentosList | Lista filtrada por cliente/empréstimo, excluir |
| PagamentosForm | Registrar pagamento (juros + principal) |

---

## 7. Melhorias Implementadas

### 7.1 Funcionalidades Extras
| # | Funcionalidade | Descrição |
|---|----------------|-----------|
| 1 | Filtro por Cliente | Empréstimos e pagamentos filtrados por cliente |
| 2 | Botão Pagar | Acesso rápido ao formulário de pagamento |
| 3 | Valor Juros Separado | Armazena valor de juros pago separadamente |
| 4 | Navegação Contextual | Botões Voltar/Avanço mantendo contexto |
| 5 | Preselection | Cliente/empréstimo pré-selecionados nos formulários |

### 7.2 Correções
| # | Correção | Descrição |
|---|----------|-----------|
| 1 | Exclusão Pagamento | Lógica corrigida para usar valor_principal |
| 2 | Total Pago Negativo | Proteção contra valores negativos |
| 3 | Valor Customizado | Removido campo duplicado no formulário |

---

## 8. Funcionalidades Pendentes (do README original)

### 8.1 Etapa 4 - Usuários e Permissões
- [ ] Model Usuario (id, nome, login, senha, role)
- [ ] Relacionar usuário com cliente
- [ ] Criptografia de senha (bcrypt)
- [ ] Login com JWT
- [ ] Autorização por roles (ADMIN/USER)
- [ ] Restringir acesso: USER vê apenas seus dados

### 8.2 Etapa 5 - Dashboard
- [ ] Total emprestado
- [ ] Total recebido
- [ ] Total em aberto
- [ ] Empréstimos atrasados
- [ ] Gráficos e indicadores visuais

### 8.3 Melhorias de Infraestrutura
- [ ] Dockerização (Dockerfile + docker-compose)
- [ ] Autenticação JWT
- [ ] Seed automático ao iniciar

---

## 9. Configurações

### 9.1 Variáveis de Ambiente
```python
DATABASE_URL = postgresql://postgres:postgres@localhost:5432/emprestimo
SECRET_KEY = dev-secret-key-123
JWT_SECRET_KEY = jwt-secret-key-123
```

### 9.2 Dependências Python
```
flask
flask-cors
sqlalchemy
psycopg2-binary
python-dotenv
```

### 9.3 Dependências Node
```
vue
vite
axios
```

---

## 10. Como Executar

### 10.1 Backend
```bash
cd backend
source venv/bin/activate
python app.py
# Servidor em http://127.0.0.1:5000
```

### 10.2 Frontend
```bash
cd frontend
npm install
npm run dev
# Servidor em http://localhost:5173
```

### 10.3 Banco de Dados
```bash
# PostgreSQL deve estar rodando
# Tabelas criadas automaticamente por db.create_all()
```

---

## 11. Diagrama de Classes Simplificado

```
┌─────────────┐       ┌───────────────┐       ┌──────────────┐
│   Cliente   │       │  Emprestimo   │       │  Pagamento   │
├─────────────┤       ├───────────────┤       ├──────────────┤
│ id          │──1:N──│ id            │──1:N──│ id           │
│ nome        │       │ valor_original│       │ valor        │
│ telefone    │       │ taxa_juros    │       │ valor_juros  │
│ endereco    │       │ saldo_devedor │       │ data         │
│ created_at  │       │ total_pago    │       │ is_juros     │
└─────────────┘       │ status        │       └──────────────┘
                      │ cliente_id (F│
                      └───────────────┘
```

---

## 12. Próximos Passos Sugeridos

1. **Autenticação** - Implementar JWT e roles
2. **Dashboard** - Indicadores e gráficos
3. **Validação** - Campos obrigatórios, limites, máscaras
4. **Histórico** - Timeline de alterações
5. **Relatórios** - Exportação PDF/Excel
6. **Docker** - Containerização completa

---

*Documento gerado em 22/04/2026*
*Baseado no README.md e implementação atual*