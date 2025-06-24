"""
Vista para mostrar los resultados de la predicción
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Callable

from utils.style_utils import crear_scrollable_frame
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
        self.frame = ttk.Frame(self.parent, padding="10")
        
        # Crear frame con scrollbar
        canvas, scrollbar, scrollable_frame = crear_scrollable_frame(self.frame)
        
        ttk.Label(scrollable_frame, text="Resultados de la Predicción Electoral 2025",
                 style='Header.TLabel').pack(pady=(10, 20))

        # Sección de resultados de votos
        self.frame_votos = ttk.LabelFrame(scrollable_frame, text="Predicción de Votos 2025")
        self.frame_votos.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)

        # Sección de resultados de escaños (Senadores)
        self.frame_senadores = ttk.LabelFrame(scrollable_frame, text=f"Distribución de Senadores (Total: {TOTAL_SENADORES})")
        self.frame_senadores.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)

        # Sección de resultados de escaños (Diputados)
        self.frame_diputados = ttk.LabelFrame(scrollable_frame, text=f"Distribución de Diputados (Total: {TOTAL_DIPUTADOS})")
        self.frame_diputados.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)

        # Botón para simular segunda vuelta si aplica
        self.btn_segunda_vuelta = ttk.Button(scrollable_frame, 
                                           text="Simular Segunda Vuelta", 
                                           command=self.simular_segunda_vuelta,
                                           state='disabled')
        self.btn_segunda_vuelta.pack(pady=10)

        # Botón para refrescar resultados
        ttk.Button(scrollable_frame, text="Actualizar Vista de Resultados", 
                  command=self.mostrar_resultados).pack(pady=15)
    
    def mostrar_resultados(self):
        """Muestra los resultados de la predicción."""
        if not self.prediccion_ejecutada:
            ttk.Label(self.frame, text="Ejecute el modelo en la pestaña 'Configuración del Modelo' para ver los resultados.",
                     style='Subheader.TLabel').pack(pady=50)
            return

        # Actualizar estado del botón de segunda vuelta
        if self.segunda_vuelta:
            self.btn_segunda_vuelta.config(state='normal')
        else:
            self.btn_segunda_vuelta.config(state='disabled')

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
            ttk.Label(self.frame_votos, text="No hay predicción de votos disponible.").pack(pady=5)
            return

        columns = ['Partido', 'Porcentaje de Votos (%)']
        self.tree_votos = ttk.Treeview(self.frame_votos, columns=columns, show='headings', 
                                      height=len(self.prediccion_votos))
        self.tree_votos.pack(fill='both', expand=True, padx=10, pady=5)

        for col in columns:
            self.tree_votos.heading(col, text=col)
            self.tree_votos.column(col, width=150, anchor='center')

        sorted_votos = sorted(self.prediccion_votos.items(), key=lambda item: item[1], reverse=True)
        for party, percentage in sorted_votos:
            self.tree_votos.insert('', 'end', values=(party, f"{percentage:.2f}%"))
    
    def _crear_grafico_votos(self):
        """Crea el gráfico de barras para la predicción de votos."""
        self.canvas_votos = crear_grafico_votos(self.prediccion_votos, self.frame_votos)
    
    def _crear_tabla_escanos(self, parent_frame, escanos_data):
        """Crea una tabla para mostrar la distribución de escaños."""
        if not escanos_data:
            ttk.Label(parent_frame, text="No se asignaron escaños para esta categoría.").pack(pady=5)
            return

        columns = ['Partido', 'Escaños']
        tree_escanos = ttk.Treeview(parent_frame, columns=columns, show='headings', 
                                   height=min(10, len(escanos_data)))
        tree_escanos.pack(fill='both', expand=True, padx=10, pady=5)

        for col in columns:
            tree_escanos.heading(col, text=col)
            tree_escanos.column(col, width=150, anchor='center')

        sorted_escanos = sorted(escanos_data.items(), key=lambda item: item[1], reverse=True)
        for party, seats in sorted_escanos:
            tree_escanos.insert('', 'end', values=(party, seats))
        
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