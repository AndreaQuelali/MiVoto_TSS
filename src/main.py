"""
Aplicación principal del Predictor Electoral Bolivia 2025
"""
import customtkinter as ctk
import sys
import os

# Agregar el directorio src al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import MainController


def main():
    """Función principal de la aplicación."""
    # Configurar apariencia de CustomTkinter
    ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    root = ctk.CTk()
    app = MainController(root)
    app.ejecutar()


if __name__ == "__main__":
    main() 