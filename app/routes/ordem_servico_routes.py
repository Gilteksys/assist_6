# app/routes/ordem_routes.py
from flask import Blueprint
from app.controllers.ordem_controller import OrdemController

ordem_bp = Blueprint('ordem', __name__, url_prefix='/api/ordens')
ordem_bp.add_url_rule('/register', 'register', OrdemController.register, methods=['POST'])