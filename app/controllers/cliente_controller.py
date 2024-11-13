# app/controllers/cliente_controller.py
from flask import request, jsonify
from app.services.cliente_service import ClienteService
from app.models.cadastro_cliente import CadastroCliente  # Assumindo que você tem o modelo Cliente

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
        
        
    @staticmethod    
    def list_all():
            try:
                # Busca todos os clientes no banco de dados
                clientes = CadastroCliente.query.all()
                
                # Converte os objetos Cliente para dicionários
                clientes_json = [
                    {
                        'id': cliente.id,
                        'nome': cliente.nome,
                        'contato': cliente.contato,
                        'email': cliente.email,
                        'documento': cliente.documento
                    }
                    for cliente in clientes
                ]
                
                return jsonify(clientes_json), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        
        

    @staticmethod
    def get(cliente_id):
        # Busca um cliente pelo ID
        cliente = CadastroCliente.query.get(cliente_id)  # Assumindo que o método `get` no modelo Cliente funciona corretamente
        if not cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        return jsonify(cliente.to_dict()), 200

    @staticmethod
    def update(cliente_id):
        # Recebe os dados da requisição JSON
        data = request.get_json()

        # Tenta buscar o cliente pelo ID
        cliente = CadastroCliente.query.get(cliente_id)
        if not cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404

        # Atualiza os dados do cliente
        nome = data.get('nome', cliente.nome)
        documento = data.get('documento', cliente.documento)
        contato = data.get('contato', cliente.contato)
        endereco = data.get('endereco', cliente.endereco)
        email = data.get('email', cliente.email)

        try:
            # Chama o serviço de atualização de cliente
            updated_cliente = ClienteService.update_cliente(
                cliente_id=cliente_id,
                nome=nome,
                documento=documento,
                contato=contato,
                endereco=endereco,
                email=email
            )

            return jsonify(updated_cliente.to_dict()), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete(cliente_id):
        # Tenta buscar o cliente pelo ID
        cliente = CadastroCliente.query.get(cliente_id)
        if not cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404

        try:
            # Chama o serviço para excluir o cliente
            ClienteService.delete_cliente(cliente_id)
            return jsonify({"message": "Cliente excluído com sucesso"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
