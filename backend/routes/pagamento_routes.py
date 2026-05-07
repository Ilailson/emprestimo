from flask import Blueprint, request, jsonify
from extensions import db
from models.pagamento import Pagamento
from models.emprestimo import Emprestimo
from models.cliente import Cliente
from datetime import datetime
from decorators import token_required, admin_required

pagamento_bp = Blueprint('pagamentos', __name__, url_prefix='/api')

def _valor_principal_pagamento(pagamento):
    """Calcula o principal de forma compatível com registros antigos e novos."""
    valor = float(pagamento.valor or 0)
    juros = float(pagamento.valor_juros or 0)

    # Juros puro: nada de principal
    if pagamento.is_juros is True:
        return 0.0

    # Novo formato (misto): valor já representa apenas o principal
    if pagamento.is_juros is None:
        return max(valor, 0.0)

    # Formato legado: valor = principal + juros
    if juros > 0:
        principal = valor - juros
        return principal if principal > 0 else 0.0

    # Principal puro
    return max(valor, 0.0)


# LISTAR PAGAMENTOS - GET: user e admin
@pagamento_bp.route('/pagamentos', methods=['GET'])
@token_required
def listar_pagamentos():
    """Lista todos os pagamentos com filtro opcional por cliente"""
    from sqlalchemy.orm import joinedload

    q = request.args.get('q', '')

    # Usar eager loading para evitar N+1 queries
    query = Pagamento.query.options(
        joinedload(Pagamento.emprestimo).joinedload(Emprestimo.cliente)
    ).order_by(Pagamento.data.desc())

    # Filtro por nome do cliente (em SQL)
    if q:
        query = query.join(Emprestimo).join(Cliente).filter(Cliente.nome.ilike(f'%{q}%'))

    pagamentos = query.all()

    return jsonify([p.to_dict() for p in pagamentos]), 200

# LISTAR PAGAMENTOS - GET: user e admin
@pagamento_bp.route('/clientes/<int:cliente_id>/pagamentos', methods=['GET'])
@token_required
def listar_pagamentos_cliente(cliente_id):
    """Lista pagamentos de um cliente específico"""
    from sqlalchemy.orm import joinedload

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    # Usar eager loading
    pagamentos = Pagamento.query.options(
        joinedload(Pagamento.emprestimo).joinedload(Emprestimo.cliente)
    ).join(Emprestimo).filter(Emprestimo.cliente_id == cliente_id).order_by(Pagamento.data.desc()).all()

    return jsonify([p.to_dict() for p in pagamentos]), 200


@pagamento_bp.route('/emprestimos/<int:emp_id>/pagamentos', methods=['GET'])
@token_required
def listar_pagamentos_emprestimo(emp_id):
    """Lista pagamentos de um empréstimo específico"""
    from sqlalchemy.orm import joinedload

    emprestimo = Emprestimo.query.get(emp_id)
    if not emprestimo:
        return jsonify({'erro': 'Empréstimo não encontrado'}), 404

    # Usar eager loading
    pagamentos = Pagamento.query.options(
        joinedload(Pagamento.emprestimo).joinedload(Emprestimo.cliente)
    ).filter_by(emprestimo_id=emp_id).order_by(Pagamento.data.desc()).all()

    return jsonify([p.to_dict() for p in pagamentos]), 200


