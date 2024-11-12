# app/models/peca_utilizadas.py
from app.appcore.extensions import db

class Peca_utilizadas(db.Model):
    __tablename__ = 'pecas_utilizadas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1) 
    gaveta = db.Column(db.String(50), nullable=True)
    valor = db.Column(db.Float, nullable=False)   
   
    

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'gaveta': self.gaveta,
            'valor': self.valor
        }
