# __init__.py

from flask import Flask
from app.extensions import db, migrate, jwt
from app.config import Config
from app.routes.user_routes import user_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    
    # Force SQLAlchemy to recognize models

    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # Inicialize o JWTManager aqui
    
    # Register blueprints
    
    app.register_blueprint(user_bp)
    
    
    return app