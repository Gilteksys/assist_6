# app/controllers/cliente_controller.py
from flask import request, jsonify
from app.services.cliente_service import ClienteService

class ClienteController:
    @staticmethod
    def register():
        # Recebe os dados da requisição JSON
        data = request.get_json()

        # Extrai os dados para criar o cliente
        nome = data.get('nome')
        documento = data.get('documento')
        contato = data.get('contato')
        endereco = data.get('endereco')
        email = data.get('email')

        try:
            # Cria o cliente chamando o serviço ClienteService
            cliente = ClienteService.create_cliente(
                nome=nome,
                contato=contato,
                documento=documento,
                endereco=endereco,
                email=email,                
            )

            # Se o cliente for criado com sucesso, retorna a resposta com o cliente
            return jsonify(cliente.to_dict()), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400
