from flask import Blueprint, request, jsonify
from extensions import db
from models.cliente import Cliente
from sqlalchemy import or_
from sqlalchemy.orm import Session

cliente_bp = Blueprint('clientes', __name__, url_prefix='/api')

# LISTAR TODOS OS CLIENTES (com busca opcional)
@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    """Retorna lista de todos os clientes, com filtro opcional por nome ou telefone"""
    termo = request.args.get('q', '')

    query = Cliente.query
    if termo:
        #ILIKE para PostgreSQL, LIKE para SQLite
        termo_upper = termo.upper()
        termo_lower = termo.lower()
        query = query.filter(
            or_(
                Cliente.nome.ilike(f'%{termo}%'),
                Cliente.nome.like(f'%{termo}%'),
                Cliente.telefone.ilike(f'%{termo}%'),
                Cliente.telefone.like(f'%{termo}%')
            )
        )

    clientes = query.all()
    return jsonify([c.to_dict() for c in clientes]), 200
# CRIAR NOVO CLIENTE
@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    """Cria um novo cliente"""
    data = request.json

    # Validar campos obrigatórios
    if not data.get('nome') or not data.get('telefone'):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    cliente = Cliente(
        nome=data['nome'],
        telefone=data['telefone'],
        endereco=data.get('endereco', '')
    )
    db.session.add(cliente)
    db.session.commit()

    return jsonify(cliente.to_dict()), 201

# BUSCAR CLIENTE POR ID
@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def buscar_cliente(id):
    """Retorna um cliente pelo ID"""
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    return jsonify(cliente.to_dict()), 200

# ATUALIZAR CLIENTE
@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    """Atualiza um cliente existente"""
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    data = request.json

    # Validar campos obrigatórios
    if not data.get('nome') or not data.get('telefone'):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    cliente.nome = data['nome']
    cliente.telefone = data['telefone']
    cliente.endereco = data.get('endereco', '')

    db.session.commit()
    return jsonify(cliente.to_dict()), 200

# EXCLUIR CLIENTE
@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def excluir_cliente(id):
    """Exclui um cliente pelo ID"""
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'mensagem': 'Cliente excluído com sucesso'}), 200

# RELATÓRIOS
@cliente_bp.route('/clientes/<int:cliente_id>/relatorio-juros', methods=['GET'])
def relatorio_juros(cliente_id):
    """Relatório de juros pagos por cliente - soma direta do valor_juros"""
    from models.emprestimo import Emprestimo
    from models.pagamento import Pagamento

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    # Buscar todos os empréstimos do cliente
    emprestimos = Emprestimo.query.filter_by(cliente_id=cliente_id).all()

    # Calcular saldo devedor total (soma do saldo_devedor de todos os empréstimos não pagos)
    saldo_devedor_total = 0
    for emp in emprestimos:
        # Considerar apenas empréstimos que ainda têm saldo devedor
        if (emp.saldo_devedor is not None) and (emp.verificar_status() != 'pago'):
            saldo_devedor_total += float(emp.saldo_devedor)

    valor_total_emprestado = sum(float(e.valor_original or 0) for e in emprestimos)

    # Buscar todos os pagamentos dos empréstimos deste cliente
    emprestimo_ids = [e.id for e in emprestimos]

    # Inicializar totais
    total_juros_pagos = 0
    total_principal_pago = 0
    total_geral_pago = 0  # Será a soma de juros + principal
    pagamentos_detalhados = []

    if emprestimo_ids:
        pagamentos = Pagamento.query.filter(Pagamento.emprestimo_id.in_(emprestimo_ids)).all()

        for pag in pagamentos:
            valor = float(pag.valor or 0)
            juros = float(pag.valor_juros or 0)
            principal = valor - juros if valor > juros else valor

            total_juros_pagos += juros
            total_principal_pago += principal
            # Total Geral Pago = Total Juros Pagos + Total Principal Pago
            total_geral_pago = total_juros_pagos + total_principal_pago

            pagamentos_detalhados.append({
                'id': pag.id,
                'data': pag.data.isoformat() if pag.data else None,
                'valor': valor,
                'juros': juros,
                'principal': principal,
                'emprestimo_id': pag.emprestimo_id
            })

    return jsonify({
        'cliente': cliente.to_dict(),
        'valor_total_emprestado': valor_total_emprestado,
        'saldo_devedor_total': saldo_devedor_total,
        'total_juros_pagos': total_juros_pagos,
        'total_principal_pago': total_principal_pago,
        'total_geral_pago': total_geral_pago,  # Juros + Principal
        'quantidade_emprestimos': len(emprestimos),
        'quantidade_pagamentos': len(pagamentos_detalhados),
        'pagamentos': pagamentos_detalhados
    }), 200
