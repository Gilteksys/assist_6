# app/controllers/assistencia_controller.py
from flask import request, jsonify
from app.models import AssistenciaTecnica
from app.appcore.extensions import db

class AssistenciaController:
    
    @staticmethod
    def register():
        data = request.get_json()
        
        # Validação dos campos obrigatórios
        required_fields = ['razao_social', 'nome_fantasia', 'cnpj', 'telefone']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Campos obrigatórios faltando'}), 400
            
        # Verifica se já existe uma assistência com este CNPJ
        if AssistenciaTecnica.query.filter_by(cnpj=data['cnpj']).first():
            return jsonify({'error': 'CNPJ já cadastrado'}), 400
            
        try:
            nova_assistencia = AssistenciaTecnica(
                razao_social=data['razao_social'],
                nome_fantasia=data['nome_fantasia'],
                cnpj=data['cnpj'],
                telefone=data['telefone'],
                email=data.get('email'),  # Campos opcionais usam .get()
                endereco=data.get('endereco'),
                status=data.get('status', 'Ativa')  # Valor padrão se não fornecido
            )
            
            db.session.add(nova_assistencia)
            db.session.commit()
            
            return jsonify({
                'message': 'Assistência técnica cadastrada com sucesso',
                'assistencia': nova_assistencia.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': f'Erro ao cadastrar assistência técnica: {str(e)}'
            }), 500

    @staticmethod
    def list_all():
        try:
            assistencias = AssistenciaTecnica.query.all()
            return jsonify([assist.to_dict() for assist in assistencias]), 200
        except Exception as e:
            return jsonify({
                'error': f'Erro ao listar assistências técnicas: {str(e)}'
            }), 500

    @staticmethod
    def get(id):
        try:
            assistencia = AssistenciaTecnica.query.get(id)
            if not assistencia:
                return jsonify({
                    'error': 'Assistência técnica não encontrada'
                }), 404
                
            return jsonify(assistencia.to_dict()), 200
            
        except Exception as e:
            return jsonify({
                'error': f'Erro ao buscar assistência técnica: {str(e)}'
            }), 500

    @staticmethod
    def update(id):
        try:
            assistencia = AssistenciaTecnica.query.get(id)
            if not assistencia:
                return jsonify({
                    'error': 'Assistência técnica não encontrada'
                }), 404
                
            data = request.get_json()
            
            # Verifica se o novo CNPJ (se fornecido) já existe para outra assistência
            if 'cnpj' in data and data['cnpj'] != assistencia.cnpj:
                existing = AssistenciaTecnica.query.filter_by(
                    cnpj=data['cnpj']
                ).first()
                if existing:
                    return jsonify({
                        'error': 'CNPJ já cadastrado para outra assistência'
                    }), 400
            
            # Atualiza os campos se fornecidos
            for field in ['razao_social', 'nome_fantasia', 'cnpj', 'telefone', 
                         'email', 'endereco', 'status']:
                if field in data:
                    setattr(assistencia, field, data[field])
            
            db.session.commit()
            
            return jsonify({
                'message': 'Assistência técnica atualizada com sucesso',
                'assistencia': assistencia.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': f'Erro ao atualizar assistência técnica: {str(e)}'
            }), 500

    @staticmethod
    def delete(id):
        try:
            assistencia = AssistenciaTecnica.query.get(id)
            if not assistencia:
                return jsonify({
                    'error': 'Assistência técnica não encontrada'
                }), 404
                
            db.session.delete(assistencia)
            db.session.commit()
            
            return jsonify({
                'message': 'Assistência técnica excluída com sucesso'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': f'Erro ao excluir assistência técnica: {str(e)}'
            }), 500