# app/routes/cliente_routes.py
from flask import Blueprint
from app.controllers.cliente_controller import ClienteController

cliente_bp = Blueprint('cliente', __name__, url_prefix='/api/clientes')

cliente_bp.add_url_rule('/register', 'register', ClienteController.register, methods=['POST'])