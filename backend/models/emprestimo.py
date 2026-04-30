from extensions import db
from datetime import datetime

class Emprestimo(db.Model):
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

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    pagamentos = db.relationship('Pagamento', backref='emprestimo', lazy=True)

    def to_dict(self):
        meses_atraso = self.calcular_meses_atraso()
        if self.saldo_devedor is None:
            self.saldo_devedor = self.valor_original
        juros_mensal = self.saldo_devedor * (self.taxa_juros / 100)
        if meses_atraso <= 0:
            juros_acumulados = juros_mensal
        else:
            juros_acumulados = juros_mensal * meses_atraso
        return {
            'id': self.id,
            'valor_original': self.valor_original,
            'taxa_juros': self.taxa_juros,
            'data': self.data.isoformat() if self.data else None,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'data_ultimo_calculo': self.data_ultimo_calculo.isoformat() if self.data_ultimo_calculo else None,
            'saldo_devedor': self.saldo_devedor,
            'total_pago': self.total_pago,
            'status': self.verificar_status(),
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'valor_total': self.calcular_total(),
            'juros': juros_mensal,
            'juros_acumulados': juros_acumulados,
            'meses_atraso': meses_atraso
        }

    def calcular_meses_atraso(self):
        if not self.data_vencimento:
            return 0
        agora = datetime.utcnow()
        if agora <= self.data_vencimento:
            return 0
        anos = agora.year - self.data_vencimento.year
        meses = agora.month - self.data_vencimento.month
        dias = agora.day - self.data_vencimento.day
        total_meses = anos * 12 + meses
        if dias < 0:
            total_meses -= 1
        return max(0, total_meses)

    def calcular_juros(self):
        if self.saldo_devedor is None:
            self.saldo_devedor = self.valor_original
        return self.saldo_devedor * (self.taxa_juros / 100)

    def calcular_juros_acumulados(self):
        meses_atraso = self.calcular_meses_atraso()
        if self.saldo_devedor is None:
            self.saldo_devedor = self.valor_original
        juros_mensal = self.saldo_devedor * (self.taxa_juros / 100)
        if meses_atraso <= 0:
            return juros_mensal
        else:
            return juros_mensal * meses_atraso

    def calcular_total(self):
        meses_atraso = self.calcular_meses_atraso()
        juros_mensal = self.calcular_juros()
        if meses_atraso <= 0:
            juros_acumulados = juros_mensal
        else:
            juros_acumulados = juros_mensal * meses_atraso
        return (self.saldo_devedor or 0) + juros_acumulados

    def verificar_status(self):
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
        self.total_pago = (self.total_pago or 0) + valor_pagamento
        self.saldo_devedor = self.saldo_devedor - valor_pagamento
        if self.saldo_devedor < 0:
            self.saldo_devedor = 0
        self.status = 'pago' if self.saldo_devedor <= 0 else 'em_aberto'
        db.session.commit()

    def atualizar_status(self):
        if self.saldo_devedor is None or self.saldo_devedor <= 0:
            self.status = 'pago'
        elif self.calcular_meses_atraso() > 0:
            self.status = 'atrasado'
        else:
            self.status = 'em_aberto'
        db.session.commit()
