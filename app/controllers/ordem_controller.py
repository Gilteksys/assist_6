# app/controllers/cliente_controller.py
from flask import request, jsonify
from app.services.ordem_service import OrdemService

class OrdemController:
    @staticmethod
    def register():
        # Recebe os dados da requisição JSON
        data = request.get_json()

        # Extrai os dados para criar o cliente
        aparelho = data.get('aparelho')
        marca = data.get('marca')
        modelo = data.get('modelo')
        serial = data.get('serial')
        defeito = data.get('defeito')
        pecas_utilizadas= data.get('pecas_utilizadas')
        valor_conserto= data.get('valor_conserto')
        garantia= data.get('garantia')
        cliente_id = data.get('cliente_id')

        try:
            # Cria a ordem chamando o serviço OrdemService
            ordem = OrdemService.create_ordem(
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

            # Se ordem for criada com sucesso, retorna a resposta a ordem
            return jsonify(ordem.to_dict()), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400