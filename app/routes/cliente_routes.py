# app/routes/cliente_routes.py
from flask import Blueprint
from app.controllers.cliente_controller import ClienteController

cliente_bp = Blueprint('cliente', __name__, url_prefix='/api/clientes')

# Rota para listar todos os clientes (GET)
cliente_bp.add_url_rule('', 'list_clientes', ClienteController.list_all, methods=['GET'])

# Rota para registrar um cliente (POST)
cliente_bp.add_url_rule('/register', 'register', ClienteController.register, methods=['POST'])

# Rota para obter um cliente específico pelo ID (GET)
cliente_bp.add_url_rule('/<int:cliente_id>', 'get_cliente', ClienteController.get, methods=['GET'])

# Rota para atualizar um cliente específico pelo ID (PUT)
cliente_bp.add_url_rule('/<int:cliente_id>', 'update_cliente', ClienteController.update, methods=['PUT'])

# Rota para excluir um cliente específico pelo ID (DELETE)
cliente_bp.add_url_rule('/<int:cliente_id>', 'delete_cliente', ClienteController.delete, methods=['DELETE'])
