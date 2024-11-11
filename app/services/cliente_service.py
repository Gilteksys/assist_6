# app/services/cliente_service.py
from app.models.cadastro_cliente import CadastroCliente
from app.appcore.extensions import db

class ClienteService:
    @staticmethod
    def create_cliente(nome, contato, documento=None, endereco=None, email=None):     
        
        cliente = CadastroCliente(   # Criação do objeto cliente com os dados fornecidos e o assistencia_id encontrado
            nome=nome,
            contato=contato,
            documento=documento,
            endereco=endereco,
            email=email            
        )

        # Adiciona o cliente ao banco de dados
        db.session.add(cliente)
        db.session.commit()
        return cliente  # Retorna o cliente recém-criado


    
    
    
