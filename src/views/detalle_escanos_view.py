"""
Vista para mostrar el detalle de escaños uninominales y plurinominales
"""
import customtkinter as ctk
from tkinter import ttk
from typing import Dict, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from utils.chart_utils import crear_grafico_escanos
from config.bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD,
    BOLIVIA_BG_CONTAINER
)
from config.settings import DEPARTAMENTOS_BOLIVIA


class DetalleEscanosView:
    """
    Vista para mostrar el detalle completo de la distribución de escaños.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.crear_vista()
    
    def crear_vista(self):
        """Crea la vista de detalle de escaños."""
        self.frame = ctk.CTkFrame(self.parent, fg_color=BOLIVIA_BG_WARM)
        
        # Contenedor principal con scroll
        self.main_container = ctk.CTkScrollableFrame(self.frame, fg_color=BOLIVIA_BG_WARM)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título principal
        titulo = ctk.CTkLabel(
            self.main_container,
            text="DETALLE DE DISTRIBUCIÓN DE ESCAÑOS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=BOLIVIA_RED
        )
        titulo.pack(pady=20)
        
        # Información explicativa
        info_text = """
        Esta sección muestra el desglose detallado de la distribución de escaños según la Ley 026 de Bolivia:
        
        • DIPUTADOS PLURINOMINALES: 60 escaños asignados por lista nacional usando el método D'Hondt
        • DIPUTADOS UNINOMINALES: 70 escaños asignados por circunscripciones departamentales
        • SENADORES: 36 escaños (4 por departamento) asignados por lista nacional
        
        Los escaños uninominales se distribuyen considerando la fuerza electoral de cada partido en cada departamento.
        """
        
        info_label = ctk.CTkLabel(
            self.main_container,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color=BOLIVIA_TEXT_DARK,
            wraplength=800,
            justify="left"
        )
        info_label.pack(pady=20, padx=20)
    
    def actualizar_detalle(self, detalle_escanos: Dict):
        """
        Actualiza la vista con el detalle de escaños.
        
        Args:
            detalle_escanos: Diccionario con el detalle completo de escaños
        """
        # Limpiar contenido anterior
        for widget in self.main_container.winfo_children():
            if widget != self.main_container.winfo_children()[0]:  # Mantener título
                widget.destroy()
        
        # Sección de Diputados Plurinominales
        self._crear_seccion_plurinominales(detalle_escanos.get('diputados_plurinominales', {}))
        
        # Sección de Diputados Uninominales
        self._crear_seccion_uninominales(detalle_escanos.get('diputados_uninominales', {}))
        
        # Sección de Diputados por Departamento
        self._crear_seccion_por_departamento(detalle_escanos.get('diputados_uninominales_por_depto', {}))
        
        # Sección de Senadores
        self._crear_seccion_senadores(detalle_escanos.get('senadores', {}))
        
        # Resumen total
        self._crear_resumen_total(detalle_escanos.get('total_diputados', {}))
    
    def _crear_seccion_plurinominales(self, diputados_plurinominales: Dict[str, int]):
        """Crea la sección de diputados plurinominales."""
        seccion = ctk.CTkFrame(self.main_container, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=10)
        
        titulo = ctk.CTkLabel(
            seccion,
            text="DIPUTADOS PLURINOMINALES (Lista Nacional - 60 escaños)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=BOLIVIA_GOLD
        )
        titulo.pack(pady=15)
        
        # Gráfico
        if diputados_plurinominales:
            canvas = crear_grafico_escanos(diputados_plurinominales, seccion, "Diputados Plurinominales")
        
        # Tabla
        self._crear_tabla_escanos(seccion, diputados_plurinominales, "Plurinominales")
    
    def _crear_seccion_uninominales(self, diputados_uninominales: Dict[str, int]):
        """Crea la sección de diputados uninominales."""
        seccion = ctk.CTkFrame(self.main_container, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=10)
        
        titulo = ctk.CTkLabel(
            seccion,
            text="DIPUTADOS UNINOMINALES (Circunscripciones - 70 escaños)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=BOLIVIA_GOLD
        )
        titulo.pack(pady=15)
        
        # Gráfico
        if diputados_uninominales:
            canvas = crear_grafico_escanos(diputados_uninominales, seccion, "Diputados Uninominales")
        
        # Tabla
        self._crear_tabla_escanos(seccion, diputados_uninominales, "Uninominales")
    
    def _crear_seccion_por_departamento(self, diputados_por_depto: Dict[str, Dict[str, int]]):
        """Crea la sección de diputados por departamento."""
        seccion = ctk.CTkFrame(self.main_container, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=10)
        
        titulo = ctk.CTkLabel(
            seccion,
            text="DIPUTADOS UNINOMINALES POR DEPARTAMENTO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=BOLIVIA_GOLD
        )
        titulo.pack(pady=15)
        
        # Tabla por departamento
        self._crear_tabla_por_departamento(seccion, diputados_por_depto)
    
    def _crear_seccion_senadores(self, senadores: Dict[str, int]):
        """Crea la sección de senadores."""
        seccion = ctk.CTkFrame(self.main_container, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=10)
        
        titulo = ctk.CTkLabel(
            seccion,
            text="SENADORES (4 por departamento - 36 totales)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=BOLIVIA_DARK_GREEN
        )
        titulo.pack(pady=15)
        
        # Gráfico
        if senadores:
            canvas = crear_grafico_escanos(senadores, seccion, "Senadores")
        
        # Tabla
        self._crear_tabla_escanos(seccion, senadores, "Senadores")
    
    def _crear_resumen_total(self, total_diputados: Dict[str, int]):
        """Crea la sección de resumen total."""
        seccion = ctk.CTkFrame(self.main_container, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=10)
        
        titulo = ctk.CTkLabel(
            seccion,
            text="RESUMEN TOTAL DE DIPUTADOS (130 escaños)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=BOLIVIA_RED
        )
        titulo.pack(pady=15)
        
        # Gráfico
        if total_diputados:
            canvas = crear_grafico_escanos(total_diputados, seccion, "Diputados Totales")
        
        # Tabla
        self._crear_tabla_escanos(seccion, total_diputados, "Total Diputados")
    
    def _crear_tabla_escanos(self, parent, escanos: Dict[str, int], tipo: str):
        """Crea una tabla de escaños."""
        if not escanos:
            return
        
        # Frame para la tabla
        tabla_frame = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_WARM)
        tabla_frame.pack(fill="x", padx=20, pady=10)
        
        # Crear Treeview
        columns = ('Partido', 'Escaños')
        tree = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=6)
        
        # Configurar columnas
        tree.heading('Partido', text='Partido Político')
        tree.heading('Escaños', text=f'{tipo}')
        tree.column('Partido', width=250)
        tree.column('Escaños', width=100)
        
        # Insertar datos
        for partido, num_escanos in sorted(escanos.items(), key=lambda x: x[1], reverse=True):
            tree.insert('', 'end', values=(partido, num_escanos))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_tabla_por_departamento(self, parent, diputados_por_depto: Dict[str, Dict[str, int]]):
        """Crea la tabla de diputados por departamento."""
        if not diputados_por_depto:
            return
        
        # Frame para la tabla
        tabla_frame = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_WARM)
        tabla_frame.pack(fill="x", padx=20, pady=10)
        
        # Crear Treeview
        columns = ('Departamento', 'Partido', 'Escaños')
        tree = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        tree.heading('Departamento', text='Departamento')
        tree.heading('Partido', text='Partido Político')
        tree.heading('Escaños', text='Escaños')
        tree.column('Departamento', width=150)
        tree.column('Partido', width=200)
        tree.column('Escaños', width=100)
        
        # Insertar datos
        for departamento, partidos in diputados_por_depto.items():
            for partido, escanos in partidos.items():
                tree.insert('', 'end', values=(departamento, partido, escanos))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame