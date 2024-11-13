import flet as ft
import requests
from urllib.parse import urljoin

class BuscaClienteUI:
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
        self.nome_field = ft.TextField(
            label="Nome",
            width=300,
            border_color=ft.colors.BLUE_400
        )
        
        self.contato_field = ft.TextField(
            label="Contato",
            width=300,
            border_color=ft.colors.BLUE_400
        )
        
        self.email_field = ft.TextField(
            label="Email",
            width=300,
            border_color=ft.colors.BLUE_400
        )
        
        self.documento_field = ft.TextField(
            label="Documento",
            width=300,
            border_color=ft.colors.BLUE_400
        )

        # Tabela de clientes
        self.clients_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Contato")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Documento")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            border=ft.border.all(2, ft.colors.BLUE_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, ft.colors.BLUE_200),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.BLUE_200),
        )

        # Campo de busca
        self.search_field = ft.TextField(
            label="Buscar cliente",
            width=300,
            prefix_icon=ft.icons.SEARCH,
            border_color=ft.colors.BLUE_400,
            on_change=self.filter_clientes
        )

        # Botões
        save_button = ft.ElevatedButton(
            text="Salvar",
            icon=ft.icons.SAVE,
            on_click=self.save_cliente,
            bgcolor=ft.colors.BLUE_400
        )

        clear_button = ft.ElevatedButton(
            text="Limpar",
            icon=ft.icons.CLEAR,
            on_click=self.clear_form,
            bgcolor=ft.colors.GREY_400
        )

        refresh_button = ft.ElevatedButton(
            text="Atualizar",
            icon=ft.icons.REFRESH,
            on_click=self.load_clientes,
            bgcolor=ft.colors.GREEN_400
        )

        # Layout
        form_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Cadastro de Cliente", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
                    self.nome_field,
                    self.contato_field,
                    self.email_field,
                    self.documento_field,
                    ft.Row([save_button, clear_button], alignment=ft.MainAxisAlignment.CENTER)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            border=ft.border.all(2, ft.colors.BLUE_400),
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )

        list_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Lista de Clientes", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
                    ft.Row([self.search_field, refresh_button], alignment=ft.MainAxisAlignment.CENTER),
                    self.clients_table
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            border=ft.border.all(2, ft.colors.BLUE_400),
            border_radius=10
        )

        # Adiciona os containers à página
        self.page.add(form_container, list_container)
        
        # Carrega a lista inicial de clientes
        self.load_clientes(None)

    def load_clientes(self, _):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                clientes = response.json()
                
                # Limpa a tabela
                self.clients_table.rows.clear()
                
                # Adiciona os clientes à tabela
                for cliente in clientes:
                    self.add_cliente_to_table(cliente)
                
                self.page.update()
            else:
                self.show_error_dialog("Erro ao carregar clientes")
        except Exception as e:
            self.show_error_dialog(f"Erro de conexão: {str(e)}")

    def add_cliente_to_table(self, cliente):
        edit_button = ft.IconButton(
            icon=ft.icons.EDIT,
            icon_color=ft.colors.BLUE_400,
            tooltip="Editar",
            on_click=lambda e: self.edit_cliente(e, cliente)
        )
        
        delete_button = ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color=ft.colors.RED_400,
            tooltip="Excluir",
            on_click=lambda e: self.delete_cliente(e, cliente['id'])
        )

        self.clients_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente['id']))),
                    ft.DataCell(ft.Text(cliente['nome'])),
                    ft.DataCell(ft.Text(cliente['contato'])),
                    ft.DataCell(ft.Text(cliente.get('email', ''))),
                    ft.DataCell(ft.Text(cliente.get('documento', ''))),
                    ft.DataCell(ft.Row([edit_button, delete_button])),
                ]
            )
        )

    def save_cliente(self, e):
        try:
            data = {
                "nome": self.nome_field.value,
                "contato": self.contato_field.value,
                "email": self.email_field.value,
                "documento": self.documento_field.value
            }
            
            response = requests.post(self.api_url, json=data)
            if response.status_code == 201:
                self.clear_form(None)
                self.load_clientes(None)
                self.show_snack_bar("Cliente salvo com sucesso!")
            else:
                self.show_error_dialog("Erro ao salvar cliente")
        except Exception as e:
            self.show_error_dialog(f"Erro de conexão: {str(e)}")

    def edit_cliente(self, e, cliente):
        # Preenche o formulário com os dados do cliente
        self.nome_field.value = cliente['nome']
        self.contato_field.value = cliente['contato']
        self.email_field.value = cliente.get('email', '')
        self.documento_field.value = cliente.get('documento', '')
        self.page.update()

    def delete_cliente(self, e, cliente_id):
        def confirm_delete(e):
            try:
                response = requests.delete(urljoin(self.api_url, str(cliente_id)))
                if response.status_code == 200:
                    self.load_clientes(None)
                    self.show_snack_bar("Cliente excluído com sucesso!")
                else:
                    self.show_error_dialog("Erro ao excluir cliente")
            except Exception as ex:
                self.show_error_dialog(f"Erro de conexão: {str(ex)}")
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text("Tem certeza que deseja excluir este cliente?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Excluir", on_click=confirm_delete),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def filter_clientes(self, e):
        search_term = self.search_field.value.lower()
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                clientes = response.json()
                
                # Limpa a tabela
                self.clients_table.rows.clear()
                
                # Filtra e adiciona os clientes
                for cliente in clientes:
                    if search_term in cliente['nome'].lower():
                        self.add_cliente_to_table(cliente)
                
                self.page.update()
        except Exception as e:
            self.show_error_dialog(f"Erro de conexão: {str(e)}")

    def clear_form(self, _):
        self.nome_field.value = ""
        self.contato_field.value = ""
        self.email_field.value = ""
        self.documento_field.value = ""
        self.page.update()

    def show_error_dialog(self, message):
        dialog = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: setattr(dialog, 'open', False)),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_snack_bar(self, message):
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message),
                action="OK",
            )
        )

def main(page: ft.Page):
    BuscaClienteUI(page)

if __name__ == "__main__":
    ft.app(target=main)