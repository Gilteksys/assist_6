import flet as ft
import requests
from urllib.parse import urljoin

class AssistenciaTecnicaUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Cadastro de Assistência Técnica"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = ft.colors.WHITE
        self.page.padding = 20
        
        # URL base da API
        self.api_url = "http://127.0.0.1:5000/api/assistencias"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Campos do formulário
        self.txt_razao_social = ft.TextField(
            label="Razão Social",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.BUSINESS
        )
        
        self.txt_nome_fantasia = ft.TextField(
            label="Nome Fantasia",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.STORE
        )
        
        self.txt_cnpj = ft.TextField(
            label="CNPJ",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.NUMBERS
        )
        
        self.txt_telefone = ft.TextField(
            label="Telefone",
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
        
        self.txt_endereco = ft.TextField(
            label="Endereço",
            width=400,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.LOCATION_ON,
            multiline=True,
        )

        # Container principal
        self.register_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Cadastro de Assistência Técnica", 
                           size=24, 
                           weight=ft.FontWeight.BOLD),
                    self.txt_razao_social,
                    self.txt_nome_fantasia,
                    self.txt_cnpj,
                    self.txt_telefone,
                    self.txt_email,
                    self.txt_endereco,
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
            'razao_social': self.txt_razao_social.value,
            'nome_fantasia': self.txt_nome_fantasia.value,
            'cnpj': self.txt_cnpj.value,
            'telefone': self.txt_telefone.value,
            'email': self.txt_email.value,
            'endereco': self.txt_endereco.value
        }

        # Validação dos campos obrigatórios
        if not all([data['razao_social'], data['nome_fantasia'], 
                   data['cnpj'], data['telefone']]):
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
                self.show_alert("Assistência técnica cadastrada com sucesso!", 
                              ft.colors.GREEN)
                # Limpa o formulário após cadastro bem-sucedido
                self.clear_form()
            else:
                error_msg = response.json().get('error','Erro ao cadastrar assistência técnica')
                self.show_alert(error_msg)
        except requests.RequestException as e:
            print(f"Erro de conexão: {str(e)}")
            self.show_alert("Erro de conexão com o servidor")

    def clear_form(self):
        self.txt_razao_social.value = ""
        self.txt_nome_fantasia.value = ""
        self.txt_cnpj.value = ""
        self.txt_telefone.value = ""
        self.txt_email.value = ""
        self.txt_endereco.value = ""
        self.page.update()

def main(page: ft.Page):
    AssistenciaTecnicaUI(page)

if __name__ == '__main__':
    ft.app(target=main)