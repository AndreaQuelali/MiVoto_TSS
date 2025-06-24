"""
Vista de introducción de la aplicación
"""
import tkinter as tk
from tkinter import ttk


class IntroduccionView:
    """
    Vista para la pestaña de introducción con información general.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.crear_vista()
    
    def crear_vista(self):
        """Crea la vista de introducción."""
        self.frame = ttk.Frame(self.parent, padding="15 15 15 15")

        ttk.Label(self.frame, 
                 text="MODELO MATEMÁTICO PARA LAS ELECCIONES GENERALES EN BOLIVIA 2025", 
                 style='Header.TLabel', wraplength=800, justify='center').pack(pady=(20, 10))
        ttk.Label(self.frame, text="Taller de Simulación de Sistemas", style='Subheader.TLabel').pack(pady=5)
        ttk.Label(self.frame, text="UNIVERSIDAD MAYOR DE SAN SIMON", font=('Arial', 11, 'italic')).pack(pady=(0, 20))

        intro_text = """
        El 17 de agosto de 2025 se llevarán a cabo las elecciones generales de Bolivia para que podamos elegir
        nuestro presidente(a), vicepresidente(a) y representantes ante la Asamblea Legislativa del Estado Plurinacional
        de Bolivia. Siendo que es posible que se dé una segunda vuelta el 19 de octubre de 2025. Como votantes
        bolivianos se elegirán al presidente(a) y vicepresidente(a) de Bolivia, 130 miembros de la Cámara de Diputados
        de Bolivia y 36 integrantes de la Cámara de Senadores de Bolivia para el periodo 2025-2030. La toma de
        posesión de autoridades electas como Presidente y Vicepresidente se realizará el 8 de noviembre de 2025.

        Esta aplicación ofrece un modelo predictivo basado en datos históricos y encuestas actuales para simular
        los posibles resultados de estas elecciones, incluyendo la distribución de escaños mediante el método D'Hondt.
        """
        ttk.Label(self.frame, text=intro_text, wraplength=750, justify='left', font=('Arial', 10)).pack(pady=10)
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame 