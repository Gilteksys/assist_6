# app/client/login_interface.py
import flet as ft
import requests
from urllib.parse import urljoin

class LoginSignupUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Login"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = ft.colors.WHITE
        self.page.padding = 20
        
        # URL base da API
        self.api_url = "http://127.0.0.1:5000/api/users"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Campos de login
        self.txt_username_login = ft.TextField(
            label="Usuário",
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.PERSON
        )
        
        self.txt_password_login = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.LOCK
        )
        
        # Campos de cadastro
        self.txt_username_signup = ft.TextField(
            label="Usuário",
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.PERSON
        )
        
        self.txt_email_signup = ft.TextField(
            label="Email",
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.EMAIL
        )
        
        self.txt_password_signup = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.LOCK
        )
        
        self.txt_confirm_password = ft.TextField(
            label="Confirmar Senha",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.LOCK_CLOCK
        )

        # Containers para login e cadastro
        self.login_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
                    self.txt_username_login,
                    self.txt_password_login,
                    ft.ElevatedButton(
                        text="Entrar",
                        width=300,
                        on_click=self.login,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_400,
                        )
                    ),
                    ft.TextButton(
                        text="Não tem conta? Cadastre-se",
                        on_click=lambda _: self.toggle_view()
                    )
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

        self.signup_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Cadastro", size=24, weight=ft.FontWeight.BOLD),
                    self.txt_username_signup,
                    self.txt_email_signup,
                    self.txt_password_signup,
                    self.txt_confirm_password,
                    ft.ElevatedButton(
                        text="Cadastrar",
                        width=300,
                        on_click=self.signup,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_400,
                        )
                    ),
                    ft.TextButton(
                        text="Já tem conta? Faça login",
                        on_click=lambda _: self.toggle_view()
                    )
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
            ),
            visible=False
        )

        # Adiciona os containers à página
        self.page.add(
            ft.Container(
                content=ft.Stack([self.login_container, self.signup_container]),
                alignment=ft.alignment.center
            )
        )

    def toggle_view(self):
        self.login_container.visible = not self.login_container.visible
        self.signup_container.visible = not self.signup_container.visible
        self.page.update()

    def show_alert(self, message, color=ft.colors.RED):
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message, color=color),
                duration=3000
            )
        )

    def login(self, e):
        username = self.txt_username_login.value
        password = self.txt_password_login.value

        if not username or not password:
            self.show_alert("Preencha todos os campos!")
            return

        try:
            response = requests.post(
                f"{self.api_url}/login",
                json={
                    'username': username,
                    'password': password
                }
            )
            
            # Exibe o status e conteúdo da resposta para depuração
            print("Status Code:", response.status_code)
            print("Response JSON:", response.json())
            
            if response.status_code == 200:
                data = response.json()
                self.show_alert("Login realizado com sucesso!", ft.colors.GREEN)
                print("Token de acesso:", data.get('access_token'))
            else:
                error_msg = response.json().get('error', 'Erro ao fazer login')
                self.show_alert(error_msg)
        except requests.RequestException as e:
            print(f"Erro de conexão: {str(e)}")
            self.show_alert("Erro de conexão com o servidor")


    def signup(self, e):
        username = self.txt_username_signup.value
        email = self.txt_email_signup.value
        password = self.txt_password_signup.value
        confirm_password = self.txt_confirm_password.value

        if not all([username, email, password, confirm_password]):
            self.show_alert("Preencha todos os campos!")
            return

        if password != confirm_password:
            self.show_alert("As senhas não coincidem!")
            return

        try:
            response = requests.post(
                f"{self.api_url}/register",
                json={
                    'username': username,
                    'email': email,
                    'password': password
                }
            )

            if response.status_code == 201:
                self.show_alert("Cadastro realizado com sucesso!", ft.colors.GREEN)
                self.toggle_view()
            else:
                error_msg = response.json().get('error', 'Erro ao criar usuário')
                self.show_alert(error_msg)
        except requests.RequestException as e:
            print(f"Erro de conexão: {str(e)}")
            self.show_alert("Erro de conexão com o servidor")

def main(page: ft.Page):
    LoginSignupUI(page)

if __name__ == '__main__':
    ft.app(target=main)
