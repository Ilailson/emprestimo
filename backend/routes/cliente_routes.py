from flask import Blueprint, request, jsonify
from extensions import db
from models.cliente import Cliente
cliente_bp = Blueprint('clientes', __name__, url_prefix='/api')
# LISTAR TODOS OS CLIENTES
@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    """Retorna lista de todos os clientes"""
    clientes = Cliente.query.all()
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
