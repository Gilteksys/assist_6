# app/services/ordem_service.py
from app.models.ordem_servico import OrdemServico
from app.appcore.extensions import db

class OrdemService:
    @staticmethod
    def create_ordem(aparelho, marca=None, modelo=None, serial=None, defeito=None):     
        
        ordem = OrdemServico(   # Criação do objeto ordem de serviço
            aparelho=aparelho,
            marca=marca,
            modelo=modelo,
            serial=serial,
            defeito=defeito            
        )

        # Adiciona a ordem ao banco de dados
        db.session.add(ordem)
        db.session.commit()
        return ordem  # Retorna a ordem recém-criada