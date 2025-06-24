"""
Vista para la gestión de datos históricos y encuestas
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Callable

from utils.style_utils import crear_scrollable_frame
from utils.chart_utils import crear_grafico_historicos, crear_grafico_encuestas
from utils.file_utils import cargar_encuestas_desde_archivo, cargar_historicos_desde_archivo
from config.settings import EXCEL_CSV_FILE_TYPES


class DatosView:
    """
    Vista para la visualización y gestión de datos históricos y de encuestas.
    """
    
    def __init__(self, parent, datos_historicos: Dict, encuestas_2025: Dict, 
                 on_datos_actualizados: Callable = None):
        self.parent = parent
        self.datos_historicos = datos_historicos
        self.encuestas_2025 = encuestas_2025
        self.on_datos_actualizados = on_datos_actualizados
        
        # Widgets de la interfaz
        self.frame = None
        self.tree_historicos = None
        self.canvas_historicos = None
        self.tree_encuestas = None
        self.canvas_encuestas = None
        
        self.crear_vista()
    
    def crear_vista(self):
        """Crea la vista de datos."""
        self.frame = ttk.Frame(self.parent, padding="10")
        
        # Crear frame con scrollbar
        canvas, scrollbar, scrollable_frame = crear_scrollable_frame(self.frame)
        
        ttk.Label(scrollable_frame, text="Gestión de Datos para el Modelo Predictivo 2025",
                  style='Header.TLabel').pack(pady=(10, 20))

        # Sección de datos históricos
        self.frame_historicos = ttk.LabelFrame(scrollable_frame, text="Resultados Históricos de Elecciones en Bolivia")
        self.frame_historicos.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)

        # Sección de encuestas 2025
        self.frame_encuestas = ttk.LabelFrame(scrollable_frame, text="Encuestas de Intención de Voto 2025")
        self.frame_encuestas.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)

        # Botones para cargar nuevos datos
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Cargar Nuevas Encuestas (CSV/Excel)",
                   command=self.cargar_encuestas).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Cargar Datos Históricos (CSV/Excel)",
                   command=self.cargar_historicos).pack(side='left', padx=10)

        self.actualizar_tablas_datos()
    
    def actualizar_tablas_datos(self):
        """Actualiza las tablas y gráficos de datos."""
        # Limpiar widgets existentes
        self._limpiar_widgets()
        
        self._crear_tabla_historicos()
        self._crear_grafico_historicos()
        self._crear_tabla_encuestas()
        self._crear_grafico_encuestas()
    
    def _limpiar_widgets(self):
        """Limpia los widgets existentes."""
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        for widget in [self.tree_historicos, self.canvas_historicos,
                      self.tree_encuestas, self.canvas_encuestas]:
            if widget:
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()
                else:
                    widget.destroy()
        plt.close('all')
    
    def _crear_tabla_historicos(self):
        """Crea la tabla para mostrar los datos históricos."""
        if not self.datos_historicos:
            ttk.Label(self.frame_historicos, text="No hay datos históricos cargados.").pack(pady=5)
            return

        # Obtener todos los partidos únicos para las columnas
        all_parties = sorted(list(set(p for data in self.datos_historicos.values() for p in data.keys())))
        columns = ['Año'] + all_parties

        self.tree_historicos = ttk.Treeview(self.frame_historicos, columns=columns, show='headings', height=7)
        self.tree_historicos.pack(fill='both', expand=True, padx=10, pady=5)

        for col in columns:
            self.tree_historicos.heading(col, text=col)
            self.tree_historicos.column(col, width=80 if col == 'Año' else 100, anchor='center')

        for year, data in sorted(self.datos_historicos.items()):
            values = [year] + [f"{data.get(party, 0):.1f}%" for party in all_parties]
            self.tree_historicos.insert('', 'end', values=values)

        # Scrollbar para la tabla
        vsb = ttk.Scrollbar(self.frame_historicos, orient="vertical", command=self.tree_historicos.yview)
        vsb.pack(side='right', fill='y')
        self.tree_historicos.configure(yscrollcommand=vsb.set)
    
    def _crear_grafico_historicos(self):
        """Crea el gráfico de líneas para la evolución histórica de votos."""
        self.canvas_historicos = crear_grafico_historicos(self.datos_historicos, self.frame_historicos)
    
    def _crear_tabla_encuestas(self):
        """Crea la tabla para mostrar los datos de las encuestas 2025."""
        if not self.encuestas_2025:
            ttk.Label(self.frame_encuestas, text="No hay datos de encuestas cargados.").pack(pady=5)
            return

        # Obtener todos los partidos únicos de las encuestas
        all_parties = sorted(list(set(p for data in self.encuestas_2025.values() for p in data.keys())))
        columns = ['Encuesta'] + all_parties

        self.tree_encuestas = ttk.Treeview(self.frame_encuestas, columns=columns, show='headings', height=5)
        self.tree_encuestas.pack(fill='both', expand=True, padx=10, pady=5)

        for col in columns:
            self.tree_encuestas.heading(col, text=col)
            self.tree_encuestas.column(col, width=100, anchor='center')

        for survey_name, data in self.encuestas_2025.items():
            values = [survey_name] + [f"{data.get(party, 0):.1f}%" for party in all_parties]
            self.tree_encuestas.insert('', 'end', values=values)

        # Scrollbar para la tabla
        vsb = ttk.Scrollbar(self.frame_encuestas, orient="vertical", command=self.tree_encuestas.yview)
        vsb.pack(side='right', fill='y')
        self.tree_encuestas.configure(yscrollcommand=vsb.set)
    
    def _crear_grafico_encuestas(self):
        """Crea el gráfico de barras para el promedio de las encuestas 2025."""
        self.canvas_encuestas = crear_grafico_encuestas(self.encuestas_2025, self.frame_encuestas)
    
    def cargar_encuestas(self):
        """Permite al usuario cargar nuevos datos de encuestas."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de encuestas",
            filetypes=EXCEL_CSV_FILE_TYPES
        )
        if not file_path:
            return
        
        try:
            encuestas_cargadas = cargar_encuestas_desde_archivo(file_path)
            self.encuestas_2025 = encuestas_cargadas
            messagebox.showinfo("Éxito", f"Encuestas cargadas correctamente desde '{file_path}'.")
            self.actualizar_tablas_datos()
            if self.on_datos_actualizados:
                self.on_datos_actualizados()
        except Exception as e:
            messagebox.showerror("Error de Carga", str(e))
    
    def cargar_historicos(self):
        """Permite al usuario cargar nuevos datos históricos."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de datos históricos",
            filetypes=EXCEL_CSV_FILE_TYPES
        )
        if not file_path:
            return
        
        try:
            historicos_cargados = cargar_historicos_desde_archivo(file_path)
            self.datos_historicos = historicos_cargados
            messagebox.showinfo("Éxito", f"Datos históricos cargados correctamente desde '{file_path}'.")
            self.actualizar_tablas_datos()
            if self.on_datos_actualizados:
                self.on_datos_actualizados()
        except Exception as e:
            messagebox.showerror("Error de Carga", str(e))
    
    def actualizar_datos(self, datos_historicos: Dict, encuestas_2025: Dict):
        """Actualiza los datos mostrados en la vista."""
        self.datos_historicos = datos_historicos
        self.encuestas_2025 = encuestas_2025
        self.actualizar_tablas_datos()
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame 