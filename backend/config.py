import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-123')
    
    # DATABASE_URL pode ser:
    # - sqlite:///instance/emprestimo.db (desenvolvimento local)
    # - postgresql://user:pass@host:5432/dbname (produção)
    # Se não definida, usa SQLite por padrão
    db_uri = os.environ.get('DATABASE_URL', '')
    if db_uri:
        SQLALCHEMY_DATABASE_URI = db_uri
    else:
        # SQLite padrão - cria pasta instance se não existir
        instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{instance_dir}/emprestimo.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-123')
