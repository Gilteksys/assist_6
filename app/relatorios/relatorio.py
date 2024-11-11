from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import datetime

def gerar_relatorio(assistencia, cliente, ordem):
    # Nome do arquivo e configuração básica
    filename = "relatorio_ordem_servico.pdf"
    pdf = SimpleDocTemplate(filename, pagesize=A4)
    
    # Estilos de texto
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 18
    normal_style = styles['BodyText']
    
    # Elementos do documento
    elements = []
    
    # Cabeçalho com título
    elements.append(Paragraph("Relatório de Ordem de Serviço", title_style))
    elements.append(Spacer(1, 12))
    
    # Informações da Assistência
    elements.append(Paragraph("Informações da Assistência", styles['Heading2']))
    assistencia_data = [
        ["Nome", assistencia['nome']],
        ["CNPJ", assistencia['cnpj']],
        ["Telefone", assistencia['telefone']],
        ["Email", assistencia['email']],
        ["Endereço", assistencia['endereco']]
    ]
    table_assistencia = Table(assistencia_data)
    table_assistencia.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table_assistencia)
    elements.append(Spacer(1, 12))

    # Informações do Cliente
    elements.append(Paragraph("Informações do Cliente", styles['Heading2']))
    cliente_data = [
        ["Nome", cliente['nome']],
        ["Documento", cliente['documento']],
        ["Contato", cliente['contato']],
        ["Email", cliente['email']],
        ["Endereço", cliente['endereco']]
    ]
    table_cliente = Table(cliente_data)
    table_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table_cliente)
    elements.append(Spacer(1, 12))

    # Informações da Ordem de Serviço
    elements.append(Paragraph("Informações da Ordem de Serviço", styles['Heading2']))
    ordem_data = [
        ["ID", ordem['id']],
        ["Data de Criação", ordem['criado_em']],
        ["Aparelho", ordem['aparelho']],
        ["Marca", ordem['marca']],
        ["Modelo", ordem['modelo']],
        ["Número de Série", ordem['serial']],
        ["Defeito Reportado", ordem['defeito']]
    ]
    table_ordem = Table(ordem_data)
    table_ordem.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table_ordem)
    elements.append(Spacer(1, 12))

    # Data de Geração do Relatório
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"Relatório gerado em: {data_atual}", normal_style))
    
    # Construção do PDF
    pdf.build(elements)
    print(f"Relatório gerado: {filename}")

# Exemplo de uso
assistencia_info = {
    'nome': "Assistência Técnica XYZ",
    'cnpj': "12.345.678/0001-99",
    'telefone': "(11) 98765-4321",
    'email': "contato@assistencia.com",
    'endereco': "Rua das Flores, 123, Centro, São Paulo - SP"
}

cliente_info = {
    'nome': "João da Silva",
    'documento': "123.456.789-00",
    'contato': "(11) 91234-5678",
    'email': "joao.silva@email.com",
    'endereco': "Av. Paulista, 1500, São Paulo - SP"
}

ordem_info = {
    'id': 1,
    'criado_em': "2024-11-10T23:13:25.959597",
    'aparelho': "TV",
    'marca': "LG",
    'modelo': "42LN5400",
    'serial': "AZ5646854",
    'defeito': "LED queimado"
}

# Gerar o relatório
gerar_relatorio(assistencia_info, cliente_info, ordem_info)
