from flask import Blueprint, request, jsonify
from extensions import db
from models.emprestimo import Emprestimo
from models.cliente import Cliente
from datetime import datetime

emprestimo_bp = Blueprint('emprestimos', __name__, url_prefix='/api')


# LISTAR TODOS OS EMPRÉSTIMOS
@emprestimo_bp.route('/emprestimos', methods=['GET'])
def listar_emprestimos():
    """Retorna lista de todos os empréstimos"""
    emprestimos = Emprestimo.query.all()
    return jsonify([e.to_dict() for e in emprestimos]), 200


# LISTAR EMPRÉSTIMOS POR CLIENTE
@emprestimo_bp.route('/clientes/<int:cliente_id>/emprestimos', methods=['GET'])
def listar_emprestimos_cliente(cliente_id):
    """Retorna empréstimos de um cliente específico"""
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    emprestimos = Emprestimo.query.filter_by(cliente_id=cliente_id).all()
    return jsonify([e.to_dict() for e in emprestimos]), 200


# CRIAR NOVO EMPRÉSTIMO
@emprestimo_bp.route('/emprestimos', methods=['POST'])
def criar_emprestimo():
    """Cria um novo empréstimo"""
    data = request.json

    # Validar campos obrigatórios
    if not data.get('valor') or not data.get('taxa_juros') or not data.get('cliente_id'):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    # Verificar se cliente existe
    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    # Converter data se informada
    data_emprestimo = None
    if data.get('data'):
        try:
            data_emprestimo = datetime.fromisoformat(data['data'])
        except:
            data_emprestimo = datetime.utcnow()

    # Criar empréstimo
    emprestimo = Emprestimo(
        valor=float(data['valor']),
        taxa_juros=float(data['taxa_juros']),
        cliente_id=data['cliente_id'],
        status=data.get('status', 'em_aberto'),
        data=data_emprestimo
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
        emprestimo.valor = float(data['valor'])
    if data.get('taxa_juros'):
        emprestimo.taxa_juros = float(data['taxa_juros'])
    if data.get('status'):
        emprestimo.status = data['status']
    if data.get('data'):
        try:
            emprestimo.data = datetime.fromisoformat(data['data'])
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