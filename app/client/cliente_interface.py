import flet as ft
import requests
from urllib.parse import urljoin

class ClienteUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Cadastro de Clientes"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = "#f5f5f5"  # Cor de fundo mais suave
        self.page.padding = 20
        
        # URL base da API
        self.api_url = "http://127.0.0.1:5000/api/clientes"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Cabeçalho com logo/ícone
        header = ft.Row(
            controls=[
                ft.Icon(name=ft.icons.PEOPLE_ALT_ROUNDED, size=40, color=ft.colors.BLUE_600),
                ft.Text("Sistema de Gerenciamento de Clientes", 
                       size=28, 
                       weight=ft.FontWeight.BOLD,
                       color=ft.colors.BLUE_600)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Campos do formulário com layout melhorado
        self.txt_nome = ft.TextField(
            label="Nome do Cliente",
            width=400,
            border_color=ft.colors.BLUE_600,
            prefix_icon=ft.icons.PERSON,
            hint_text="Digite o nome completo"
        )
        
        self.txt_documento = ft.TextField(
            label="CPF/CNPJ",
            width=400,
            border_color=ft.colors.BLUE_600,
            prefix_icon=ft.icons.BADGE,
            hint_text="Digite o documento"
        )
        
        self.txt_contato = ft.TextField(
            label="Telefone",
            width=400,
            border_color=ft.colors.BLUE_600,
            prefix_icon=ft.icons.PHONE,
            hint_text="(00) 00000-0000"
        )
        
        self.txt_endereco = ft.TextField(
            label="Endereço Completo",
            width=400,
            border_color=ft.colors.BLUE_600,
            prefix_icon=ft.icons.LOCATION_ON,
            hint_text="Rua, número, bairro, cidade"
        )
        
        self.txt_email = ft.TextField(
            label="E-mail",
            width=400,
            border_color=ft.colors.BLUE_600,
            prefix_icon=ft.icons.EMAIL,
            hint_text="cliente@email.com"
        )

        # Botões com estilo melhorado
        buttons_row = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Limpar Campos",
                    width=190,
                    on_click=lambda _: self.clear_form(),
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_600,
                        bgcolor=ft.colors.WHITE,
                        side=ft.BorderSide(width=2, color=ft.colors.BLUE_600),
                    )
                ),
                ft.ElevatedButton(
                    text="Cadastrar Cliente",
                    width=190,
                    on_click=self.register_assistencia,
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLUE_600,
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # Container principal com visual renovado
        self.register_container = ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Divider(height=2, color=ft.colors.BLUE_200),
                    self.txt_nome,
                    self.txt_documento,
                    self.txt_contato,                                        
                    self.txt_endereco,
                    self.txt_email,
                    buttons_row
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
            width=500
        )

        # Adiciona o container à página
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

    def register_assistencia(self, e):
        data = {
            'nome': self.txt_nome.value,
            'documento': self.txt_documento.value,
            'contato': self.txt_contato.value,
            'endereco': self.txt_endereco.value,
            'email': self.txt_email.value           
        }

        if not all([data['nome'], data['contato']]):
            self.show_alert("Por favor, preencha pelo menos o nome e contato do cliente!")
            return

        try:
            response = requests.post(
                f"{self.api_url}/register",
                json=data
            )
            
            print("Status Code:", response.status_code)
            print("Response JSON:", response.json())
            
            if response.status_code == 201:
                self.show_alert("Cliente cadastrado com sucesso!", ft.colors.GREEN)
                self.clear_form()
            else:
                error_msg = response.json().get('error','Erro ao cadastrar cliente')
                self.show_alert(error_msg)
        except requests.RequestException as e:
            print(f"Erro de conexão: {str(e)}")
            self.show_alert("Erro de conexão com o servidor")

    def clear_form(self):
        self.txt_nome.value = ""
        self.txt_documento.value = ""
        self.txt_contato.value = ""
        self.txt_email.value = ""
        self.txt_endereco.value = ""        
        self.page.update()

def main(page: ft.Page):
    ClienteUI(page)

if __name__ == '__main__':
    ft.app(target=main)