"""
Script de migração para adicionar novas colunas à tabela.emprestimos
Executar: cd backend && python migrate_emprestimo.py
"""
from extensions import db
from app import create_app

def migrate():
    app = create_app()
    with app.app_context():
        with db.engine.connect() as conn:
            # Verificar se coluna valor_original existe
            result = conn.execute(db.text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'emprestimos' AND column_name = 'valor_original'
            """))
            if not result.fetchone():
                print("Adicionando coluna valor_original...")
                conn.execute(db.text("""
                    ALTER TABLE emprestimos ADD COLUMN valor_original FLOAT
                """))
            
            # Verificar se coluna saldo_devedor existe
            result = conn.execute(db.text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'emprestimos' AND column_name = 'saldo_devedor'
            """))
            if not result.fetchone():
                print("Adicionando columna saldo_devedor...")
                conn.execute(db.text("""
                    ALTER TABLE emprestimos ADD COLUMN saldo_devedor FLOAT
                """))
            
            # Verificar se coluna total_pago existe
            result = conn.execute(db.text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'emprestimos' AND column_name = 'total_pago'
            """))
            if not result.fetchone():
                print("Adicionando coluna total_pago...")
                conn.execute(db.text("""
                    ALTER TABLE emprestimos ADD COLUMN total_pago FLOAT DEFAULT 0
                """))
            
            # Copiar dados de valor para valor_original
            print("Copiando valores existentes para novas colunas...")
            conn.execute(db.text("""
                UPDATE emprestimos 
                SET valor_original = valor, 
                    saldo_devedor = COALESCE(saldo_devedor, valor),
                    total_pago = COALESCE(total_pago, 0)
                WHERE valor_original IS NULL
            """))
            
            conn.commit()
    
    print("Migração concluída com sucesso!")

if __name__ == '__main__':
    migrate()