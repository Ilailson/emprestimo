from flask import Blueprint, request, jsonify
from extensions import db
from models.emprestimo import Emprestimo
from models.cliente import Cliente
from datetime import datetime

emprestimo_bp = Blueprint('emprestimos', __name__, url_prefix='/api')


# LISTAR TODOS OS EMPRÉSTIMOS
@emprestimo_bp.route('/emprestimos', methods=['GET'])
def listar_emprestimos():
    """Retorna lista de todos os empréstimos com filtros opcionais"""
    from sqlalchemy.orm import joinedload
    
    q = request.args.get('q', '')
    status = request.args.get('status', '')
    
    # Usar eager loading para evitar N+1 queries
    query = Emprestimo.query.options(joinedload(Emprestimo.cliente))
    
    # Filtro por nome do cliente (em SQL)
    if q:
        query = query.join(Cliente).filter(Cliente.nome.ilike(f'%{q}%'))
    
    # Filtro por status (em SQL)
    if status:
        agora = datetime.utcnow()
        if status == 'atrasado':
            query = query.filter(
                Emprestimo.saldo_devedor > 0,
                Emprestimo.data_vencimento != None,
                Emprestimo.data_vencimento < agora
            )
        elif status == 'em_aberto':
            query = query.filter(Emprestimo.status == 'em_aberto')
        elif status == 'pago':
            query = query.filter(Emprestimo.status == 'pago')
    
    # Usar distinct para evitar duplicatas quando há join
    emprestimos = query.distinct().all()
    
    return jsonify([e.to_dict() for e in emprestimos]), 200


# LISTAR EMPRÉSTIMOS POR CLIENTE
@emprestimo_bp.route('/clientes/<int:cliente_id>/emprestimos', methods=['GET'])
def listar_emprestimos_cliente(cliente_id):
    """Retorna empréstimos de um cliente específico com filtros opcionais"""
    from sqlalchemy.orm import joinedload
    
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    status = request.args.get('status', '')
    
    # Usar eager loading
    query = Emprestimo.query.options(joinedload(Emprestimo.cliente)).filter_by(cliente_id=cliente_id)
    
    # Filtro por status (em SQL)
    if status:
        agora = datetime.utcnow()
        if status == 'atrasado':
            query = query.filter(
                Emprestimo.saldo_devedor > 0,
                Emprestimo.data_vencimento != None,
                Emprestimo.data_vencimento < agora
            )
        elif status == 'em_aberto':
            query = query.filter(Emprestimo.status == 'em_aberto')
        elif status == 'pago':
            query = query.filter(Emprestimo.status == 'pago')
    
    emprestimos = query.all()
    
    return jsonify([e.to_dict() for e in emprestimos]), 200


# CRIAR NOVO EMPRÉSTIMO
@emprestimo_bp.route('/emprestimos', methods=['POST'])
def criar_emprestimo():
    """Cria um novo empréstimo"""
    data = request.json

    if not data.get('valor') or not data.get('taxa_juros') or not data.get('cliente_id'):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    data_emprestimo = None
    if data.get('data'):
        try:
            data_emprestimo = datetime.fromisoformat(data['data'])
        except:
            data_emprestimo = datetime.utcnow()

    data_vencimento = None
    if data.get('data_vencimento'):
        try:
            data_vencimento_str = data['data_vencimento']
            if data_vencimento_str:
                data_vencimento = datetime.fromisoformat(data_vencimento_str)
        except:
            pass

    valor_original = float(data['valor'])
    taxa = float(data['taxa_juros'])

    emprestimo = Emprestimo(
        valor_original=valor_original,
        taxa_juros=taxa,
        cliente_id=data['cliente_id'],
        status=data.get('status', 'em_aberto'),
        data=data_emprestimo,
        data_vencimento=data_vencimento,
        data_ultimo_calculo=datetime.utcnow(),
        saldo_devedor=valor_original,
        total_pago=0.0
    )

    db.session.add(emprestimo)
    db.session.commit()

    return jsonify(emprestimo.to_dict()), 201


# BUSCAR EMPRÉSTIMO POR ID
@emprestimo_bp.route('/emprestimos/<int:id>', methods=['GET'])
def buscar_emprestimo(id):
    """Retorna um empréstimo pelo ID"""
    emprestimo = Emprestimo.query.get(id)
    if not emprestimo:
        return jsonify({'erro': 'Empréstimo não encontrado'}), 404
    return jsonify(emprestimo.to_dict()), 200


# ATUALIZAR EMPRÉSTIMO
@emprestimo_bp.route('/emprestimos/<int:id>', methods=['PUT'])
def atualizar_emprestimo(id):
    """Atualiza um empréstimo existente"""
    emprestimo = Emprestimo.query.get(id)
    if not emprestimo:
        return jsonify({'erro': 'Empréstimo não encontrado'}), 404

    data = request.json

    if data.get('valor'):
        emprestimo.valor_original = float(data['valor'])
    if data.get('valor_original'):
        emprestimo.valor_original = float(data['valor_original'])
    if data.get('saldo_devedor'):
        saldo_novo = float(data['saldo_devedor'])
        saldo_antigo = emprestimo.saldo_devedor or 0
        diferenca = saldo_novo - saldo_antigo
        if diferenca != 0:
            emprestimo.valor_original = (emprestimo.valor_original or 0) + diferenca
        emprestimo.saldo_devedor = saldo_novo
    if data.get('taxa_juros'):
        emprestimo.taxa_juros = float(data['taxa_juros'])
    if data.get('status'):
        emprestimo.status = data['status']
    if data.get('data'):
        try:
            emprestimo.data = datetime.fromisoformat(data['data'])
        except:
            pass
    if data.get('data_vencimento'):
        try:
            emprestimo.data_vencimento = datetime.fromisoformat(data['data_vencimento'])
        except:
            pass

    db.session.commit()
    return jsonify(emprestimo.to_dict()), 200


# EXCLUIR EMPRÉSTIMO
@emprestimo_bp.route('/emprestimos/<int:id>', methods=['DELETE'])
def excluir_emprestimo(id):
    """Exclui um empréstimo pelo ID"""
    emprestimo = Emprestimo.query.get(id)
    if not emprestimo:
        return jsonify({'erro': 'Empréstimo não encontrado'}), 404

    db.session.delete(emprestimo)
    db.session.commit()
    return jsonify({'mensagem': 'Empréstimo excluído com sucesso'}), 200