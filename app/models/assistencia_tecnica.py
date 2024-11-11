# app/models/assistencia_tecnica.py
from app.appcore.extensions import db
from datetime import datetime

class AssistenciaTecnica(db.Model):
    __tablename__ = 'assistencia_tecnica'
    
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150), nullable=False)
    nome_fantasia = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)    
    status = db.Column(db.String(50), nullable=False, default='Ativa')
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)    

    def to_dict(self):
        return {
            'id': self.id,
            'razao_social': self.razao_social,
            'nome_fantasia': self.nome_fantasia,
            'cnpj': self.cnpj,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,            
            'status': self.status,
            'criado_em': self.criado_em.isoformat(),      
        }




