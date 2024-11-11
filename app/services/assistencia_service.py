#assistencia_service.py

from app.models.assistencia_tecnica import AssistenciaTecnica
from app.appcore.extensions import db

class AssistenciaService:
    @staticmethod
    def create_assistencia(razao_social, nome_fantasia, cnpj, telefone, email=None, endereco=None):
        assistencia = AssistenciaTecnica(
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            cnpj=cnpj,
            telefone=telefone,
            email=email,
            endereco=endereco,            
        )
        
        db.session.add(assistencia)
        db.session.commit()
        return assistencia  # Retorna o objeto criado para ser manipulado ou retornado como resposta

