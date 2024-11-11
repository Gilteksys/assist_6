#assistencia_controller.py
from flask import jsonify, request
from app.services.assistencia_service import AssistenciaService

class AssistenciaController:
    @staticmethod
    def register():
        # Obtendo os dados da requisição
        data = request.get_json()
        
        # Verificando se todos os campos obrigatórios estão presentes
        required_fields = ['razao_social', 'nome_fantasia', 'cnpj', 'telefone']
        if not all(k in data for k in required_fields):
            return jsonify({'error': 'Dados incompletos'}), 400
            
        try:
            # Chamando o método estático 'create_assistencia' para criar a nova assistência
            assistencia = AssistenciaService.create_assistencia(
                razao_social=data['razao_social'],
                nome_fantasia=data['nome_fantasia'],
                cnpj=data['cnpj'],
                telefone=data['telefone'],
                email=data.get('email'),  # email é opcional
                endereco=data.get('endereco'),  # endereco é opcional
            )
            
            # Retornando a resposta com os dados da nova assistência criada
            return jsonify(assistencia.to_dict()), 201
        
        except Exception as e:
            # Caso ocorra algum erro, retorna a mensagem de erro
            return jsonify({'error': str(e)}), 400
