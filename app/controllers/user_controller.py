# app/controllers/user_controller.py
from flask import jsonify, request
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token

class UserController:
    @staticmethod
    def register():
        data = request.get_json()
        
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Dados incompletos'}), 400
            
        try:
            user = UserService.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return jsonify(user.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @staticmethod
    def login():
        data = request.get_json()
        
        user = UserService.get_user_by_username(data.get('username'))
        if user and user.check_password(data.get('password')):
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
            
        return jsonify({'error': 'Credenciais inválidas'}), 401   
    
    
    

    
    
