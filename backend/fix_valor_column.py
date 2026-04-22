"""
Remove coluna valor antiga do banco
"""
from extensions import db
from app import create_app

def migrate():
    app = create_app()
    with app.app_context():
        with db.engine.connect() as conn:
            # Verificar se coluna valor existe
            result = conn.execute(db.text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'emprestimos' AND column_name = 'valor'
            """))
            if result.fetchone():
                print("Removendo coluna valor...")
                conn.execute(db.text("""
                    ALTER TABLE emprestimos DROP COLUMN valor
                """))
                print("Coluna valor removida!")
            else:
                print("Coluna valor não existe")
            
            conn.commit()
    
    print("Migração concluída!")

if __name__ == '__main__':
    migrate()