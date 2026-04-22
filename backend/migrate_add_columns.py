from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    conn = db.engine.connect()
    
    result = conn.execute(db.text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'emprestimos'
    """))
    existing_cols = [row[0] for row in result]
    print(f"Colunas existentes: {existing_cols}")
    
    if 'data_vencimento' not in existing_cols:
        conn.execute(db.text("""
            ALTER TABLE emprestimos ADD COLUMN data_vencimento TIMESTAMP
        """))
        print("✓ Coluna data_vencimento adicionada")
    else:
        print("✓ Coluna data_vencimento já existe")
    
    if 'data_ultimo_calculo' not in existing_cols:
        conn.execute(db.text("""
            ALTER TABLE emprestimos ADD COLUMN data_ultimo_calculo TIMESTAMP
        """))
        print("✓ Coluna data_ultimo_calculo adicionada")
    else:
        print("✓ Coluna data_ultimo_calculo já existe")
    
    if 'saldo_atual' not in existing_cols:
        conn.execute(db.text("""
            ALTER TABLE emprestimos ADD COLUMN saldo_atual DOUBLE PRECISION
        """))
        print("✓ Coluna saldo_atual adicionada")
    else:
        print("✓ Coluna saldo_atual já existe")
    
    conn.commit()
    conn.close()
    print("\nMigration concluída!")