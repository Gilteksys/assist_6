import flet as ft
import requests
from datetime import datetime

class OrdemServicoUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ordem de Serviço"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = "#f0f4f8"
        self.page.padding = 20
        self.page.scroll = "auto"
        
        self.api_url = "http://127.0.0.1:5000/api/ordens"
        
        self.setup_ui()
    
    def setup_ui(self):
        # Cabeçalho
        header = ft.Row(
            controls=[
                ft.Icon(name=ft.icons.BUILD_CIRCLE, size=40, color=ft.colors.BLUE_800),
                ft.Text("Ordem de Serviço", 
                       size=28, 
                       weight=ft.FontWeight.BOLD,
                       color=ft.colors.BLUE_800)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Seção de Informações do Cliente
        self.txt_cliente_id = ft.TextField(
            label="ID do Cliente",
            width=200,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.PERSON_PIN,
            hint_text="Digite o ID do cliente"
        )

        # Seção de Informações do Aparelho
        self.txt_aparelho = ft.TextField(
            label="Aparelho *",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.DEVICES,
            hint_text="Digite o tipo de aparelho"
        )
        
        self.txt_marca = ft.TextField(
            label="Marca",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.BLENDER_SHARP,
            hint_text="Digite a marca"
        )
        
        self.txt_modelo = ft.TextField(
            label="Modelo",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.MODEL_TRAINING,
            hint_text="Digite o modelo"
        )
        
        self.txt_serial = ft.TextField(
            label="Número de Série",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.NUMBERS,
            hint_text="Digite o número de série"
        )

        # Seção de Serviço
        self.txt_defeito = ft.TextField(
            label="Defeito Relatado",
            width=400,
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.WARNING,
            hint_text="Descreva o defeito relatado"
        )
        
        self.txt_pecas = ft.TextField(
            label="Peças Utilizadas",
            width=400,
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.SETTINGS,
            hint_text="Liste as peças utilizadas"
        )
        
        self.txt_valor = ft.TextField(
            label="Valor do Conserto (R$)",
            width=200,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.ATTACH_MONEY,
            hint_text="0.00"
        )
        
        self.txt_garantia = ft.TextField(
            label="Garantia *",
            width=400,
            multiline=True,
            min_lines=2,
            max_lines=3,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.VERIFIED,
            hint_text="Descreva os termos da garantia"
        )

        # Botões
        buttons_row = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Limpar",
                    width=180,
                    on_click=lambda _: self.clear_form(),
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_800,
                        bgcolor=ft.colors.WHITE,
                        side=ft.BorderSide(width=2, color=ft.colors.BLUE_800),
                    )
                ),
                ft.ElevatedButton(
                    text="Gerar Ordem de Serviço",
                    width=180,
                    on_click=self.register_ordem,
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLUE_800,
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # Container Principal
        self.register_container = ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Divider(height=2, color=ft.colors.BLUE_200),
                    ft.Text("Informações do Cliente", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                    self.txt_cliente_id,
                    ft.Text("Informações do Aparelho", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                    self.txt_aparelho,
                    ft.Row([self.txt_marca, self.txt_modelo], spacing=20),
                    self.txt_serial,
                    ft.Text("Detalhes do Serviço", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                    self.txt_defeito,
                    self.txt_pecas,
                    ft.Row([self.txt_valor], alignment=ft.MainAxisAlignment.START),
                    self.txt_garantia,
                    buttons_row,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=30,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_200,
                offset=ft.Offset(0, 2)
            ),
            width=850
        )

        self.page.add(
            ft.Container(
                content=self.register_container,
                alignment=ft.alignment.center
            )
        )

    def show_alert(self, message, color=ft.colors.RED):
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message, color=color),
                duration=3000
            )
        )

    def register_ordem(self, e):
        try:
            valor = float(self.txt_valor.value) if self.txt_valor.value else None
        except ValueError:
            self.show_alert("Valor do conserto deve ser um número válido")
            return

        data = {
            'cliente_id': int(self.txt_cliente_id.value) if self.txt_cliente_id.value else None,
            'aparelho': self.txt_aparelho.value,
            'marca': self.txt_marca.value,
            'modelo': self.txt_modelo.value,
            'serial': self.txt_serial.value,
            'defeito': self.txt_defeito.value,
            'pecas_utilizadas': self.txt_pecas.value,
            'valor_conserto': valor,
            'garantia': self.txt_garantia.value
        }

        # Validação dos campos obrigatórios
        if not all([data['aparelho'], data['garantia'], data['cliente_id']]):
            self.show_alert("Preencha todos os campos obrigatórios (Aparelho, Garantia e ID do Cliente)!")
            return

        try:
            response = requests.post(
                f"{self.api_url}/register",
                json=data
            )
            
            if response.status_code == 201:
                self.show_alert("Ordem de Serviço registrada com sucesso!", ft.colors.GREEN)
                self.clear_form()
            else:
                error_msg = response.json().get('error', 'Erro ao registrar Ordem de Serviço')
                self.show_alert(error_msg)
        except requests.RequestException as e:
            print(f"Erro de conexão: {str(e)}")
            self.show_alert("Erro de conexão com o servidor")

    def clear_form(self):
        for field in [self.txt_cliente_id, self.txt_aparelho, self.txt_marca, 
                     self.txt_modelo, self.txt_serial, self.txt_defeito, 
                     self.txt_pecas, self.txt_valor, self.txt_garantia]:
            field.value = ""
        self.page.update()

def main(page: ft.Page):
    OrdemServicoUI(page)

if __name__ == '__main__':
    ft.app(target=main)