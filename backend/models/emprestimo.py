from extensions import db
from datetime import datetime, timedelta
class Emprestimo(db.Model):
    """Modelo Empréstimo - dinheiro emprestado a um cliente"""
    __tablename__ = 'emprestimos'

    id = db.Column(db.Integer, primary_key=True)
    valor_original = db.Column(db.Float, nullable=False)
    taxa_juros = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.DateTime, nullable=True)
    data_ultimo_calculo = db.Column(db.DateTime, nullable=True)
    saldo_devedor = db.Column(db.Float, nullable=True)
    total_pago = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='em_aberto')

    # FK para cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    # Relacionamento: vários pagamentos por empréstimo
    pagamentos = db.relationship('Pagamento', backref='emprestimo', lazy=True)

    def to_dict(self):
        """Converte empréstimo para dicionário (JSON)"""
        return {
            'id': self.id,
            'valor_original': self.valor_original,
            'taxa_juros': self.taxa_juros,
            'data': self.data.isoformat() if self.data else None,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'data_ultimo_calculo': self.data_ultimo_calculo.isoformat() if self.data_ultimo_calculo else None,
            'saldo_devedor': self.saldo_devedor,
            'total_pago': self.total_pago,
            'status': self.status,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'valor_total': self.calcular_total(),
            'juros': self.calcular_juros()
        }

    def calcular_juros(self):
        """Calcula juros sobre o saldo devedor atual (não sobre o valor original)"""
        if self.saldo_devedor is None:
            self.saldo_devedor = self.valor_original
        return self.saldo_devedor * (self.taxa_juros / 100)

    def calcular_total(self):
        """Calcula valor total: saldo devedor + juros"""
        return self.saldo_devedor + self.calcular_juros() if self.saldo_devedor else 0

    def calcular_meses_atraso(self):
        """Calcula meses de atraso"""
        if not self.data_vencimento:
            return 0
        dias = (datetime.utcnow() - self.data_vencimento).days
        return max(0, dias // 30)

    def verificar_status(self):
        """Verifica status automático basedo em saldo devedor"""
        if self.status == 'pago':
            return 'pago'
        if self.saldo_devedor is None or self.saldo_devedor <= 0:
            self.status = 'pago'
            self.saldo_devedor = 0
            return 'pago'
        if self.calcular_meses_atraso() > 0:
            return 'atrasado'
        return 'em_aberto'

    def aplicar_pagamento(self, valor_pagamento):
        """Aplica um pagamento atualizando saldo_devedor e total_pago"""
        self.total_pago = (self.total_pago or 0) + valor_pagamento
        self.saldo_devedor = self.saldo_devedor - valor_pagamento
        if self.saldo_devedor < 0:
            self.saldo_devedor = 0
        self.status = 'pago' if self.saldo_devedor <= 0 else 'em_aberto'
        db.session.commit()

    def atualizar_status(self):
        """Atualiza status baseado em saldo devedor e data de vencimento"""
        if self.saldo_devedor is None or self.saldo_devedor <= 0:
            self.status = 'pago'
        elif self.calcular_meses_atraso() > 0:
            self.status = 'atrasado'
        else:
            self.status = 'em_aberto'
        db.session.commit()