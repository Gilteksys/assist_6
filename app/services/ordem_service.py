# app/services/ordem_service.py
from app.models.ordem_servico import OrdemServico
from app.appcore.extensions import db

class OrdemService:
    @staticmethod
    def create_ordem(aparelho, pecas_utilizadas, valor_conserto, garantia, marca=None, modelo=None, serial=None, defeito=None, cliente_id=None,): 
        if cliente_id is None:
            raise ValueError("Assistência ID é obrigatório")
        
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