@pagamento_bp.route('/pagamentos', methods=['POST'])
@admin_required
def criar_pagamento():
    """Registra um novo pagamento e atualiza o empréstimo"""
    data = request.json

    if not data.get('emprestimo_id'):
        return jsonify({'erro': 'Empréstimo é obrigatório'}), 400

    emprestimo = Emprestimo.query.get(data['emprestimo_id'])
    if not emprestimo:
        return jsonify({'erro': 'Empréstimo não encontrado'}), 404

    valor_informado = float(data.get('valor', 0))
    if valor_informado <= 0:
        return jsonify({'erro': 'Valor deve ser maior que zero'}), 400

    pagar_juros = bool(data.get('pagar_juros', False))
    pagar_saldo = float(data.get('pagar_saldo', 0))

    valor_juros = 0
    valor_principal = 0
    valor_total = 0

    # Fluxo padrão (formulário existente): juros calculado + saldo opcional
    if pagar_juros or pagar_saldo > 0:
        if pagar_juros:
            # Usar juros acumulados dinâmico baseado no atraso
            valor_juros = emprestimo.calcular_juros_acumulados()

        if pagar_saldo > 0:
            if emprestimo.saldo_devedor and pagar_saldo > emprestimo.saldo_devedor:
                pagar_saldo = emprestimo.saldo_devedor
            valor_principal = pagar_saldo

        valor_total = valor_juros + valor_principal

    # Fluxo manual (pendências mensais): registra pagamento informado como juros
    else:
        valor_juros = valor_informado
        valor_total = valor_informado

    if valor_total <= 0:
        return jsonify({'erro': 'Valor total do pagamento inválido'}), 400

    if valor_principal > 0:
        emprestimo.total_pago = (emprestimo.total_pago or 0) + valor_principal
        emprestimo.saldo_devedor = (emprestimo.saldo_devedor or 0) - valor_principal
        if emprestimo.saldo_devedor <= 0:
            emprestimo.saldo_devedor = 0
            emprestimo.status = 'pago'

    # Novo padrão de gravação:
    # - Juros puro: valor = juros e valor_juros = juros
    # - Principal puro: valor = principal e valor_juros = 0
    # - Misto (principal + juros): valor = principal e valor_juros = juros
    if valor_principal > 0 and valor_juros > 0:
        valor_registrado = valor_principal
        is_juros = None
    elif valor_principal > 0:
        valor_registrado = valor_principal
        is_juros = False
    else:
        # Juros puro: não houve principal
        valor_registrado = 0
        is_juros = True

    data_pagamento = None
    if data.get('data'):
        try:
            data_pagamento = datetime.fromisoformat(str(data['data']))
        except:
            try:
                data_pagamento = datetime.fromisoformat(str(data['data']).split('T')[0])
            except:
                data_pagamento = None

    pagamento = Pagamento(
        valor=valor_registrado,
        valor_juros=valor_juros,
        emprestimo_id=data['emprestimo_id'],
        is_juros=is_juros
    )

    if data_pagamento:
        pagamento.data = data_pagamento

    db.session.add(pagamento)
    db.session.commit()

    return jsonify(pagamento.to_dict()), 201


@pagamento_bp.route('/pagamentos/<int:id>', methods=['GET'])
@admin_required
def buscar_pagamento(id):
    """Busca pagamento por ID"""
    pagamento = Pagamento.query.get(id)
    if not pagamento:
        return jsonify({'erro': 'Pagamento não encontrado'}), 404
    return jsonify(pagamento.to_dict()), 200


@pagamento_bp.route('/pagamentos/<int:id>', methods=['PUT'])
@admin_required
def atualizar_pagamento(id):
    """Atualiza um pagamento"""
    pagamento = Pagamento.query.get(id)
    if not pagamento:
        return jsonify({'erro': 'Pagamento não encontrado'}), 404

    data = request.json
    if data.get('valor'):
        valor_novo = float(data['valor'])
        valor_antigo = pagamento.valor
        diferenca = valor_novo - valor_antigo

        pagamento.valor = valor_novo

        emprestimo = pagamento.emprestimo
        if emprestimo:
            emprestimo.total_pago = (emprestimo.total_pago or 0) + diferenca
            emprestimo.saldo_devedor = (emprestimo.saldo_devedor or 0) - diferenca

            if emprestimo.saldo_devedor < 0:
                emprestimo.saldo_devedor = 0
            if emprestimo.saldo_devedor <= 0:
                emprestimo.status = 'pago'

        db.session.commit()

    return jsonify(pagamento.to_dict()), 200


@pagamento_bp.route('/pagamentos/<int:id>', methods=['DELETE'])
@admin_required
def excluir_pagamento(id):
    """Exclui um pagamento"""
    pagamento = Pagamento.query.get(id)
    if not pagamento:
        return jsonify({'erro': 'Pagamento não encontrado'}), 404

    emprestimo = pagamento.emprestimo
    if emprestimo:
        valor_principal = _valor_principal_pagamento(pagamento)

        emprestimo.total_pago = (emprestimo.total_pago or 0) - valor_principal
        if emprestimo.total_pago < 0:
            emprestimo.total_pago = 0

        emprestimo.saldo_devedor = (emprestimo.saldo_devedor or 0) + valor_principal
        if emprestimo.saldo_devedor > emprestimo.valor_original:
            emprestimo.saldo_devedor = emprestimo.valor_original

    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({'mensagem': 'Pagamento excluído com sucesso'}), 200
