# __init__.py

from flask import Flask
from app.appcore.extensions import db, migrate, jwt
from app.appcore.config import Config
from app.routes.user_routes import user_bp
from app.routes.assistencia_routes import assistencia_bp
from app.routes.cliente_routes import cliente_bp
from app.routes.ordem_servico_routes import ordem_bp
from app.models.user import User
from app.models import assistencia_tecnica
from app.models import cadastro_cliente
from app.models import ordem_servico


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
        
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # Inicialize o JWTManager aqui
    
    # Register blueprints
    
    app.register_blueprint(user_bp)
    app.register_blueprint(assistencia_bp)    
    app.register_blueprint(cliente_bp) 
    app.register_blueprint(ordem_bp)
    
    return app