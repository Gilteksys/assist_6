# run_client.py
import flet as ft
from app.client.ordem_interface import main

if __name__ == '__main__':
    ft.app(target=main)