import flet as ft
import requests
from urllib.parse import urljoin

class BuscaClienteUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Cadastro de Cliente"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = ft.colors.with_opacity
        self.page.padding = 20
        
        # URL base da API
        self.api_url = "http://127.0.0.1:5000/api/clientes"
        
        # Cliente selecionado atualmente
        self.current_selected = None
        
        self.setup_ui()

    def setup_ui(self):
        # Campos do formulário
        self.nome_field = ft.TextField(
            color="WHITE",
            label="Nome",
            width=500,
            border_color=ft.colors.BLUE_400
        )
        
        self.contato_field = ft.TextField(
            color="WHITE",
            label="Contato",
            width=500,
            border_color=ft.colors.BLUE_400
        )
        
        self.email_field = ft.TextField(
            color="WHITE",
            label="Email",
            width=500,
            border_color=ft.colors.BLUE_400
        )
        
        self.documento_field = ft.TextField(
            color="WHITE",
            label="Documento",
            width=500,
            border_color=ft.colors.BLUE_400
        )

        # Tabela de clientes melhorada
        self.clients_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID"), numeric=True),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Contato")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Documento")),
                ft.DataColumn(ft.Text("Ações")),
            ],            
            border=ft.border.all(2, ft.colors.BLUE_400),
            border_radius=5,
            vertical_lines=ft.border.BorderSide(3, ft.colors.BLUE_200),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.BLUE_200),
            heading_row_color=ft.colors.BLUE_700,
            heading_row_height=70,
            data_row_color={"hovered": ft.colors.BLUE_50},
            column_spacing=10,
            divider_thickness=0,
            width=1000,
            height=400,
        )

        # Campo de busca
        self.search_field = ft.TextField(
            color="WHITE",
            label="Buscar cliente",
            width=400,
            prefix_icon=ft.icons.SEARCH,
            border_color=ft.colors.BLUE_400,
            on_change=self.filter_clientes
        )

        # Botões
        save_button = ft.ElevatedButton(
            text="Salvar",
            icon=ft.icons.SAVE,
            on_click=self.save_cliente,
            bgcolor=ft.colors.GREEN_500,
            color=ft.colors.WHITE,
            width=150
        )

        clear_button = ft.ElevatedButton(
            text="Limpar",
            icon=ft.icons.CLEAR,
            on_click=self.clear_form,
            bgcolor=ft.colors.GREY_400,
            color=ft.colors.WHITE,
            width=150
        )

        refresh_button = ft.ElevatedButton(
            text="Atualizar",
            icon=ft.icons.REFRESH,
            on_click=self.load_clientes,
            bgcolor=ft.colors.YELLOW_500,
            color=ft.colors.WHITE,
            width=150
        )

        # Layout
        form_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Cadastro de Cliente", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
                    self.nome_field,
                    self.contato_field,
                    self.email_field,
                    self.documento_field,
                    ft.Row(
                        [save_button, clear_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
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
                    ft.Row(
                        [self.search_field, refresh_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    self.clients_table
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
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
            response = requests.get(self.api_url, timeout=5)
            if response.status_code == 200:
                clientes = response.json()
                
                # Limpa a tabela
                self.clients_table.rows.clear()
                
                # Adiciona os clientes à tabela
                for cliente in clientes:
                    self.add_cliente_to_table(cliente)
                
                self.page.update()
            else:
                self.show_error_dialog(f"Erro ao carregar clientes: {response.status_code}")
        except Exception as e:
            self.show_error_dialog(f"Erro de conexão: {str(e)}")

    def add_cliente_to_table(self, cliente):
        edit_button = ft.IconButton(
            icon=ft.icons.EDIT,
            icon_color=ft.colors.BLUE_400,
            tooltip="Editar",
            data=cliente,
            on_click=lambda e: self.edit_cliente(e, cliente)
        )
        
        delete_button = ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color=ft.colors.RED_400,
            tooltip="Excluir",
            data=cliente['id'],
            on_click=lambda e: self.delete_cliente(e, cliente['id'])
        )

        self.clients_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente['id']), text_align="center")),
                    ft.DataCell(ft.Text(cliente['nome'])),
                    ft.DataCell(ft.Text(cliente['contato'])),
                    ft.DataCell(ft.Text(cliente.get('email', ''))),
                    ft.DataCell(ft.Text(cliente.get('documento', ''))),
                    ft.DataCell(ft.Row(
                        [edit_button, delete_button],
                        alignment=ft.MainAxisAlignment.CENTER
                    )),
                ],
                color=ft.colors.WHITE,
                on_select_changed=lambda e: self.row_selected(e, cliente)
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
            
            response = requests.post(urljoin(self.api_url, 'register'), json=data)
            if response.status_code == 201:
                self.clear_form(None)
                self.load_clientes(None)
                self.show_snack_bar("Cliente salvo com sucesso!")
            else:
                self.show_error_dialog("Erro ao salvar cliente")
        except Exception as e:
            self.show_error_dialog(f"Erro de conexão: {str(e)}")

    def edit_cliente(self, e, cliente):
        self.nome_field.value = cliente['nome']
        self.contato_field.value = cliente['contato']
        self.email_field.value = cliente.get('email', '')
        self.documento_field.value = cliente.get('documento', '')
        self.current_selected = cliente
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
                
                self.clients_table.rows.clear()
                
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
        self.current_selected = None
        self.page.update()

    def row_selected(self, e, cliente):
        if e.data == 'true':
            self.current_selected = cliente
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