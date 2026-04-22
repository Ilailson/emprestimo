"""
Adiciona coluna valor_juros à tabela pagamentos
"""
from extensions import db
from app import create_app

def migrate():
    app = create_app()
    with app.app_context():
        with db.engine.connect() as conn:
            result = conn.execute(db.text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'pagamentos' AND column_name = 'valor_juros'
            """))
            if not result.fetchone():
                print("Adicionando coluna valor_juros...")
                conn.execute(db.text("""
                    ALTER TABLE pagamentos ADD COLUMN valor_juros DECIMAL(12,2) DEFAULT 0
                """))
                conn.commit()
                print("Coluna valor_juros adicionada!")
            else:
                print("Coluna valor_juros já existe")

if __name__ == '__main__':
    migrate()