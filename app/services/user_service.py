# app/services/user_service.py
from app.models.user import User
from app.extensions import db

class UserService:
    @staticmethod
    def create_user(username, email, password, role='user'):
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
    
    
