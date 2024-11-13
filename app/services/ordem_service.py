# app/services/ordem_service.py
from app.models.ordem_servico import OrdemServico
from app.appcore.extensions import db
from app.models.cadastro_cliente import CadastroCliente

class OrdemService:
    @staticmethod
    def create_ordem(aparelho, pecas_utilizadas, valor_conserto, garantia,  cliente_id, marca=None, modelo=None, serial=None, defeito=None): 
        if cliente_id is None:
            raise ValueError("Cliente ID é obrigatório")
        
         # Verifica se o cliente existe
        cliente = CadastroCliente.query.get(cliente_id)
        if not cliente:
            raise ValueError("Cliente ID fornecido não existe")
        
        # Criação do objeto ordem de serviço
        ordem = OrdemServico(               
            aparelho=aparelho,
            marca=marca,
            modelo=modelo,
            serial=serial,
            defeito=defeito, 
            pecas_utilizadas=pecas_utilizadas,  
            valor_conserto=valor_conserto,  
            garantia=garantia,
            cliente_id=cliente_id           
        )

        # Adiciona a ordem ao banco de dados
        db.session.add(ordem)
        db.session.commit()
        return ordem  # Retorna a ordem recém-criada