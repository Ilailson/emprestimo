from flask import Blueprint, request, jsonify
from extensions import db, limiter
from models.usuario import Usuario
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
import logging

# Configuração de log para segurança (tentativas de login falhas)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Rate Limit específico para login: 5 tentativas por minuto (anti brute force)
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Rota de login: valida credenciais e retorna tokens JWT
    - POST /api/auth/login
    - Body: { "login": "admin", "senha": "123456" }
    """
    data = request.json
    
    # Validação de dados de entrada (obrigatório)
    if not data or not data.get('login') or not data.get('senha'):
        return jsonify({'erro': 'Login e senha são obrigatórios'}), 400
    
    login = data['login'].strip()
    senha = data['senha']
    
    # Busca usuário pelo login (único)
    usuario = Usuario.query.filter_by(login=login).first()
    
    # Validação de senha (usando bcrypt)
    if not usuario or not usuario.verificar_senha(senha):
        # Log de segurança: tentativa de login falha
        logger.warning(f"Tentativa de login falha: login={login}, ip={request.remote_addr}")
        return jsonify({'erro': 'Credenciais inválidas'}), 401
    
    # Atualiza último login
    usuario.last_login = db.func.now()
    db.session.commit()
    
    # Cria tokens JWT (inclui user_id e role no identity)
    # Identity deve ser string (JWT exige)
    access_token = create_access_token(
        identity=str(usuario.id),
        additional_claims={'role': usuario.role}
    )
    refresh_token = create_refresh_token(identity=str(usuario.id))
    
    logger.info(f"Login bem-sucedido: usuario={usuario.login}, role={usuario.role}")
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': usuario.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renova access token usando refresh token válido
    - POST /api/auth/refresh
    - Header: Authorization: Bearer <refresh_token>
    """
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(current_user_id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 401
    
    # Novo access token com os mesmos claims
    new_access_token = create_access_token(
        identity=str(usuario.id),
        additional_claims={'role': usuario.role}
    )
    
    return jsonify({'access_token': new_access_token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Retorna dados do usuário logado (para o frontend)"""
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(current_user_id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 401
    
    return jsonify(usuario.to_dict()), 200
