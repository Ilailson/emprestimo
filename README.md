<!-- Faça a leitura de todo o projeto para checar em que fase está para prosseguir com o desenvolvimento -->
<!-- Fazer backup do backup e do projeto a cada funcionalidade implantada. -->
<!-- Analise o meu projeto, aprenda todas as funcionalidades dele entenda como ele funciona e me explique se você entendeu pois, vou pedir modificações ou melhorias. -->

Crie um sistema web completo para controle de empréstimos de dinheiro utilizando abordagem incremental (vibe coding), desenvolvendo uma funcionalidade por vez com backend e frontend integrados.

📌 Tecnologias:
- Backend: Python com Flask
- Banco de dados: PostgreSQL
- ORM: SQLAlchemy
- Frontend: Vue.js (Vue 3)

📌 Regras gerais:
- Código simples e bem explicado (nível iniciante)
- Backend organizado em models, routes e services
- Frontend organizado em componentes Vue
- Cada etapa deve ser funcional antes de avançar
- Sempre mostrar integração frontend/backend
- Mostrar estrutura de pastas
- Preparar e implementar autenticação e autorização
- Sempre aguardar confirmação do usuário antes de avançar para a próxima etapa

- Sempre dividir a resposta em:
  1. Explicação simples
  2. Código
  3. Como testar

- Sempre comentar o código explicando o que cada parte faz

- Garantir a ordem correta de criação das tabelas respeitando dependências:
  - Primeiro tabelas sem dependência (Cliente)
  - Depois tabelas dependentes (Emprestimo)
  - Depois tabelas com múltiplas dependências (Pagamento)

- Utilizar criação automática de tabelas com SQLAlchemy (db.create_all()) OU migrations (Flask-Migrate/Alembic)

- Garantir que todas as tabelas estejam criadas antes de executar qualquer inserção de dados

📌 Regras de negócio:
- Um cliente pode ser também um usuário do sistema
- Usuários possuem dois perfis:
  - ADMIN: acesso total ao sistema
  - USER: só pode visualizar seus próprios empréstimos e dívidas
- O sistema deve controlar empréstimos, pagamentos e saldo devedor

- O cálculo de juros deve ser feito sempre sobre o saldo devedor atual (não sobre o valor original)

- Regra de cálculo:
  saldo_devedor = valor_original - soma_pagamentos

  juros = saldo_devedor * (taxa_juros / 100)

  valor_total = saldo_devedor + juros

- A cada pagamento:
  - o valor pago deve ser abatido do saldo devedor
  - o próximo cálculo de juros deve considerar o novo saldo atualizado

- O sistema não deve recalcular juros sobre valores já pagos

- Armazenar no banco:
  - valor_original
  - saldo_devedor atualizado
  - total_pago

📌 Funcionalidades:

🧩 Etapa 1 - Clientes
- Model Cliente (id, nome, telefone, endereco)
- CRUD básico
- Tela Vue para cadastro e listagem

🧩 Etapa 2 - Empréstimos
- Model Emprestimo (valor_original, taxa_juros, data, cliente_id, status, saldo_devedor, total_pago)
- Criar relacionamento correto com Cliente (foreign key)
- Implementar cálculo de juros baseado no saldo devedor
- Listagem com destaque:
  - Em aberto
  - Atrasado
- Tela Vue completa

🧩 Etapa 3 - Pagamentos
- Model Pagamento (valor, data, emprestimo_id)
- Criar relacionamento correto com Emprestimo (foreign key)
- Ao registrar pagamento:
  - atualizar saldo_devedor
  - atualizar total_pago
- Tela de registro de pagamento

🧩 Etapa 4 - Usuários e Permissões
- Model Usuario (id, nome, login, senha, role)
- Relacionar usuário com cliente
- Criptografia de senha
- Implementar login com JWT
- Explicar claramente autenticação (JWT) e autorização (roles)
- Restringir acesso:
  - USER vê apenas seus dados
  - ADMIN vê tudo

🧩 Etapa 5 - Dashboard
- Exibir indicadores:
  - Total emprestado
  - Total recebido
  - Total em aberto
  - Empréstimos atrasados
- Interface simples e moderna

📌 Frontend:
- Interface simples, moderna e responsiva
- Formulários para:
  - Cadastro de clientes
  - Cadastro de empréstimos
  - Registro de pagamentos
- Tabela de empréstimos com destaques visuais
- Dashboard com indicadores principais

📌 Importante:
- Não pular etapas
- Explicar tudo de forma simples
- Sempre mostrar como testar
- Sempre mostrar exemplos de requisições (curl ou Postman)
- Sempre integrar backend com frontend antes de avançar

Comece pela Etapa 1 (Clientes).

📌 Dados iniciais (Seed do banco):
- Popular automaticamente o banco de dados com dados fictícios para testes
- Criar script separado chamado seed.py
- Criar pelo menos:
  - 10 clientes com nome e telefone válidos
  - 10 empréstimos vinculados a esses clientes

- Os empréstimos devem conter:
  - valores variados
  - taxas de juros diferentes
  - datas diferentes (incluindo alguns atrasados)
  - status (em aberto, pago, atrasado)

- Garantir que os dados sejam realistas

📌 Regras do Seed:
- Executar o seed somente após todas as tabelas estarem criadas corretamente
- Executar automaticamente ao iniciar o sistema
- Evitar duplicação de dados ao reiniciar
- Criar:
  - alguns empréstimos em aberto
  - alguns pagos
  - alguns atrasados
- Explicar como funciona a geração dos dados

📌 Containerização com Docker:

- Criar Dockerfile para o backend (Flask)
- Criar Dockerfile para o frontend (Vue.js)
- Criar docker-compose.yml para orquestrar:
  - backend
  - frontend
  - banco PostgreSQL

📌 Requisitos:
- O backend deve conectar corretamente ao banco dentro do container
- O frontend deve consumir a API do backend
- Configurar variáveis de ambiente (DB_HOST, DB_USER, DB_PASSWORD, etc)
- Garantir que tudo funcione com um único comando:
  docker-compose up

📌 Boas práticas:
- Usar volumes para persistência do banco
- Evitar rebuild desnecessário
- Explicar cada parte do Dockerfile e docker-compose

📌 Importante:
- Só implementar Docker após todas as etapas do sistema estarem funcionando corretamente
