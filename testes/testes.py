from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.appcore.extensions import db

# Criar Blueprint para rotas de usuário
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Verificar se todos os campos necessários estão presentes
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    # Verificar se usuário já existe
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Nome de usuário já existe'}), 400
    
    # Verificar se email já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 400
    
    try:
        # Criar novo usuário
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        # Adicionar à base de dados
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar usuário: {str(e)}'}), 500

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Verificar se todos os campos necessários estão presentes
    if not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        # Buscar usuário
        user = User.query.filter_by(username=data['username']).first()
        
        # Verificar se usuário existe e senha está correta
        if user and user.check_password(data['password']):
            if not user.active:
                return jsonify({'error': 'Conta desativada'}), 401
                
            # Criar token JWT
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                'message': 'Login realizado com sucesso',
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
        
        return jsonify({'error': 'Usuário ou senha inválidos'}), 401
        
    except Exception as e:
        return jsonify({'error': f'Erro ao realizar login: {str(e)}'}), 500

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        # Obter ID do usuário do token JWT
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar perfil: {str(e)}'}), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'email' in data:
            # Verificar se email já existe
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != current_user_id:
                return jsonify({'error': 'Email já cadastrado'}), 400
            user.email = data['email']
            
        if 'password' in data:
            user.set_password(data['password'])
            
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar perfil: {str(e)}'}), 500