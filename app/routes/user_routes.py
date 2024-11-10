# app/routes/user_routes.py
from flask import Blueprint
from app.controllers.user_controller import UserController

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

user_bp.add_url_rule('/register', 'register', UserController.register, methods=['POST'])
user_bp.add_url_rule('/login', 'login', UserController.login, methods=['POST'])


#user_bp.add_url_rule('/busca', 'busca', UserController.buscar, methods=['GET'])
