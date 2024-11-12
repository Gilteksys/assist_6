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
    pecas_utilizadas = db.Column(db.String(200), nullable=True)
    garantia = db.Column(db.Text(300), nullable=False)
    valor_conserto = db.Column(db.Float, nullable=True)    
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('cadastro_cliente.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'aparelho': self.aparelho,
            'marca': self.marca,
            'modelo': self.modelo,  
            'serial': self.serial,
            'defeito': self.defeito,
            'pecas_utilizadas': self.pecas_utilizadas,  
            'valor_conserto': self.valor_conserto,  
            'garantia': self.garantia,
            'criado_em': self.criado_em.isoformat(),         
            'cliente_id': self.cliente_id  
        }
        
        
        
        
        
