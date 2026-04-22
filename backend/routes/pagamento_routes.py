from flask import Blueprint, request, jsonify
from extensions import db
from models.pagamento import Pagamento
from models.emprestimo import Emprestimo

pagamento_bp = Blueprint('pagamentos', __name__, url_prefix='/api')


@pagamento_bp.route('/pagamentos', methods=['GET'])
def listar_pagamentos():
    """Lista todos os pagamentos"""
    pagamentos = Pagamento.query.order_by(Pagamento.data.desc()).all()
    return jsonify([p.to_dict() for p in pagamentos]), 200


@pagamento_bp.route('/emprestimos/<int:emp_id>/pagamentos', methods=['GET'])
def listar_pagamentos_emprestimo(emp_id):
    """Lista pagamentos de um empréstimo específico"""
    emprestimo = Emprestimo.query.get(emp_id)
    if not emprestimo:
        return jsonify({'erro': 'Empréstimo não encontrado'}), 404
    pagamentos = Pagamento.query.filter_by(emprestimo_id=emp_id).order_by(Pagamento.data.desc()).all()
    return jsonify([p.to_dict() for p in pagamentos]), 200


@pagamento_bp.route('/pagamentos', methods=['POST'])
def criar_pagamento():
    """Registra um novo pagamento e atualiza o empréstimo"""
    data = request.json

    if not data.get('emprestimo_id'):
        return jsonify({'erro': 'Empréstimo é obrigatório'}), 400

    emprestimo = Emprestimo.query.get(data['emprestimo_id'])
    if not emprestimo:
        return jsonify({'erro': 'Empréstimo não encontrado'}), 404

    valor = float(data.get('valor', 0))
    if valor <= 0:
        return jsonify({'erro': 'Valor deve ser maior que zero'}), 400

    pagar_juros = data.get('pagar_juros', False)
    pagar_saldo = float(data.get('pagar_saldo', 0))

    valor_juros = 0
    valor_principal = 0

    if pagar_juros:
        valor_juros = emprestimo.calcular_juros()

    if pagar_saldo > 0:
        if emprestimo.saldo_devedor and pagar_saldo > emprestimo.saldo_devedor:
            pagar_saldo = emprestimo.saldo_devedor
        valor_principal = pagar_saldo

    valor_total = valor_juros + valor_principal

    if valor_total > 0:
        if valor_principal > 0:
            emprestimo.total_pago = (emprestimo.total_pago or 0) + valor_principal
            emprestimo.saldo_devedor = (emprestimo.saldo_devedor or 0) - valor_principal
            if emprestimo.saldo_devedor <= 0:
                emprestimo.saldo_devedor = 0
                emprestimo.status = 'pago'

    is_juros = valor_principal == 0 and valor_total > 0

    pagamento = Pagamento(
        valor=valor_total,
        valor_juros=valor_juros,
        emprestimo_id=data['emprestimo_id'],
        is_juros=is_juros
    )
    db.session.add(pagamento)
    db.session.commit()

    return jsonify(pagamento.to_dict()), 201


@pagamento_bp.route('/pagamentos/<int:id>', methods=['GET'])
def buscar_pagamento(id):
    """Busca pagamento por ID"""
    pagamento = Pagamento.query.get(id)
    if not pagamento:
        return jsonify({'erro': 'Pagamento não encontrado'}), 404
    return jsonify(pagamento.to_dict()), 200


@pagamento_bp.route('/pagamentos/<int:id>', methods=['PUT'])
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
def excluir_pagamento(id):
    """Exclui um pagamento"""
    pagamento = Pagamento.query.get(id)
    if not pagamento:
        return jsonify({'erro': 'Pagamento não encontrado'}), 404

    emprestimo = pagamento.emprestimo
    if emprestimo:
        valor_principal = pagamento.valor - (pagamento.valor_juros or 0)
        if valor_principal < 0:
            valor_principal = 0

        emprestimo.total_pago = (emprestimo.total_pago or 0) - valor_principal
        if emprestimo.total_pago < 0:
            emprestimo.total_pago = 0

        emprestimo.saldo_devedor = (emprestimo.saldo_devedor or 0) + valor_principal
        if emprestimo.saldo_devedor > emprestimo.valor_original:
            emprestimo.saldo_devedor = emprestimo.valor_original

    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({'mensagem': 'Pagamento excluído com sucesso'}), 200