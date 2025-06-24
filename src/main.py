"""
Aplicación principal del Predictor Electoral Bolivia 2025
"""
import tkinter as tk
import sys
import os

# Agregar el directorio src al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import MainController


def main():
    """Función principal de la aplicación."""
    root = tk.Tk()
    app = MainController(root)
    app.ejecutar()


if __name__ == "__main__":
    main() 