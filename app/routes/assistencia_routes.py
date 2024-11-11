# app/routes/assistencia_routes.py
from flask import Blueprint
from app.controllers.assistencia_controller import AssistenciaController

assistencia_bp = Blueprint('assistencia', __name__, url_prefix='/api/assistencias')

assistencia_bp.add_url_rule('/register', 'register', AssistenciaController.register, methods=['POST'])