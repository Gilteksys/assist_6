import flet as ft
import requests

class AssistenciaTecnicaUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Gestão de Assistências Técnicas"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
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
        
        self.dd_status = ft.Dropdown(
            label="Status",
            width=400,
            options=[
                ft.dropdown.Option("Ativa"),
                ft.dropdown.Option("Inativa"),
                ft.dropdown.Option("Em análise"),
                ft.dropdown.Option("Suspensa")
            ],
            border_color=ft.colors.BLUE_400,
            value="Ativa"
        )

        # DataTable para listar as assistências
        self.data_table = ft.DataTable(
            width=1200,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            columns=[
                ft.DataColumn(ft.Text("Razão Social")),
                ft.DataColumn(ft.Text("Nome Fantasia")),
                ft.DataColumn(ft.Text("CNPJ")),
                ft.DataColumn(ft.Text("Telefone")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[]
        )

        # Containers principais
        self.form_container = ft.Container(
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
                    self.dd_status,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Cadastrar",
                                style=ft.ButtonStyle(
                                    color=ft.colors.WHITE,
                                    bgcolor=ft.colors.BLUE_400,
                                ),
                                on_click=self.save_assistencia
                            ),
                            ft.ElevatedButton(
                                text="Limpar",
                                style=ft.ButtonStyle(
                                    color=ft.colors.WHITE,
                                    bgcolor=ft.colors.GREY_400,
                                ),
                                on_click=self.clear_form
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
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

        self.list_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Assistências Técnicas Cadastradas", 
                                   size=20, 
                                   weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.REFRESH,
                                on_click=self.load_assistencias
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    self.data_table
                ],
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

        # Adiciona os containers à página
        self.page.add(
            ft.Column(
                controls=[
                    self.form_container,
                    self.list_container
                ],
                spacing=30
            )
        )
        
        # Carrega dados iniciais
        self.load_assistencias()

    def show_alert(self, message, color=ft.colors.RED):
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message, color=color),
                duration=3000
            )
        )

    def clear_form(self, e=None):
        self.txt_razao_social.value = ""
        self.txt_nome_fantasia.value = ""
        self.txt_cnpj.value = ""
        self.txt_telefone.value = ""
        self.txt_email.value = ""
        self.txt_endereco.value = ""
        self.dd_status.value = "Ativa"
        self.page.update()

    def load_assistencias(self, e=None):
        try:
            response = requests.get(f"{self.api_url}")
            if response.status_code == 200:
                assistencias = response.json()
                self.data_table.rows.clear()
                
                for assist in assistencias:
                    self.data_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(assist['razao_social'])),
                                ft.DataCell(ft.Text(assist['nome_fantasia'])),
                                ft.DataCell(ft.Text(assist['cnpj'])),
                                ft.DataCell(ft.Text(assist['telefone'])),
                                ft.DataCell(ft.Text(assist['status'])),
                                ft.DataCell(
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.icons.EDIT,
                                                on_click=lambda e, id=assist['id']: 
                                                    self.edit_assistencia(id)
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.DELETE,
                                                on_click=lambda e, id=assist['id']: 
                                                    self.delete_assistencia(id)
                                            ),
                                        ]
                                    )
                                ),
                            ]
                        )
                    )
                self.page.update()
        except requests.RequestException as e:
            self.show_alert(f"Erro ao carregar dados: {str(e)}")

    def save_assistencia(self, e):
        data = {
            'razao_social': self.txt_razao_social.value,
            'nome_fantasia': self.txt_nome_fantasia.value,
            'cnpj': self.txt_cnpj.value,
            'telefone': self.txt_telefone.value,
            'email': self.txt_email.value,
            'endereco': self.txt_endereco.value,
            'status': self.dd_status.value
        }

        if not all([data['razao_social'], data['nome_fantasia'], 
                   data['cnpj'], data['telefone']]):
            self.show_alert("Preencha todos os campos obrigatórios!")
            return

        try:
            response = requests.post(
                f"{self.api_url}",
                json=data
            )
            
            if response.status_code in [200, 201]:
                self.show_alert("Assistência técnica salva com sucesso!", 
                              ft.colors.GREEN)
                self.clear_form()
                self.load_assistencias()
            else:
                error_msg = response.json().get('error', 
                                              'Erro ao salvar assistência técnica')
                self.show_alert(error_msg)
        except requests.RequestException as e:
            self.show_alert(f"Erro de conexão: {str(e)}")

    def edit_assistencia(self, id):
        try:
            response = requests.get(f"{self.api_url}/{id}")
            if response.status_code == 200:
                data = response.json()
                self.txt_razao_social.value = data['razao_social']
                self.txt_nome_fantasia.value = data['nome_fantasia']
                self.txt_cnpj.value = data['cnpj']
                self.txt_telefone.value = data['telefone']
                self.txt_email.value = data['email']
                self.txt_endereco.value = data['endereco']
                self.dd_status.value = data['status']
                self.page.update()
        except requests.RequestException as e:
            self.show_alert(f"Erro ao carregar dados: {str(e)}")

    def delete_assistencia(self, id):
        try:
            response = requests.delete(f"{self.api_url}/{id}")
            if response.status_code == 200:
                self.show_alert("Assistência técnica excluída com sucesso!", 
                              ft.colors.GREEN)
                self.load_assistencias()
            else:
                self.show_alert("Erro ao excluir assistência técnica")
        except requests.RequestException as e:
            self.show_alert(f"Erro de conexão: {str(e)}")

def main(page: ft.Page):
    AssistenciaTecnicaUI(page)

if __name__ == '__main__':
    ft.app(target=main)