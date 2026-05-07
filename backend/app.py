from flask import Flask
from flask_cors import CORS
from extensions import db, jwt, limiter

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar extensões (apenas uma vez)
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # CORS SEGURO: Permitir apenas domínio do frontend Vue
    CORS(app, origins=[app.config['FRONTEND_URL']], supports_credentials=True)

    # Importar models e routes
    from models import cliente, emprestimo, pagamento, usuario
    from routes.cliente_routes import cliente_bp
    from routes.emprestimo_routes import emprestimo_bp
    from routes.pagamento_routes import pagamento_bp
    from routes.auth_routes import auth_bp

    # Registrar blueprints
    app.register_blueprint(cliente_bp)
    app.register_blueprint(emprestimo_bp)
    app.register_blueprint(pagamento_bp)
    app.register_blueprint(auth_bp)

    # Criar tabelas e usuário admin padrão
    with app.app_context():
        db.create_all()

        from models.usuario import Usuario
        if not Usuario.query.filter_by(login='admin').first():
            admin = Usuario(
                nome='Administrador',
                login='admin',
                role='admin'
            )
            admin.set_senha('admin123')  # ALTERE ESSA SENHA EM PRODUÇÃO!
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado: login=admin, senha=admin123")

    return app


if __name__ == '__main__':
    import os
    debug = os.environ.get('FLASK_ENV') != 'production'
    app = create_app()
    app.run(debug=debug, host='0.0.0.0', port=5000)
