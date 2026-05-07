from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.usuario import Usuario

def token_required(fn):
    """Decorator base: exige que o usuário esteja autenticado (JWT válido)
    - Valida assinatura do token
    - Verifica expiração
    - Injeta user_id no contexto
    """
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'erro': 'Token inválido ou expirado'}), 401
        
        # Converte identity (string) para int para consulta no banco
        try:
            user_id = int(current_user_id)
        except (ValueError, TypeError):
            return jsonify({'erro': 'Token inválido'}), 401
        
        usuario = Usuario.query.get(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 401
        
        request.current_user = usuario
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def admin_required(fn):
    """Decorator: exige que o usuário seja ADMIN
    - Aplica token_required primeiro
    - Verifica se role == 'admin'
    """
    @token_required
    def wrapper(*args, **kwargs):
        if request.current_user.role != 'admin':
            return jsonify({'erro': 'Acesso negado: apenas administradores'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def user_required(fn):
    """Decorator: permite USER e ADMIN (acesso de leitura)
    - Aplica token_required primeiro
    - User e admin são permitidos
    """
    @token_required
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
