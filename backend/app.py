from flask import Flask
from flask_cors import CORS
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar SQLAlchemy com a app
    db.init_app(app)
    CORS(app)

    # Importar modelos (para SQLAlchemy conhecer as classes)
    from models import cliente, emprestimo, pagamento

    # Registrar blueprints (rotas)
    from routes.cliente_routes import cliente_bp
    from routes.emprestimo_routes import emprestimo_bp
    from routes.pagamento_routes import pagamento_bp
    app.register_blueprint(cliente_bp)
    app.register_blueprint(emprestimo_bp)
    app.register_blueprint(pagamento_bp)

    # Criar tabelas se não existirem
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=5000)
