"""
Vista para mostrar los resultados de la predicción electoral
"""
import customtkinter as ctk
from tkinter import messagebox, ttk
from typing import Dict, Callable, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from utils.chart_utils import crear_grafico_votos, crear_grafico_escanos
from utils.logo_utils import logo_manager
from utils.style_utils import aplicar_estilo_grafico
from config.settings import TOTAL_SENADORES, TOTAL_DIPUTADOS, DEPARTAMENTOS_BOLIVIA
from config.bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD,
    BOLIVIA_BG_CONTAINER, BOLIVIA_BG_SECTION
)


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
        self.frame = ctk.CTkFrame(self.parent, fg_color=BOLIVIA_BG_WARM)
        
        # Contenedor principal centrado
        contenedor = ctk.CTkFrame(self.frame, fg_color=BOLIVIA_BG_CONTAINER)
        contenedor.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Logo del sistema encima del título, sin borde
        logo_label = logo_manager.obtener_logo_widget(contenedor, size=(100, 100))
        logo_label.pack(pady=(0, 15))
        
        # Título debajo del logo, centrado
        titulo_label = ctk.CTkLabel(
            contenedor, 
            text="Resultados de la Predicción Electoral 2025",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=(BOLIVIA_RED, BOLIVIA_RED)
        )
        titulo_label.pack(pady=(0, 24))

        # Scrollable frame para el contenido de resultados
        self.scrollable_frame = ctk.CTkScrollableFrame(contenedor, width=800, height=500, fg_color=BOLIVIA_BG_WARM)
        self.scrollable_frame.pack(fill='both', expand=True, padx=0, pady=0)

        # Sección de resultados de votos
        self.frame_votos = ctk.CTkFrame(self.scrollable_frame, fg_color=BOLIVIA_BG_SECTION)
        self.frame_votos.pack(fill='x', padx=10, pady=12)
        votos_label = ctk.CTkLabel(
            self.frame_votos,
            text="Predicción de Votos 2025",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=(BOLIVIA_DARK_GREEN, BOLIVIA_DARK_GREEN)
        )
        votos_label.pack(pady=(12, 8))

        # Sección de resultados de escaños (Senadores)
        self.frame_senadores = ctk.CTkFrame(self.scrollable_frame, fg_color=BOLIVIA_BG_SECTION)
        self.frame_senadores.pack(fill='x', padx=10, pady=12)
        senadores_label = ctk.CTkLabel(
            self.frame_senadores,
            text=f"Distribución de Senadores (Total: {TOTAL_SENADORES})",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=(BOLIVIA_DARK_GREEN, BOLIVIA_DARK_GREEN)
        )
        senadores_label.pack(pady=(12, 8))

        # Sección de resultados de escaños (Diputados)
        self.frame_diputados = ctk.CTkFrame(self.scrollable_frame, fg_color=BOLIVIA_BG_SECTION)
        self.frame_diputados.pack(fill='x', padx=10, pady=12)
        diputados_label = ctk.CTkLabel(
            self.frame_diputados,
            text=f"Distribución de Diputados (Total: {TOTAL_DIPUTADOS})",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=(BOLIVIA_DARK_GREEN, BOLIVIA_DARK_GREEN)
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
            height=38,
            fg_color=BOLIVIA_GREEN,
            hover_color=BOLIVIA_DARK_GREEN
        )
        self.btn_segunda_vuelta.pack(pady=18)

        # Botón para refrescar resultados
        actualizar_btn = ctk.CTkButton(
            self.scrollable_frame, 
            text="Actualizar Vista de Resultados", 
            command=self.mostrar_resultados,
            font=ctk.CTkFont(size=13, weight="bold"),
            width=260,
            height=38,
            fg_color=BOLIVIA_GREEN,
            hover_color=BOLIVIA_DARK_GREEN
        )
        actualizar_btn.pack(pady=10)
    
    def mostrar_resultados(self):
        """Muestra los resultados de la predicción."""
        if not self.prediccion_ejecutada:
            # Limpiar contenido existente de los frames
            for widget in self.frame_votos.winfo_children():
                widget.destroy()
            for widget in self.frame_senadores.winfo_children():
                widget.destroy()
            for widget in self.frame_diputados.winfo_children():
                widget.destroy()
            
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
        
        # Limpiar contenido existente de los frames
        for widget in self.frame_votos.winfo_children():
            widget.destroy()
        for widget in self.frame_senadores.winfo_children():
            widget.destroy()
        for widget in self.frame_diputados.winfo_children():
            widget.destroy()

        self._crear_seccion_votos(self.frame_votos, self.prediccion_votos)
        self._crear_seccion_senadores(self.frame_senadores, self.senadores)
        self._crear_seccion_diputados(self.frame_diputados, self.diputados)
    
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
    
    def actualizar_resultados(self, prediccion_votos: Dict[str, float], 
                             senadores: Dict[str, int], diputados: Dict[str, int],
                             segunda_vuelta: bool, candidatos_segunda_vuelta: List[str],
                             diputados_plurinominales: Dict[str, int] = None,
                             diputados_uninominales: Dict[str, int] = None,
                             diputados_uninominales_por_depto: Dict[str, Dict[str, int]] = None):
        """
        Actualiza los resultados mostrados en la vista.
        
        Args:
            prediccion_votos: Predicción de votos por partido
            senadores: Distribución de senadores por partido
            diputados: Distribución total de diputados por partido
            segunda_vuelta: Si se requiere segunda vuelta
            candidatos_segunda_vuelta: Lista de candidatos para segunda vuelta
            diputados_plurinominales: Distribución de diputados plurinominales
            diputados_uninominales: Distribución de diputados uninominales
            diputados_uninominales_por_depto: Distribución de diputados uninominales por departamento
        """
        # Actualizar variables de instancia
        self.prediccion_votos = prediccion_votos
        self.senadores = senadores
        self.diputados = diputados
        self.segunda_vuelta = segunda_vuelta
        self.candidatos_segunda_vuelta = candidatos_segunda_vuelta
        self.prediccion_ejecutada = True
        
        # Mostrar los resultados
        self.mostrar_resultados()
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame 
    
    def _crear_seccion_votos(self, parent, prediccion_votos):
        """Crea la sección de predicción de votos."""
        seccion = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(seccion, text="PREDICCIÓN DE VOTOS 2025", 
                             font=ctk.CTkFont(size=16, weight="bold"),
                             text_color=BOLIVIA_RED)
        titulo.pack(pady=10)
        
        # Crear gráfico de votos
        self.canvas_votos = crear_grafico_votos(prediccion_votos, seccion)
        
        # Crear tabla de votos
        self._crear_tabla_votos(seccion, prediccion_votos)
    
    def _crear_seccion_senadores(self, parent, senadores):
        """Crea la sección de distribución de senadores."""
        seccion = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(seccion, text=f"DISTRIBUCIÓN DE SENADORES (Total: {TOTAL_SENADORES})", 
                             font=ctk.CTkFont(size=16, weight="bold"),
                             text_color=BOLIVIA_DARK_GREEN)
        titulo.pack(pady=10)
        
        # Crear gráfico de senadores
        self.canvas_senadores = crear_grafico_escanos(senadores, seccion, "Senadores")
        
        # Crear tabla de senadores
        self._crear_tabla_escanos(seccion, senadores, "Senadores")
    
    def _crear_seccion_diputados(self, parent, diputados):
        """Crea la sección de distribución total de diputados."""
        seccion = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(seccion, text=f"DISTRIBUCIÓN TOTAL DE DIPUTADOS (Total: {TOTAL_DIPUTADOS})", 
                             font=ctk.CTkFont(size=16, weight="bold"),
                             text_color=BOLIVIA_DARK_GREEN)
        titulo.pack(pady=10)
        
        # Crear gráfico de diputados
        self.canvas_diputados = crear_grafico_escanos(diputados, seccion, "Diputados")
        
        # Crear tabla de diputados
        self._crear_tabla_escanos(seccion, diputados, "Diputados")
    
    def _crear_seccion_diputados_plurinominales(self, parent, diputados_plurinominales):
        """Crea la sección de diputados plurinominales."""
        seccion = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(seccion, text="DIPUTADOS PLURINOMINALES (Lista Nacional - 60 escaños)", 
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=BOLIVIA_GOLD)
        titulo.pack(pady=10)
        
        # Crear tabla de diputados plurinominales
        self._crear_tabla_escanos(seccion, diputados_plurinominales, "Diputados Plurinominales")
    
    def _crear_seccion_diputados_uninominales(self, parent, diputados_uninominales):
        """Crea la sección de diputados uninominales."""
        seccion = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(seccion, text="DIPUTADOS UNINOMINALES (Circunscripciones - 70 escaños)", 
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=BOLIVIA_GOLD)
        titulo.pack(pady=10)
        
        # Crear tabla de diputados uninominales
        self._crear_tabla_escanos(seccion, diputados_uninominales, "Diputados Uninominales")
    
    def _crear_seccion_diputados_por_depto(self, parent, diputados_uninominales_por_depto):
        """Crea la sección de diputados uninominales por departamento."""
        seccion = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(seccion, text="DIPUTADOS UNINOMINALES POR DEPARTAMENTO", 
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color=BOLIVIA_GOLD)
        titulo.pack(pady=10)
        
        # Crear tabla de diputados por departamento
        self._crear_tabla_diputados_por_depto(seccion, diputados_uninominales_por_depto)
    
    def _crear_seccion_segunda_vuelta(self, parent, candidatos_segunda_vuelta):
        """Crea la sección de segunda vuelta."""
        seccion = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_CONTAINER)
        seccion.pack(fill="x", padx=10, pady=5)
        
        titulo = ctk.CTkLabel(seccion, text="SEGUNDA VUELTA REQUERIDA", 
                             font=ctk.CTkFont(size=16, weight="bold"),
                             text_color=BOLIVIA_RED)
        titulo.pack(pady=10)
        
        info = ctk.CTkLabel(seccion, 
                           text=f"Los candidatos que pasan a segunda vuelta son:\n{candidatos_segunda_vuelta[0]} y {candidatos_segunda_vuelta[1]}",
                           font=ctk.CTkFont(size=12),
                           text_color=BOLIVIA_TEXT_DARK)
        info.pack(pady=10)
    
    def _crear_boton_segunda_vuelta(self, parent):
        """Crea el botón para simular segunda vuelta."""
        boton_frame = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_WARM)
        boton_frame.pack(fill="x", padx=10, pady=10)
        
        boton = ctk.CTkButton(boton_frame, 
                             text="Simular Segunda Vuelta",
                             command=self.on_simular_segunda_vuelta,
                             fg_color=BOLIVIA_RED,
                             hover_color=BOLIVIA_DARK_GREEN,
                             font=ctk.CTkFont(size=14, weight="bold"))
        boton.pack(pady=10)
    
    def _crear_tabla_votos(self, parent, prediccion_votos):
        """Crea la tabla de votos."""
        # Frame para la tabla
        tabla_frame = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_WARM)
        tabla_frame.pack(fill="x", padx=20, pady=10)
        
        # Crear Treeview
        columns = ('Partido', 'Porcentaje')
        self.tree_votos = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=6)
        
        # Configurar columnas
        self.tree_votos.heading('Partido', text='Partido Político')
        self.tree_votos.heading('Porcentaje', text='Porcentaje (%)')
        self.tree_votos.column('Partido', width=200)
        self.tree_votos.column('Porcentaje', width=100)
        
        # Insertar datos
        for partido, porcentaje in sorted(prediccion_votos.items(), key=lambda x: x[1], reverse=True):
            self.tree_votos.insert('', 'end', values=(partido, f'{porcentaje:.2f}%'))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree_votos.yview)
        self.tree_votos.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        self.tree_votos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_tabla_escanos(self, parent, escanos, tipo):
        """Crea la tabla de escaños."""
        # Frame para la tabla
        tabla_frame = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_WARM)
        tabla_frame.pack(fill="x", padx=20, pady=10)
        
        # Crear Treeview
        columns = ('Partido', 'Escaños')
        tree = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=6)
        
        # Configurar columnas
        tree.heading('Partido', text='Partido Político')
        tree.heading('Escaños', text=f'{tipo}')
        tree.column('Partido', width=200)
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
    
    def _crear_tabla_diputados_por_depto(self, parent, diputados_por_depto):
        """Crea la tabla de diputados por departamento."""
        # Frame para la tabla
        tabla_frame = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_WARM)
        tabla_frame.pack(fill="x", padx=20, pady=10)
        
        # Crear Treeview
        columns = ('Departamento', 'Partido', 'Escaños')
        tree = ttk.Treeview(tabla_frame, columns=columns, show='headings', height=8)
        
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