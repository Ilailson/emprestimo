from extensions import db
from datetime import datetime
class Cliente(db.Model):
    """Modelo Cliente - pessoa que pega emprestado dinheiro"""
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento: um cliente pode ter vários empréstimos
    emprestimos = db.relationship('Emprestimo', backref='cliente', lazy=True)

    def to_dict(self):
        """Converte cliente para dicionário (JSON)"""
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
