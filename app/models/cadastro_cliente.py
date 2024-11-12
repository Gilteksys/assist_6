# app/models/cliente.py
from app.appcore.extensions import db
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

class CadastroCliente(db.Model):
    __tablename__ = 'cadastro_cliente'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    documento = db.Column(db.String(100), nullable=True)    
    contato = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(150), nullable=True, unique=True)  # Campo de email
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ordens_servico = db.relationship('OrdemServico', backref='cadastro_cliente', lazy=True)

    def validate_email(self, email):
        try:
            # tenta validar o email
            valid = validate_email(email)
            # atualiza o email com o valor validado
            self.email = valid.email
            return True
        except EmailNotValidError as e:
            # email inválido, retorna False e a mensagem de erro
            return False, str(e)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'contato': self.contato,
            'email': self.email,  
            'documento': self.documento,
            'endereco': self.endereco,
            'criado_em': self.criado_em.isoformat(),
            'ordens_servico': [ordem.to_dict() for ordem in self.ordens_servico]           
        }


