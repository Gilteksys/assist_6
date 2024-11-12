import flet as ft
import requests
from urllib.parse import urljoin

class LoginSignupUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Login"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = "#E8EDF5"  # Fundo suave azulado
        self.page.padding = 20
        
        # URL base da API
        self.api_url = "http://127.0.0.1:5000/api/users"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Campos de login com cores melhoradas
        self.txt_username_login = ft.TextField(
            label="Usuário",
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.PERSON,
            cursor_color=ft.colors.BLUE_600,
            focused_border_color=ft.colors.BLUE_600,
            hint_text="Digite seu usuário",
            text_size=16
        )
        
        self.txt_password_login = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.LOCK,
            cursor_color=ft.colors.BLUE_600,
            focused_border_color=ft.colors.BLUE_600,
            hint_text="Digite sua senha",
            text_size=16
        )
        
        # Campos de cadastro com cores melhoradas
        self.txt_username_signup = ft.TextField(
            label="Usuário",
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.PERSON,
            cursor_color=ft.colors.BLUE_600,
            focused_border_color=ft.colors.BLUE_600,
            hint_text="Escolha seu usuário",
            text_size=16
        )
        
        self.txt_email_signup = ft.TextField(
            label="Email",
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.EMAIL,
            cursor_color=ft.colors.BLUE_600,
            focused_border_color=ft.colors.BLUE_600,
            hint_text="Digite seu email",
            text_size=16
        )
        
        self.txt_password_signup = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.LOCK,
            cursor_color=ft.colors.BLUE_600,
            focused_border_color=ft.colors.BLUE_600,
            hint_text="Crie sua senha",
            text_size=16
        )
        
        self.txt_confirm_password = ft.TextField(
            label="Confirmar Senha",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.colors.BLUE_400,
            prefix_icon=ft.icons.LOCK_CLOCK,
            cursor_color=ft.colors.BLUE_600,
            focused_border_color=ft.colors.BLUE_600,
            hint_text="Confirme sua senha",
            text_size=16
        )

        # Gradiente para o fundo dos containers
        gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                "#1a237e",  # Azul escuro
                "#303f9f"   # Azul médio
            ],
        )

        # Containers para login e cadastro com design melhorado
        self.login_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(name=ft.icons.ACCOUNT_CIRCLE_ROUNDED, 
                           size=80, 
                           color=ft.colors.WHITE),
                    ft.Text("Bem-vindo de volta!", 
                           size=28, 
                           weight=ft.FontWeight.BOLD,
                           color=ft.colors.WHITE),
                    ft.Text("Faça login na sua conta", 
                           size=16, 
                           color=ft.colors.WHITE70),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.txt_username_login,
                                self.txt_password_login,
                                ft.Container(height=10),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.LOGIN, color=ft.colors.WHITE),
                                            ft.Text("Entrar", size=16, weight=ft.FontWeight.W_500)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    width=300,
                                    height=45,
                                    on_click=self.login,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor="#4CAF50",  # Verde
                                        animation_duration=500,
                                        shadow_color=ft.colors.BLACK38
                                    )
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        ),
                        padding=30,
                        bgcolor=ft.colors.WHITE,
                        border_radius=8
                    ),
                    ft.TextButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(name=ft.icons.PERSON_ADD, color=ft.colors.WHITE70),
                                ft.Text("Não tem conta? Cadastre-se", color=ft.colors.WHITE70)
                            ]
                        ),
                        on_click=lambda _: self.toggle_view()
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            padding=30,
            gradient=gradient,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK38,
                offset=ft.Offset(0, 5)
            )
        )

        self.signup_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(name=ft.icons.PERSON_ADD_ROUNDED, 
                           size=80, 
                           color=ft.colors.WHITE),
                    ft.Text("Criar Conta", 
                           size=28, 
                           weight=ft.FontWeight.BOLD,
                           color=ft.colors.WHITE),
                    ft.Text("Preencha seus dados para começar", 
                           size=16, 
                           color=ft.colors.WHITE70),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.txt_username_signup,
                                self.txt_email_signup,
                                self.txt_password_signup,
                                self.txt_confirm_password,
                                ft.Container(height=10),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.APP_REGISTRATION, color=ft.colors.WHITE),
                                            ft.Text("Cadastrar", size=16, weight=ft.FontWeight.W_500)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    width=300,
                                    height=45,
                                    on_click=self.signup,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor="#FF7043",  # Laranja
                                        animation_duration=500,
                                        shadow_color=ft.colors.BLACK38
                                    )
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        ),
                        padding=30,
                        bgcolor=ft.colors.WHITE,
                        border_radius=8
                    ),
                    ft.TextButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(name=ft.icons.LOGIN, color=ft.colors.WHITE70),
                                ft.Text("Já tem conta? Faça login", color=ft.colors.WHITE70)
                            ]
                        ),
                        on_click=lambda _: self.toggle_view()
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            padding=30,
            gradient=gradient,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK38,
                offset=ft.Offset(0, 5)
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
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            name=ft.icons.INFO,
                            color=color,
                            size=20
                        ),
                        ft.Text(message, color=color)
                    ],
                    spacing=10
                ),
                bgcolor=ft.colors.WHITE,
                duration=3000
            )
        )

    def login(self, e):
        username = self.txt_username_login.value
        password = self.txt_password_login.value

        if not username or not password:
            self.show_alert("Por favor, preencha todos os campos!")
            return

        try:
            response = requests.post(
                f"{self.api_url}/login",
                json={
                    'username': username,
                    'password': password
                }
            )
            
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
            self.show_alert("Por favor, preencha todos os campos!")
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