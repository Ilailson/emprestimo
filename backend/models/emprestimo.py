from extensions import db
from datetime import datetime, timedelta
class Emprestimo(db.Model):
    """Modelo Empréstimo - dinheiro emprestado a um cliente"""
    __tablename__ = 'emprestimos'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    taxa_juros = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='em_aberto')  # em_aberto, pago, atrasado

    # FK para cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    # Relacionamento: vários pagamentos por empréstimo
    pagamentos = db.relationship('Pagamento', backref='emprestimo', lazy=True)

    def to_dict(self):
        """Converte empréstimo para dicionário (JSON)"""
        return {
            'id': self.id,
            'valor': self.valor,
            'taxa_juros': self.taxa_juros,
            'data': self.data.isoformat() if self.data else None,
            'status': self.status,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'valor_total': self.calcular_total(),
            'valor_pago': self.calcular_pago(),
            'valor_devedor': self.calcular_devedor()
        }

    def calcular_total(self):
        """Calcula valor total com juros"""
        meses = self.calcular_meses()
        return self.valor * (1 + (self.taxa_juros / 100) * meses)

    def calcular_pago(self):
        """Calcula valor já pago"""
        return sum(p.valor for p in self.pagamentos)

    def calcular_devedor(self):
        """Calcula valor devedor"""
        return self.calcular_total() - self.calcular_pago()

    def calcular_meses(self):
        """Calcula meses desde o empréstimo"""
        if not self.data:
            return 0
        return max(1, (datetime.utcnow() - self.data).days // 30)

    def verificar_status(self):
        """Verifica se está atrasado"""
        if self.status == 'pago':
            return 'pago'
        if self.calcular_devedor() <= 0:
            return 'pago'
        meses = self.calcular_meses()
        if meses > 3:
            return 'atrasado'
        return 'em_aberto'