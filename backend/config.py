import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/emprestimo'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration (Token Security)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-123')  # Use uma chave forte em produção!
    JWT_ACCESS_TOKEN_EXPIRES = 15 * 60  # 15 minutos (900 segundos)
    JWT_REFRESH_TOKEN_EXPIRES = 30 * 24 * 60 * 60  # 30 dias
    JWT_TOKEN_LOCATION = ['headers']  # Tokens apenas no header Authorization
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # CORS (Permitir apenas domínio do frontend Vue)
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

    # Rate Limit (Anti brute force)
    RATELIMIT_STORAGE_URL = "memory://"  # Em produção use Redis
    RATELIMIT_DEFAULT = "5 per minute"  # Limite padrão: 5 requisições/minuto
