"""
Adiciona coluna is_juros à tabela pagamentos
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
                WHERE table_name = 'pagamentos' AND column_name = 'is_juros'
            """))
            if not result.fetchone():
                print("Adicionando coluna is_juros...")
                conn.execute(db.text("""
                    ALTER TABLE pagamentos ADD COLUMN is_juros BOOLEAN DEFAULT FALSE
                """))
                conn.commit()
                print("Coluna is_juros adicionada!")
            else:
                print("Coluna is_juros já existe")

if __name__ == '__main__':
    migrate()