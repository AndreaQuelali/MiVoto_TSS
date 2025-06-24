"""
Vista para mostrar los resultados de la predicción
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, Callable

from utils.chart_utils import crear_grafico_votos, crear_grafico_escanos
from config.settings import TOTAL_SENADORES, TOTAL_DIPUTADOS


class ResultadosView:
    """
    Vista para mostrar los resultados de la predicción electoral.
    """
    
    def __init__(self, parent, on_simular_segunda_vuelta: Callable = None):
        self.parent = parent
        self.on_simular_segunda_vuelta = on_simular_segunda_vuelta
        
        # Datos de resultados
        self.prediccion_votos = {}
        self.senadores = {}
        self.diputados = {}
        self.segunda_vuelta = False
        self.candidatos_segunda_vuelta = []
        self.prediccion_ejecutada = False
        
        # Widgets de la interfaz
        self.frame = None
        self.tree_votos = None
        self.canvas_votos = None
        self.tree_senadores = None
        self.canvas_senadores = None
        self.tree_diputados = None
        self.canvas_diputados = None
        self.btn_segunda_vuelta = None
        
        self.crear_vista()
    
    def crear_vista(self):
        """Crea la vista de resultados."""
        self.frame = ctk.CTkFrame(self.parent)
        
        # Contenedor principal centrado
        contenedor = ctk.CTkFrame(self.frame)
        contenedor.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Título
        titulo_label = ctk.CTkLabel(
            contenedor, 
            text="Resultados de la Predicción Electoral 2025",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1a237e", "#bbdefb")
        )
        titulo_label.pack(pady=(10, 24))

        # Scrollable frame para el contenido de resultados
        self.scrollable_frame = ctk.CTkScrollableFrame(contenedor, width=800, height=500)
        self.scrollable_frame.pack(fill='both', expand=True, padx=0, pady=0)

        # Sección de resultados de votos
        self.frame_votos = ctk.CTkFrame(self.scrollable_frame)
        self.frame_votos.pack(fill='x', padx=10, pady=12)
        votos_label = ctk.CTkLabel(
            self.frame_votos,
            text="Predicción de Votos 2025",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#1565c0", "#90caf9")
        )
        votos_label.pack(pady=(12, 8))

        # Sección de resultados de escaños (Senadores)
        self.frame_senadores = ctk.CTkFrame(self.scrollable_frame)
        self.frame_senadores.pack(fill='x', padx=10, pady=12)
        senadores_label = ctk.CTkLabel(
            self.frame_senadores,
            text=f"Distribución de Senadores (Total: {TOTAL_SENADORES})",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#1565c0", "#90caf9")
        )
        senadores_label.pack(pady=(12, 8))

        # Sección de resultados de escaños (Diputados)
        self.frame_diputados = ctk.CTkFrame(self.scrollable_frame)
        self.frame_diputados.pack(fill='x', padx=10, pady=12)
        diputados_label = ctk.CTkLabel(
            self.frame_diputados,
            text=f"Distribución de Diputados (Total: {TOTAL_DIPUTADOS})",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#1565c0", "#90caf9")
        )
        diputados_label.pack(pady=(12, 8))

        # Botón para simular segunda vuelta si aplica
        self.btn_segunda_vuelta = ctk.CTkButton(
            self.scrollable_frame, 
            text="Simular Segunda Vuelta", 
            command=self.simular_segunda_vuelta,
            state='disabled',
            font=ctk.CTkFont(size=13, weight="bold"),
            width=260,
            height=38
        )
        self.btn_segunda_vuelta.pack(pady=18)

        # Botón para refrescar resultados
        actualizar_btn = ctk.CTkButton(
            self.scrollable_frame, 
            text="Actualizar Vista de Resultados", 
            command=self.mostrar_resultados,
            font=ctk.CTkFont(size=13, weight="bold"),
            width=260,
            height=38
        )
        actualizar_btn.pack(pady=10)
    
    def mostrar_resultados(self):
        """Muestra los resultados de la predicción."""
        if not self.prediccion_ejecutada:
            no_results_label = ctk.CTkLabel(
                self.frame_votos, 
                text="Ejecute el modelo en la pestaña 'Configuración del Modelo' para ver los resultados.",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("gray50", "gray50")
            )
            no_results_label.pack(pady=50)
            return

        # Actualizar estado del botón de segunda vuelta
        if self.segunda_vuelta:
            self.btn_segunda_vuelta.configure(state='normal')
        else:
            self.btn_segunda_vuelta.configure(state='disabled')

        # Limpiar widgets existentes
        self._limpiar_widgets()

        self._crear_tabla_votos()
        self._crear_grafico_votos()
        self._crear_tabla_escanos(self.frame_senadores, self.senadores)
        self._crear_grafico_escanos(self.frame_senadores, self.senadores, "Senadores")
        self._crear_tabla_escanos(self.frame_diputados, self.diputados)
        self._crear_grafico_escanos(self.frame_diputados, self.diputados, "Diputados")
    
    def _limpiar_widgets(self):
        """Limpia los widgets existentes."""
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        for widget in [self.tree_votos, self.canvas_votos,
                      self.tree_senadores, self.canvas_senadores,
                      self.tree_diputados, self.canvas_diputados]:
            if widget:
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()
                else:
                    widget.destroy()
        plt.close('all')
    
    def _crear_tabla_votos(self):
        """Crea la tabla para mostrar la predicción de votos."""
        if not self.prediccion_votos:
            no_data_label = ctk.CTkLabel(
                self.frame_votos, 
                text="No hay predicción de votos disponible.",
                text_color=("gray50", "gray50")
            )
            no_data_label.pack(pady=5)
            return

        # Crear tabla usando CTkTextbox para simular una tabla
        self.tree_votos = ctk.CTkTextbox(self.frame_votos, height=150, fg_color="#f5f5f5")
        self.tree_votos.pack(fill='both', expand=True, padx=10, pady=5)

        # Crear encabezados
        header = "Partido".ljust(20) + "Porcentaje de Votos (%)".ljust(25)
        self.tree_votos.configure(font=("Consolas", 13, "bold"))
        self.tree_votos.insert("1.0", header + "\n")
        self.tree_votos.insert("end", "=" * len(header) + "\n")

        # Insertar datos ordenados
        sorted_votos = sorted(self.prediccion_votos.items(), key=lambda item: item[1], reverse=True)
        for idx, (party, percentage) in enumerate(sorted_votos):
            row = f"{party}".ljust(20) + f"{percentage:.2f}%".ljust(25)
            self.tree_votos.insert("end", row + "\n")
            if idx == 0:
                self.tree_votos.insert("end", "-" * len(header) + "\n")

        self.tree_votos.configure(state="disabled")
    
    def _crear_grafico_votos(self):
        """Crea el gráfico de barras para la predicción de votos."""
        self.canvas_votos = crear_grafico_votos(self.prediccion_votos, self.frame_votos)
    
    def _crear_tabla_escanos(self, parent_frame, escanos_data):
        """Crea una tabla para mostrar la distribución de escaños."""
        if not escanos_data:
            no_data_label = ctk.CTkLabel(
                parent_frame, 
                text="No se asignaron escaños para esta categoría.",
                text_color=("gray50", "gray50")
            )
            no_data_label.pack(pady=5)
            return

        # Crear tabla usando CTkTextbox para simular una tabla
        tree_escanos = ctk.CTkTextbox(parent_frame, height=120, fg_color="#f5f5f5")
        tree_escanos.pack(fill='both', expand=True, padx=10, pady=5)
        tree_escanos.configure(font=("Consolas", 13, "bold"))

        # Crear encabezados
        header = "Partido".ljust(20) + "Escaños".ljust(10)
        tree_escanos.insert("1.0", header + "\n")
        tree_escanos.insert("end", "=" * len(header) + "\n")

        # Insertar datos ordenados
        sorted_escanos = sorted(escanos_data.items(), key=lambda item: item[1], reverse=True)
        for idx, (party, seats) in enumerate(sorted_escanos):
            row = f"{party}".ljust(20) + f"{seats}".ljust(10)
            tree_escanos.insert("end", row + "\n")
            if idx == 0:
                tree_escanos.insert("end", "-" * len(header) + "\n")

        tree_escanos.configure(state="disabled")
        
        # Guardar referencia según el tipo
        if parent_frame == self.frame_senadores:
            self.tree_senadores = tree_escanos
        else:
            self.tree_diputados = tree_escanos
    
    def _crear_grafico_escanos(self, parent_frame, escanos_data, title_suffix):
        """Crea el gráfico de barras para la distribución de escaños."""
        canvas_escanos = crear_grafico_escanos(escanos_data, parent_frame, title_suffix)
        
        # Guardar referencia según el tipo
        if parent_frame == self.frame_senadores:
            self.canvas_senadores = canvas_escanos
        else:
            self.canvas_diputados = canvas_escanos
    
    def simular_segunda_vuelta(self):
        """Simula la segunda vuelta electoral."""
        if self.on_simular_segunda_vuelta:
            self.on_simular_segunda_vuelta()
    
    def actualizar_resultados(self, prediccion_votos: Dict, senadores: Dict, diputados: Dict,
                            segunda_vuelta: bool, candidatos_segunda_vuelta: list):
        """Actualiza los resultados mostrados en la vista."""
        self.prediccion_votos = prediccion_votos
        self.senadores = senadores
        self.diputados = diputados
        self.segunda_vuelta = segunda_vuelta
        self.candidatos_segunda_vuelta = candidatos_segunda_vuelta
        self.prediccion_ejecutada = True
        self.mostrar_resultados()
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame 