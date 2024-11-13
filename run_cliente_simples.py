# run_client.py
import flet as ft
from app.client.buscacliente_simples import main

if __name__ == '__main__':
    ft.app(target=main)