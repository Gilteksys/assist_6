import logging
from app.models.cadastro_cliente import CadastroCliente
from app.appcore.extensions import db

# Configuração do logger
logger = logging.getLogger(__name__)

class ClienteService:
    @staticmethod
    def create_cliente(nome, contato, documento=None, endereco=None, email=None):
        """
        Cria um novo cliente no banco de dados.
        
        Args:
            nome (str): Nome do cliente (obrigatório)
            contato (str): Contato do cliente (obrigatório)
            documento (str, optional): Documento do cliente
            endereco (str, optional): Endereço do cliente
            email (str, optional): Email do cliente
            
        Returns:
            CadastroCliente: Objeto do cliente criado
            
        Raises:
            ValueError: Se os dados forem inválidos
            Exception: Se ocorrer erro durante a criação
        """
        try:
            logger.info(f"Iniciando criação de cliente: {nome}")
            
            # Validação dos campos obrigatórios
            if not nome or not contato:
                raise ValueError("Nome e contato são campos obrigatórios")
            
            # Validação do email
            if email and '@' not in email:
                raise ValueError("Formato de email inválido")
            
            # Verificação de documento duplicado
            if documento:
                cliente_existente = CadastroCliente.query.filter_by(documento=documento).first()
                if cliente_existente:
                    raise ValueError("Já existe um cliente cadastrado com este documento")
            
            # Verificação de email duplicado
            if email:
                cliente_existente = CadastroCliente.query.filter_by(email=email).first()
                if cliente_existente:
                    raise ValueError("Já existe um cliente cadastrado com este email")
            
            # Criação do objeto cliente
            cliente = CadastroCliente(
                nome=nome,
                contato=contato,
                documento=documento,
                endereco=endereco,
                email=email
            )
            
            # Salvando no banco de dados
            db.session.add(cliente)
            db.session.commit()
            
            logger.info(f"Cliente criado com sucesso: ID {cliente.id}")
            return cliente
            
        except Exception as e:
            logger.error(f"Erro ao criar cliente: {str(e)}")
            db.session.rollback()
            raise Exception(f"Erro ao criar cliente: {str(e)}")

    @staticmethod
    def get_cliente(cliente_id):
        """
        Busca um cliente pelo ID.
        
        Args:
            cliente_id: ID do cliente
            
        Returns:
            CadastroCliente: Objeto do cliente encontrado
            
        Raises:
            ValueError: Se o cliente não for encontrado
        """
        try:
            logger.info(f"Buscando cliente ID: {cliente_id}")
            
            cliente = CadastroCliente.query.get(cliente_id)
            if not cliente:
                raise ValueError("Cliente não encontrado")
                
            return cliente
            
        except Exception as e:
            logger.error(f"Erro ao buscar cliente: {str(e)}")
            raise

    @staticmethod
    def update_cliente(cliente_id, nome=None, contato=None, documento=None, endereco=None, email=None):
        """
        Atualiza os dados de um cliente existente.
        
        Args:
            cliente_id: ID do cliente
            nome (str, optional): Novo nome
            contato (str, optional): Novo contato
            documento (str, optional): Novo documento
            endereco (str, optional): Novo endereço
            email (str, optional): Novo email
            
        Returns:
            CadastroCliente: Objeto do cliente atualizado
            
        Raises:
            ValueError: Se o cliente não for encontrado ou dados forem inválidos
            Exception: Se ocorrer erro durante a atualização
        """
        try:
            logger.info(f"Iniciando atualização do cliente ID: {cliente_id}")
            
            cliente = CadastroCliente.query.get(cliente_id)
            if not cliente:
                raise ValueError("Cliente não encontrado")
            
            modificado = False
            
            # Validação e atualização do email
            if email:
                if '@' not in email:
                    raise ValueError("Formato de email inválido")
                    
                cliente_existente = CadastroCliente.query.filter(
                    CadastroCliente.email == email,
                    CadastroCliente.id != cliente_id
                ).first()
                
                if cliente_existente:
                    raise ValueError("Email já está em uso por outro cliente")
                    
                if email != cliente.email:
                    cliente.email = email
                    modificado = True
            
            # Validação e atualização do documento
            if documento:
                cliente_existente = CadastroCliente.query.filter(
                    CadastroCliente.documento == documento,
                    CadastroCliente.id != cliente_id
                ).first()
                
                if cliente_existente:
                    raise ValueError("Documento já está em uso por outro cliente")
                    
                if documento != cliente.documento:
                    cliente.documento = documento
                    modificado = True
            
            # Atualização dos demais campos
            if nome and nome != cliente.nome:
                cliente.nome = nome
                modificado = True
                
            if contato and contato != cliente.contato:
                cliente.contato = contato
                modificado = True
                
            if endereco and endereco != cliente.endereco:
                cliente.endereco = endereco
                modificado = True
            
            # Salva as alterações se houve modificação
            if modificado:
                db.session.commit()
                logger.info(f"Cliente ID {cliente_id} atualizado com sucesso")
            else:
                logger.info(f"Nenhuma modificação necessária para o cliente ID {cliente_id}")
            
            return cliente
            
        except Exception as e:
            logger.error(f"Erro ao atualizar cliente: {str(e)}")
            db.session.rollback()
            raise Exception(f"Erro ao atualizar cliente: {str(e)}")

    @staticmethod
    def delete_cliente(cliente_id):
        """
        Remove um cliente do banco de dados.
        
        Args:
            cliente_id: ID do cliente a ser removido
            
        Returns:
            bool: True se cliente foi removido com sucesso
            
        Raises:
            ValueError: Se cliente não for encontrado
            Exception: Se ocorrer erro durante a remoção
        """
        try:
            logger.info(f"Iniciando remoção do cliente ID: {cliente_id}")
            
            cliente = CadastroCliente.query.get(cliente_id)
            if not cliente:
                raise ValueError("Cliente não encontrado")
            
            db.session.delete(cliente)
            db.session.commit()
            
            logger.info(f"Cliente ID {cliente_id} removido com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover cliente: {str(e)}")
            db.session.rollback()
            raise Exception(f"Erro ao remover cliente: {str(e)}")

    @staticmethod
    def list_clientes():
        """
        Lista todos os clientes cadastrados.
        
        Returns:
            list: Lista de objetos CadastroCliente
            
        Raises:
            Exception: Se ocorrer erro durante a consulta
        """
        try:
            logger.info("Listando todos os clientes")
            return CadastroCliente.query.all()
            
        except Exception as e:
            logger.error(f"Erro ao listar clientes: {str(e)}")
            raise Exception(f"Erro ao listar clientes: {str(e)}")
