from extensions import db
from datetime import datetime
class Pagamento(db.Model):
    """Modelo Pagamento - pagamento de um empréstimo"""
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    # FK para empréstimo
    emprestimo_id = db.Column(db.Integer, db.ForeignKey('emprestimos.id'), nullable=False)

    def to_dict(self):
        """Converte pagamento para dicionário (JSON)"""
        return {
            'id': self.id,
            'valor': self.valor,
            'data': self.data.isoformat() if self.data else None,
            'emprestimo_id': self.emprestimo_id
        }