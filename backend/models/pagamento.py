from extensions import db
from datetime import datetime
class Pagamento(db.Model):
    """Modelo Pagamento - pagamento de um empréstimo"""
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    valor_juros = db.Column(db.Float, default=0)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    is_juros = db.Column(db.Boolean, nullable=True)

    # FK para empréstimo
    emprestimo_id = db.Column(db.Integer, db.ForeignKey('emprestimos.id'), nullable=False)

    def to_dict(self):
        """Converte pagamento para dicionário (JSON)"""
        valor = float(self.valor or 0)
        valor_juros = float(self.valor_juros or 0)

        if self.is_juros is True:
            valor_principal = 0.0
            tipo_pagamento = 'juros'
        elif self.is_juros is None and valor_juros > 0:
            valor_principal = max(valor, 0.0)
            tipo_pagamento = 'misto'
        elif valor_juros > 0:
            # Compatibilidade com registros antigos (valor = total)
            valor_principal = max(valor - valor_juros, 0.0)
            tipo_pagamento = 'misto' if valor_principal > 0 else 'juros'
        else:
            valor_principal = max(valor, 0.0)
            tipo_pagamento = 'principal'

        return {
            'id': self.id,
            'valor': valor,
            'valor_juros': valor_juros,
            'valor_principal': valor_principal,
            'tipo_pagamento': tipo_pagamento,
            'data': self.data.isoformat() if self.data else None,
            'emprestimo_id': self.emprestimo_id,
            'emprestimo_nome': self.emprestimo.cliente.nome if self.emprestimo and self.emprestimo.cliente else None,
            'is_juros': self.is_juros
        }
