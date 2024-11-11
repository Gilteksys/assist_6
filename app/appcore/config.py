#config.py
import os
from datetime import timedelta
SECRET_KEY = 'dde6b92df4ae2e1f17095c532f7d38218b3f85dcfd18c9d5c097ab86236208208'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///assistencia_tecnica.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

