from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Extensão do banco de dados
db = SQLAlchemy()

# Extensão JWT (será inicializada na app)
jwt = JWTManager()

# Extensão Rate Limiter (anti brute force)
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Extensão JWT (gerencia tokens de autenticação)
jwt = JWTManager()

# Extensão Limiter (rate limiting para prevenir brute force)
limiter = Limiter(
    key_func=get_remote_address,  # Identifica usuário pelo IP (pode ser adaptado para login)
    default_limits=["200 per day", "50 per hour"]  # Limites padrão
)
