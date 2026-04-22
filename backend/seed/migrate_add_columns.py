"""
Script de migração para adicionar novas colunas à tabela.emprestimos
Executar: python -m seed.migrate_add_columns
"""
from extensions import db
from app import create_app

def migrate():
    app = create_app()
    with app.app_context():
        connection = db.engine.connect()
        
        # Verificar se coluna valor_original existe
        result = connection.execute(db.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'emprestimos' AND column_name = 'valor_original'
        """))
        
        if result.fetchone() is None:
            print("Adicionando coluna valor_original...")
            connection.execute(db.text("""
                ALTER TABLE emprestimos 
                ADD COLUMN valor_original FLOAT
            """))
        
        # Verificar se coluna saldo_devedor existe
        result = connection.execute(db.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'emprestimos' AND column_name = 'saldo_devedor'
        """))
        
        if result.fetchone() is None:
            print("Adicionando coluna saldo_devedor...")
            connection.execute(db.text("""
                ALTER TABLE emprestimos 
                ADD COLUMN saldo_devedor FLOAT
            """))
        
        # Verificar se coluna total_pago existe
        result = connection.execute(db.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'emprestimos' AND column_name = 'total_pago'
        """))
        
        if result.fetchone() is None:
            print("Adicionando coluna total_pago...")
            connection.execute(db.text("""
                ALTER TABLE emprestimos 
                ADD COLUMN total_pago FLOAT DEFAULT 0
            """))
        
        # Copiar dados de valor para valor_original (onde ainda não existe)
        print("Copiando valores existentes...")
        connection.execute(db.text("""
            UPDATE emprestimos 
            SET valor_original = valor, 
                saldo_devedor = COALESCE(saldo_devedor, valor),
                total_pago = COALESCE(total_pago, 0)
            WHERE valor_original IS NULL
        """))
        
        connection.commit()
        connection.close()
        print("Migração concluída!")

if __name__ == '__main__':
    migrate()