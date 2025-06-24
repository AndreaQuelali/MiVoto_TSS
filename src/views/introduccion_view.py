"""
Vista de introducción de la aplicación
"""
import customtkinter as ctk


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
        self.frame = ctk.CTkFrame(self.parent)

        # Contenedor central
        contenedor = ctk.CTkFrame(self.frame)
        contenedor.pack(expand=True, fill="both", padx=40, pady=40)

        # Título principal
        titulo_label = ctk.CTkLabel(
            contenedor, 
            text="MODELO MATEMÁTICO PARA LAS ELECCIONES GENERALES EN BOLIVIA 2025",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("#1a237e", "#bbdefb"),
            wraplength=700,
            justify="center"
        )
        titulo_label.pack(pady=(30, 18))
        
        # Subtítulo
        subtitulo_label = ctk.CTkLabel(
            contenedor, 
            text="Taller de Simulación de Sistemas",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1565c0", "#90caf9")
        )
        subtitulo_label.pack(pady=8)
        
        # Universidad
        universidad_label = ctk.CTkLabel(
            contenedor, 
            text="UNIVERSIDAD MAYOR DE SAN SIMON",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color=("#263238", "#b0bec5")
        )
        universidad_label.pack(pady=(0, 28))

        # Texto de introducción
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
        
        intro_label = ctk.CTkLabel(
            contenedor, 
            text=intro_text,
            font=ctk.CTkFont(size=12),
            text_color=("gray10", "gray90"),
            wraplength=700,
            justify="left"
        )
        intro_label.pack(pady=18, padx=20)
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame 