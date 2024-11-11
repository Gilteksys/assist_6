# app/models/ordem_servico.py
from app.appcore.extensions import db
from datetime import datetime

class OrdemServico(db.Model):
    __tablename__ = 'ordem_de_servico'
    
    id = db.Column(db.Integer, primary_key=True)
    aparelho = db.Column(db.String(150), nullable=False)
    marca = db.Column(db.String(100), nullable=True)    
    modelo = db.Column(db.String(100), nullable=True)
    serial = db.Column(db.String(100), nullable=True)
    defeito = db.Column(db.String(150), nullable=True) 
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'aparelho': self.aparelho,
            'marca': self.marca,
            'modelo': self.modelo,  
            'serial': self.serial,
            'defeito': self.defeito,
            'criado_em': self.criado_em.isoformat(),           
        }