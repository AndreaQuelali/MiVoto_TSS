"""
Vista para la gestión de datos históricos y encuestas
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, Callable, Optional
import tkinter as tk

from utils.chart_utils import crear_grafico_historicos, crear_grafico_encuestas
from utils.file_utils import cargar_encuestas_desde_archivo, cargar_historicos_desde_archivo
from utils.logo_utils import logo_manager
from config.settings import EXCEL_CSV_FILE_TYPES
from config.bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD,
    BOLIVIA_BG_CONTAINER, BOLIVIA_BG_FRAME, BOLIVIA_BG_SECTION
)


class DatosView:
    """
    Vista para la visualización y gestión de datos históricos y de encuestas.
    """
    
    def __init__(self, parent, datos_historicos: Dict, encuestas_2025: Dict, 
                 on_datos_actualizados: Optional[Callable] = None):
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
            text="Gestión de Datos para el Modelo Predictivo 2025",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=(BOLIVIA_RED, BOLIVIA_RED)
        )
        titulo_label.pack(pady=(0, 24))

        # Scrollable frame para el contenido de datos
        self.scrollable_frame = ctk.CTkScrollableFrame(contenedor, width=800, height=500, fg_color=BOLIVIA_BG_WARM)
        self.scrollable_frame.pack(fill='both', expand=True, padx=0, pady=0)

        # Sección de datos históricos
        self.frame_historicos = ctk.CTkFrame(self.scrollable_frame, fg_color=BOLIVIA_BG_SECTION)
        self.frame_historicos.pack(fill='x', padx=10, pady=10)
        historicos_label = ctk.CTkLabel(
            self.frame_historicos,
            text="Resultados Históricos de Elecciones en Bolivia",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=(BOLIVIA_DARK_GREEN, BOLIVIA_DARK_GREEN)
        )
        historicos_label.pack(pady=(12, 8))

        # Sección de encuestas 2025
        self.frame_encuestas = ctk.CTkFrame(self.scrollable_frame, fg_color=BOLIVIA_BG_SECTION)
        self.frame_encuestas.pack(fill='x', padx=10, pady=10)
        encuestas_label = ctk.CTkLabel(
            self.frame_encuestas,
            text="Encuestas de Intención de Voto 2025",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=(BOLIVIA_DARK_GREEN, BOLIVIA_DARK_GREEN)
        )
        encuestas_label.pack(pady=(12, 8))

        # Botones para cargar nuevos datos
        btn_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=BOLIVIA_BG_FRAME)
        btn_frame.pack(pady=30)
        cargar_encuestas_btn = ctk.CTkButton(
            btn_frame, 
            text="Cargar Nuevas Encuestas (CSV/Excel)",
            command=self.cargar_encuestas,
            font=ctk.CTkFont(size=13, weight="bold"),
            width=220,
            height=38,
            fg_color=BOLIVIA_GREEN,
            hover_color=BOLIVIA_DARK_GREEN
        )
        cargar_encuestas_btn.pack(side='left', padx=18)
        cargar_historicos_btn = ctk.CTkButton(
            btn_frame, 
            text="Cargar Datos Históricos (CSV/Excel)",
            command=self.cargar_historicos,
            font=ctk.CTkFont(size=13, weight="bold"),
            width=220,
            height=38,
            fg_color=BOLIVIA_GREEN,
            hover_color=BOLIVIA_DARK_GREEN
        )
        cargar_historicos_btn.pack(side='left', padx=18)
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
            no_data_label = ctk.CTkLabel(
                self.frame_historicos, 
                text="No hay datos históricos cargados.",
                text_color=("gray50", "gray50")
            )
            no_data_label.pack(pady=5)
            return

        # Obtener todos los partidos únicos para las columnas
        all_parties = sorted(list(set(p for data in self.datos_historicos.values() for p in data.keys())))
        columns = ['Año'] + all_parties

        # Frame para contener la tabla y el scrollbar
        tabla_frame = ctk.CTkFrame(self.frame_historicos, fg_color="transparent")
        tabla_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Crear tabla usando CTkTextbox para simular una tabla
        self.tree_historicos = ctk.CTkTextbox(tabla_frame, height=200, fg_color="#f5f5f5", wrap="none")
        self.tree_historicos.pack(side='left', fill='both', expand=True)
        self.tree_historicos.configure(font=("Consolas", 13, "bold"))

        # Scrollbar horizontal
        h_scroll = tk.Scrollbar(tabla_frame, orient='horizontal', command=self.tree_historicos.xview)
        h_scroll.pack(side='bottom', fill='x')
        self.tree_historicos.configure(xscrollcommand=h_scroll.set)

        # --- DRAG TO SCROLL ---
        self._add_drag_to_scroll(self.tree_historicos)

        # Crear encabezados (históricos)
        header = "Año".ljust(8)
        for party in all_parties:
            header += f"{party}".ljust(24)
        self.tree_historicos.insert("1.0", header + "\n")
        self.tree_historicos.insert("end", "=" * len(header) + "\n")

        # Insertar datos (históricos)
        for idx, (year, data) in enumerate(sorted(self.datos_historicos.items())):
            row = f"{year}".ljust(8)
            for party in all_parties:
                row += f"{data.get(party, 0):.1f}%".ljust(24)
            self.tree_historicos.insert("end", row + "\n")
            self.tree_historicos.insert("end", "-" * len(header) + "\n")

        self.tree_historicos.configure(state="disabled")
    
    def _crear_grafico_historicos(self):
        """Crea el gráfico de líneas para la evolución histórica de votos."""
        self.canvas_historicos = crear_grafico_historicos(self.datos_historicos, self.frame_historicos)
    
    def _crear_tabla_encuestas(self):
        """Crea la tabla para mostrar los datos de las encuestas 2025."""
        if not self.encuestas_2025:
            no_data_label = ctk.CTkLabel(
                self.frame_encuestas, 
                text="No hay datos de encuestas cargados.",
                text_color=("gray50", "gray50")
            )
            no_data_label.pack(pady=5)
            return

        # Obtener todos los partidos únicos de las encuestas
        all_parties = sorted(list(set(p for data in self.encuestas_2025.values() for p in data.keys())))
        columns = ['Encuesta'] + all_parties

        # Frame para contener la tabla y el scrollbar
        tabla_frame = ctk.CTkFrame(self.frame_encuestas, fg_color="transparent")
        tabla_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Crear tabla usando CTkTextbox para simular una tabla
        self.tree_encuestas = ctk.CTkTextbox(tabla_frame, height=150, fg_color="#f5f5f5", wrap="none")
        self.tree_encuestas.pack(side='left', fill='both', expand=True)
        self.tree_encuestas.configure(font=("Consolas", 13, "bold"))

        # Scrollbar horizontal
        h_scroll = tk.Scrollbar(tabla_frame, orient='horizontal', command=self.tree_encuestas.xview)
        h_scroll.pack(side='bottom', fill='x')
        self.tree_encuestas.configure(xscrollcommand=h_scroll.set)

        # --- DRAG TO SCROLL ---
        self._add_drag_to_scroll(self.tree_encuestas)

        # Crear encabezados (encuestas)
        header = "Encuesta".ljust(15)
        for party in all_parties:
            header += f"{party}".ljust(24)
        self.tree_encuestas.insert("1.0", header + "\n")
        self.tree_encuestas.insert("end", "=" * len(header) + "\n")

        # Insertar datos (encuestas)
        for idx, (survey_name, data) in enumerate(self.encuestas_2025.items()):
            row = f"{survey_name}".ljust(15)
            for party in all_parties:
                row += f"{data.get(party, 0):.1f}%".ljust(24)
            self.tree_encuestas.insert("end", row + "\n")
            self.tree_encuestas.insert("end", "-" * len(header) + "\n")

        self.tree_encuestas.configure(state="disabled")
    
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

    def _add_drag_to_scroll(self, textbox):
        """Permite hacer drag-to-scroll horizontal en un CTkTextbox."""
        def on_mouse_down(event):
            textbox._drag_scroll_x = event.x
            textbox._drag_scroll_start = textbox.xview()
            textbox._dragging = True

        def on_mouse_move(event):
            if getattr(textbox, '_dragging', False):
                dx = event.x - textbox._drag_scroll_x
                # Ajusta la sensibilidad del scroll (mayor divisor = más lento)
                factor = 2.0 * (textbox.winfo_width() or 1)
                start = textbox._drag_scroll_start[0] - dx / factor
                textbox.xview_moveto(max(0, min(1, start)))

        def on_mouse_up(event):
            textbox._dragging = False

        textbox.bind('<Button-1>', on_mouse_down)
        textbox.bind('<B1-Motion>', on_mouse_move)
        textbox.bind('<ButtonRelease-1>', on_mouse_up) 