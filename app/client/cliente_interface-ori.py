import flet as ft
import requests
from urllib.parse import urljoin

class ClienteUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Cadastro de Cliente"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = ft.colors.WHITE
        self.page.padding = 20
        
        # URL base da API
        self.api_url = "http://127.0.0.1:5000/api/clientes"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Campos do formulário
        self.txt_nome = ft.TextField(
            label="Nome",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.BUSINESS
        )
        
        self.txt_documento = ft.TextField(
            label="Documento",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.STORE
        )
        
        self.txt_contato = ft.TextField(
            label="Contato",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.NUMBERS
        )
        
        self.txt_endereco = ft.TextField(
            label="Endereço",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.PHONE
        )
        
        self.txt_email = ft.TextField(
            label="Email",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.EMAIL
        )        


        # Container principal
        self.register_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Cadastro de Clinte", 
                           size=24, 
                           weight=ft.FontWeight.BOLD),
                    self.txt_nome,
                    self.txt_documento,
                    self.txt_contato,                                        
                    self.txt_endereco,
                    self.txt_email,
                    ft.ElevatedButton(
                        text="Cadastrar",
                        width=400,
                        on_click=self.register_assistencia,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_400,
                        )
                    ),
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
                color=ft.colors.BLUE_GREY_100,
            )
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

        # Validação dos campos obrigatórios
        if not all([data['nome'], data['contato']]):
            self.show_alert("Preencha todos os campos obrigatórios!")
            return

        try:
            response = requests.post(
                f"{self.api_url}/register",
                json=data
            )
            
            # Exibe o status e conteúdo da resposta para depuração
            print("Status Code:", response.status_code)
            print("Response JSON:", response.json())
            
            if response.status_code == 201:
                self.show_alert("Cliente cadastrado com sucesso!", ft.colors.GREEN)
                # Limpa o formulário após cadastro bem-sucedido
                self.clear_form()
            else:
                error_msg = response.json().get('error','Erro ao cadastrar Cliente')
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