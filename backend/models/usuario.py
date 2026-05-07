from extensions import db
from datetime import datetime
import bcrypt

class Usuario(db.Model):
    """Modelo Usuario - gerencia autenticação e autorização
    Diferença entre Autenticação e Autorização:
    - Autenticação: Verificar QUEM é o usuário (login/senha, JWT)
    - Autorização: Verificar O QUE o usuário pode fazer (role admin/user)
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_senha(self, senha_pura: str) -> None:
        """Gera hash da senha usando bcrypt (nunca armazenar texto puro)"""
        self.senha_hash = bcrypt.hashpw(senha_pura.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verificar_senha(self, senha_pura: str) -> bool:
        """Valida senha no login comparando com o hash armazenado"""
        return bcrypt.checkpw(senha_pura.encode('utf-8'), self.senha_hash.encode('utf-8'))

    def to_dict(self):
        """Retorna dados do usuário sem expor o hash da senha"""
        return {
            'id': self.id,
            'nome': self.nome,
            'login': self.login,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
