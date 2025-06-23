import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from collections import defaultdict # Import defaultdict

class PredictorElectoral2025:
    """
    Aplicación de Escritorio para la Predicción Electoral en Bolivia 2025.

    Permite cargar datos históricos y encuestas actuales, configurar parámetros
    del modelo predictivo, visualizar resultados de votos y distribución de escaños
    (senadores y diputados), y exportar los resultados a Excel, imágenes o PDF.
    """

    def __init__(self, root):
        """
        Inicializa la aplicación Predictor Electoral 2025.

        Args:
            root (tk.Tk): La ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Predictor Electoral Bolivia 2025")
        self.root.geometry("1400x950")
        self.root.option_add('*tearOff', False) # Evita que los menús se separen

        # Configuración de estilos visuales
        self.configurar_estilos()

        # Datos históricos de elecciones en Bolivia (ejemplo inicial)
        self.datos_historicos = {
            '2005': {'MAS': 53.7, 'PODEMOS': 28.6, 'UN': 7.8, 'MNR': 6.5, 'Otros': 3.4},
            '2009': {'MAS': 64.2, 'PPB-CN': 26.5, 'UN': 5.7, 'Otros': 3.6},
            '2014': {'MAS': 61.4, 'UD': 24.2, 'PDC': 9.0, 'Otros': 5.4},
            '2019': {'MAS': 47.1, 'CC': 36.5, 'FPV': 8.9, 'Otros': 7.5},
            '2020': {'MAS': 55.1, 'CC': 28.8, 'Creemos': 14.0, 'FPV': 1.6, 'Otros': 0.5}
        }

        # Encuestas 2025 (datos de ejemplo - idealmente cargados externamente)
        self.encuestas_2025 = {
            'Encuesta1': {'MAS': 48.0, 'CC': 32.0, 'Creemos': 15.0, 'FPV': 3.0, 'Nuevo': 2.0},
            'Encuesta2': {'MAS': 45.0, 'CC': 35.0, 'Creemos': 12.0, 'FPV': 5.0, 'Nuevo': 3.0},
            'Encuesta3': {'MAS': 50.0, 'CC': 30.0, 'Creemos': 13.0, 'FPV': 4.0, 'Nuevo': 3.0}
        }

        # Configuración electoral (fijas para el contexto boliviano)
        self.total_senadores = 36
        self.total_diputados = 130
        self.umbral_minimo = 0.03  # 3% mínimo para representación parlamentaria en Bolivia

        # Variables del modelo predictivo (valores iniciales)
        self.peso_historico = 0.4  # Ponderación para datos históricos
        self.peso_encuestas = 0.6  # Ponderación para encuestas actuales
        self.margen_error_prediccion = 0.03 # 3% de margen de error inicial
        self.tendencia_ajuste = "Conservar" # Tipo de ajuste de tendencia

        # Resultados de la predicción
        self.prediccion_2025 = {}
        self.senadores_2025 = {}
        self.diputados_2025 = {}
        self.prediccion_ejecutada = False # Bandera para saber si se ha corrido la predicción

        # Inicializar la interfaz gráfica del usuario
        self.inicializar_interfaz()
        # Cargar los datos iniciales en las Treeviews al inicio
        self.actualizar_tablas_datos()


    def configurar_estilos(self):
        """
        Configura los estilos visuales (temas, fuentes, colores) de la aplicación Tkinter
        para una apariencia moderna y consistente.
        """
        self.style = ttk.Style()
        self.style.theme_use('clam') # Tema 'clam' es más personalizable

        # Colores
        primary_color = '#3498db' # Azul
        secondary_color = '#2c3e50' # Gris oscuro
        accent_color = '#e74c3c' # Rojo para acentos
        bg_color = '#ecf0f1' # Gris claro para fondo
        text_color = '#2c3e50'

        # FIX: ttk.Frame cannot take 'background' directly. Configure it via style.
        # Ensure 'TFrame' style is configured before frames are created.
        self.style.configure('.', background=bg_color, foreground=text_color, font=('Arial', 10))
        self.style.configure('TFrame', background=bg_color) # This is the key fix for ttk.Frame background
        self.style.configure('TLabel', background=bg_color, foreground=text_color)
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground=primary_color)
        self.style.configure('Subheader.TLabel', font=('Arial', 12, 'bold'), foreground=secondary_color)
        self.style.configure('TButton', font=('Arial', 10, 'bold'), background=primary_color, foreground='white', padding=8)
        self.style.map('TButton', background=[('active', secondary_color)])

        self.style.configure('TNotebook', background=bg_color, borderwidth=0)
        self.style.configure('TNotebook.Tab', background=secondary_color, foreground='white', padding=[10, 5])
        self.style.map('TNotebook.Tab',
                        background=[('selected', primary_color)],
                        foreground=[('selected', 'white')])

        self.style.configure('TLabelframe', background=bg_color, foreground=primary_color)
        self.style.configure('TLabelframe.Label', font=('Arial', 12, 'bold'), foreground=primary_color)

        self.style.configure('Treeview',
                             background="#ffffff",
                             foreground="#333333",
                             fieldbackground="#ffffff",
                             font=('Arial', 9))
        self.style.map('Treeview',
                        background=[('selected', primary_color)])
        self.style.configure('Treeview.Heading',
                             font=('Arial', 10, 'bold'),
                             background=secondary_color,
                             foreground='white')


    def inicializar_interfaz(self):
        """
        Crea y organiza los componentes principales de la interfaz gráfica del usuario,
        incluyendo el Notebook con las diferentes pestañas.
        """
        # Notebook principal para organizar las secciones
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Crear y añadir las pestañas
        self.crear_pestana_introduccion()
        self.crear_pestana_datos()
        self.crear_pestana_modelo()
        self.crear_pestana_resultados()
        self.crear_pestana_exportacion()

        # Seleccionar la pestaña de introducción al inicio
        self.notebook.select(0)

        # Disable results and export tabs initially
        self.notebook.tab(self.resultados_frame, state='disabled')
        self.notebook.tab(self.exportacion_frame, state='disabled')


    def crear_pestana_introduccion(self):
        """Crea la pestaña de introducción con información general del proyecto."""
        self.intro_frame = ttk.Frame(self.notebook, padding="15 15 15 15")
        self.notebook.add(self.intro_frame, text="Introducción")

        ttk.Label(self.intro_frame, text="MODELO MATEMÁTICO PARA LAS ELECCIONES GENERALES EN BOLIVIA 2025", style='Header.TLabel', wraplength=800, justify='center').pack(pady=(20, 10))
        ttk.Label(self.intro_frame, text="Taller de Simulación de Sistemas", style='Subheader.TLabel').pack(pady=5)
        ttk.Label(self.intro_frame, text="UNIVERSIDAD MAYOR DE SAN SIMON", font=('Arial', 11, 'italic')).pack(pady=(0, 20))

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
        ttk.Label(self.intro_frame, text=intro_text, wraplength=750, justify='left', font=('Arial', 10)).pack(pady=10)


    def crear_pestana_datos(self):
        """
        Crea la pestaña para la visualización y gestión de datos históricos y de encuestas.
        Incluye gráficos de tendencias y tablas de datos.
        """
        self.datos_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.datos_frame, text="Datos Históricos y Encuestas")

        # Frame principal con scrollbar
        main_frame = ttk.Frame(self.datos_frame)
        main_frame.pack(fill='both', expand=True)

        # Removed 'background' from Canvas, it's not a ttk widget.
        # It's better to manage its background via tk.Canvas directly if needed,
        # but for scrollable_frame, it will pick up the 'TFrame' style.
        canvas = tk.Canvas(main_frame) # Removed background=self.style.lookup(...)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # FIX: The background for ttk.Frame is set via self.style.configure('TFrame', background=bg_color)
        # So, no need to pass it here. It will automatically inherit.
        scrollable_frame = ttk.Frame(canvas) # Removed background=self.style.lookup(...)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Label(scrollable_frame, text="Gestión de Datos para el Modelo Predictivo 2025",
                  style='Header.TLabel').pack(pady=(10, 20))

        # Sección de datos históricos
        self.frame_historicos = ttk.LabelFrame(scrollable_frame, text="Resultados Históricos de Elecciones en Bolivia")
        self.frame_historicos.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)
        self.tree_historicos = None # Se inicializa más tarde
        self.canvas_historicos = None # Se inicializa más tarde

        # Sección de encuestas 2025
        self.frame_encuestas = ttk.LabelFrame(scrollable_frame, text="Encuestas de Intención de Voto 2025")
        self.frame_encuestas.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)
        self.tree_encuestas = None # Se inicializa más tarde
        self.canvas_encuestas = None # Se inicializa más tarde

        # Botones para cargar nuevos datos
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Cargar Nuevas Encuestas (CSV/Excel)",
                   command=self.cargar_encuestas).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Cargar Datos Históricos (CSV/Excel)",
                   command=self.cargar_historicos).pack(side='left', padx=10)

        self.actualizar_tablas_datos() # Llenar las tablas y gráficos iniciales

    def actualizar_tablas_datos(self):
        """
        Actualiza las Treeviews y los gráficos en la pestaña de datos
        cada vez que se cargan nuevos datos.
        """
        # Limpiar widgets existentes
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        for widget in [self.tree_historicos, self.canvas_historicos,
                        self.tree_encuestas, self.canvas_encuestas]:
            if widget:
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()
                else:
                    widget.destroy()
        plt.close('all') # Cierra todas las figuras de matplotlib

        self._crear_tabla_historicos(self.frame_historicos)
        self._crear_grafico_historicos(self.frame_historicos)

        self._crear_tabla_encuestas(self.frame_encuestas)
        self._crear_grafico_encuestas(self.frame_encuestas)

    def _crear_tabla_historicos(self, parent_frame):
        """Crea la Treeview para mostrar los datos históricos."""
        if not self.datos_historicos:
            ttk.Label(parent_frame, text="No hay datos históricos cargados.").pack(pady=5)
            return

        # Obtener todos los partidos únicos para las columnas
        all_parties = sorted(list(set(p for data in self.datos_historicos.values() for p in data.keys())))
        columns = ['Año'] + all_parties

        self.tree_historicos = ttk.Treeview(parent_frame, columns=columns, show='headings', height=7)
        self.tree_historicos.pack(fill='both', expand=True, padx=10, pady=5)

        for col in columns:
            self.tree_historicos.heading(col, text=col)
            self.tree_historicos.column(col, width=80 if col == 'Año' else 100, anchor='center')

        for year, data in sorted(self.datos_historicos.items()):
            values = [year] + [f"{data.get(party, 0):.1f}%" for party in all_parties]
            self.tree_historicos.insert('', 'end', values=values)

        # Scrollbar para la tabla
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=self.tree_historicos.yview)
        vsb.pack(side='right', fill='y', in_=self.tree_historicos.winfo_parent())
        self.tree_historicos.configure(yscrollcommand=vsb.set)


    def _crear_grafico_historicos(self, parent_frame):
        """Crea el gráfico de líneas para la evolución histórica de votos."""
        if not self.datos_historicos:
            return

        fig_hist, ax_hist = plt.subplots(figsize=(10, 5))

        all_parties = sorted(list(set(p for data in self.datos_historicos.values() for p in data.keys())))
        years = sorted(list(self.datos_historicos.keys()))

        for party in all_parties:
            percentages = [self.datos_historicos.get(year, {}).get(party, 0) for year in years]
            if any(p > 0 for p in percentages): # Solo trazar si el partido tiene votos
                ax_hist.plot(years, percentages, 'o-', label=party)

        ax_hist.set_title("Evolución Histórica de Votación por Partido")
        ax_hist.set_ylabel("Porcentaje de Votos (%)")
        ax_hist.set_xlabel("Año Electoral")
        ax_hist.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
        ax_hist.grid(True, linestyle='--', alpha=0.7)
        fig_hist.tight_layout() # Ajustar el diseño para evitar que la leyenda se superponga

        self.canvas_historicos = FigureCanvasTkAgg(fig_hist, master=parent_frame)
        self.canvas_historicos.draw()
        self.canvas_historicos.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def _crear_tabla_encuestas(self, parent_frame):
        """Crea la Treeview para mostrar los datos de las encuestas 2025."""
        if not self.encuestas_2025:
            ttk.Label(parent_frame, text="No hay datos de encuestas cargados.").pack(pady=5)
            return

        # Obtener todos los partidos únicos de las encuestas
        all_parties = sorted(list(set(p for data in self.encuestas_2025.values() for p in data.keys())))
        columns = ['Encuesta'] + all_parties

        self.tree_encuestas = ttk.Treeview(parent_frame, columns=columns, show='headings', height=5)
        self.tree_encuestas.pack(fill='both', expand=True, padx=10, pady=5)

        for col in columns:
            self.tree_encuestas.heading(col, text=col)
            self.tree_encuestas.column(col, width=100, anchor='center')

        for survey_name, data in self.encuestas_2025.items():
            values = [survey_name] + [f"{data.get(party, 0):.1f}%" for party in all_parties]
            self.tree_encuestas.insert('', 'end', values=values)

        # Scrollbar para la tabla
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=self.tree_encuestas.yview)
        vsb.pack(side='right', fill='y', in_=self.tree_encuestas.winfo_parent())
        self.tree_encuestas.configure(yscrollcommand=vsb.set)

    def _crear_grafico_encuestas(self, parent_frame):
        """Crea el gráfico de barras para el promedio de las encuestas 2025."""
        if not self.encuestas_2025:
            return

        fig_enc, ax_enc = plt.subplots(figsize=(10, 5))

        # Calcular promedios de encuestas
        party_votes = defaultdict(list)
        for data in self.encuestas_2025.values():
            for party, votes in data.items():
                party_votes[party].append(votes)

        promedios = {p: np.mean(v) for p, v in party_votes.items()}
        sorted_promedios = dict(sorted(promedios.items(), key=lambda item: item[1], reverse=True))

        parties = list(sorted_promedios.keys())
        percentages = list(sorted_promedios.values())

        bars = ax_enc.bar(parties, percentages, color='#2ecc71') # Verde

        ax_enc.set_title("Promedio de Encuestas 2025")
        ax_enc.set_ylabel("Porcentaje de Votos (%)")
        ax_enc.set_xlabel("Partido Político")
        ax_enc.grid(True, linestyle='--', alpha=0.7, axis='y')
        ax_enc.set_ylim(0, 100) # Asegurar que el eje Y vaya de 0 a 100

        # Mostrar valor sobre cada barra
        for bar in bars:
            height = bar.get_height()
            ax_enc.text(bar.get_x() + bar.get_width() / 2, height,
                        f'{height:.1f}%', ha='center', va='bottom')

        fig_enc.tight_layout()

        self.canvas_encuestas = FigureCanvasTkAgg(fig_enc, master=parent_frame)
        self.canvas_encuestas.draw()
        self.canvas_encuestas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)


    def cargar_encuestas(self):
        """
        Permite al usuario cargar nuevos datos de encuestas desde un archivo CSV o Excel.
        Valida el formato del archivo y actualiza la visualización.
        """
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de encuestas",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")]
        )
        if not file_path:
            return
        try:
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            if 'Encuesta' not in df.columns:
                raise ValueError("El archivo debe contener una columna llamada 'Encuesta' para identificar las encuestas.")

            encuestas_cargadas = {}
            for idx, row in df.iterrows():
                encuesta_nombre = str(row['Encuesta'])
                # Asegurarse de que el resto de columnas son partidos y son numéricas
                # Convertir a float y manejar NaN para partidos no presentes en todas encuestas
                partido_data = {col: float(row[col]) if pd.notna(row[col]) else 0.0 for col in df.columns if col != 'Encuesta'}
                
                # Check if there are any parties in the data
                if not partido_data:
                    raise ValueError(f"La encuesta '{encuesta_nombre}' no contiene datos de partidos.")

                # Ensure percentages sum to 100 with a small tolerance
                current_sum = sum(partido_data.values())
                if abs(current_sum - 100) > 0.1: # Tolerancia de 0.1 para suma del 100%
                    # Optional: normalize if sum is slightly off
                    # partido_data = {p: (v / current_sum) * 100 for p, v in partido_data.items()}
                    messagebox.showwarning("Advertencia de Formato", f"Los porcentajes de la encuesta '{encuesta_nombre}' no suman exactamente 100%. Suma actual: {current_sum:.1f}%. Se utilizarán los valores tal cual.")
                
                encuestas_cargadas[encuesta_nombre] = partido_data

            self.encuestas_2025 = encuestas_cargadas
            messagebox.showinfo("Éxito", f"Encuestas cargadas correctamente desde '{os.path.basename(file_path)}'.")
            self.actualizar_tablas_datos() # Refrescar la visualización
        except ValueError as ve:
            messagebox.showerror("Error de Formato", str(ve))
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo: {e}")

    def cargar_historicos(self):
        """
        Permite al usuario cargar nuevos datos históricos desde un archivo CSV o Excel.
        Valida el formato del archivo y actualiza la visualización.
        """
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de datos históricos",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")]
        )
        if not file_path:
            return
        try:
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            if 'Año' not in df.columns:
                raise ValueError("El archivo debe contener una columna llamada 'Año' para identificar el año de la elección.")

            historicos_cargados = {}
            for idx, row in df.iterrows():
                # Convertir el año a string entero (por ejemplo, '2020') sin decimales
                año = str(int(float(row['Año'])))
                # Asegurarse de que el resto de columnas son partidos y son numéricas
                partido_data = {col: float(row[col]) if pd.notna(row[col]) else 0.0 for col in df.columns if col != 'Año'}
                if not partido_data:
                    raise ValueError(f"Los datos históricos del año '{año}' no contienen datos de partidos.")
                current_sum = sum(partido_data.values())
                if abs(current_sum - 100) > 0.1:
                    messagebox.showwarning("Advertencia de Formato", f"Los porcentajes del año '{año}' no suman exactamente 100%. Suma actual: {current_sum:.1f}%. Se utilizarán los valores tal cual.")
                historicos_cargados[año] = partido_data

            self.datos_historicos = historicos_cargados
            messagebox.showinfo("Éxito", f"Datos históricos cargados correctamente desde '{os.path.basename(file_path)}'.")
            self.actualizar_tablas_datos() # Refrescar la visualización
        except ValueError as ve:
            messagebox.showerror("Error de Formato", str(ve))
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo: {e}")

    def crear_pestana_modelo(self):
        """
        Crea la pestaña de configuración del modelo predictivo, permitiendo al usuario
        ajustar la ponderación de datos, el margen de error y la tendencia histórica.
        """
        self.modelo_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.modelo_frame, text="Configuración del Modelo")

        main_frame = ttk.Frame(self.modelo_frame)
        main_frame.pack(fill='both', expand=True)

        # Removed 'background' from Canvas, it's not a ttk widget.
        canvas = tk.Canvas(main_frame) # Removed background=self.style.lookup(...)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # FIX: The background for ttk.Frame is set via self.style.configure('TFrame', background=bg_color)
        scrollable_frame = ttk.Frame(canvas) # Removed background=self.style.lookup(...)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Label(scrollable_frame, text="Ajuste de Parámetros del Modelo Predictivo",
                  style='Header.TLabel').pack(pady=(10, 20))

        # Sección de ponderación de datos
        frame_ponderacion = ttk.LabelFrame(scrollable_frame, text="Ponderación de Datos de Entrada")
        frame_ponderacion.pack(fill='x', padx=10, pady=10, ipadx=5, ipady=5)

        ttk.Label(frame_ponderacion, text="Peso de datos históricos (%):", anchor='w').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.peso_hist_var = tk.DoubleVar(value=self.peso_historico * 100)
        self.peso_hist_scale = ttk.Scale(frame_ponderacion, from_=0, to=100, orient='horizontal', variable=self.peso_hist_var, command=self._update_pesos)
        self.peso_hist_scale.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.peso_hist_label = ttk.Label(frame_ponderacion, textvariable=self.peso_hist_var, width=5, anchor='e')
        self.peso_hist_label.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(frame_ponderacion, text="Peso de encuestas 2025 (%):", anchor='w').grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.peso_enc_var = tk.DoubleVar(value=self.peso_encuestas * 100)
        self.peso_enc_scale = ttk.Scale(frame_ponderacion, from_=0, to=100, orient='horizontal', variable=self.peso_enc_var, command=self._update_pesos)
        self.peso_enc_scale.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.peso_enc_label = ttk.Label(frame_ponderacion, textvariable=self.peso_enc_var, width=5, anchor='e')
        self.peso_enc_label.grid(row=1, column=2, padx=5, pady=5)

        frame_ponderacion.columnconfigure(1, weight=1) # Permite que la escala se expanda


        # Sección de variables de ajuste
        frame_ajuste = ttk.LabelFrame(scrollable_frame, text="Variables de Ajuste Fino")
        frame_ajuste.pack(fill='x', padx=10, pady=10, ipadx=5, ipady=5)

        ttk.Label(frame_ajuste, text="Margen de error de predicción (%):", anchor='w').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.margen_error_var = tk.DoubleVar(value=self.margen_error_prediccion * 100)
        self.margen_error_spinbox = ttk.Spinbox(frame_ajuste, from_=0, to=10, increment=0.1, textvariable=self.margen_error_var, width=5)
        self.margen_error_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(frame_ajuste, text="%").grid(row=0, column=2, padx=2, pady=5, sticky='w')


        ttk.Label(frame_ajuste, text="Tendencia histórica:", anchor='w').grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.tendencia_var = tk.StringVar(value=self.tendencia_ajuste)
        self.tendencia_combobox = ttk.Combobox(frame_ajuste, values=["Conservar", "Suavizar", "Acentuar"],
                                                 textvariable=self.tendencia_var, state='readonly')
        self.tendencia_combobox.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        self.tendencia_combobox.set(self.tendencia_ajuste)

        ttk.Label(frame_ajuste, text="Umbral mínimo de votos para escaños (%):", anchor='w').grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        self.umbral_minimo_var = tk.DoubleVar(value=self.umbral_minimo * 100)
        self.umbral_minimo_spinbox = ttk.Spinbox(frame_ajuste, from_=0, to=10, increment=0.1, textvariable=self.umbral_minimo_var, width=5)
        self.umbral_minimo_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(frame_ajuste, text="%").grid(row=2, column=2, padx=2, pady=5, sticky='w')

        frame_ajuste.columnconfigure(1, weight=1)


        # Botón para ejecutar predicción
        ttk.Button(scrollable_frame, text="EJECUTAR PREDICCIÓN ELECTORAL 2025",
                   command=self.ejecutar_prediccion, style='TButton').pack(pady=30, ipadx=20, ipady=10)

    def _update_pesos(self, event=None):
        """Ajusta automáticamente el peso de la otra escala para que la suma sea 100%."""
        # Determine which scale was moved
        if event == self.peso_hist_scale:
            current_hist_weight = self.peso_hist_var.get()
            self.peso_enc_var.set(100 - current_hist_weight)
        elif event == self.peso_enc_scale:
            current_enc_weight = self.peso_enc_var.get()
            self.peso_hist_var.set(100 - current_enc_weight)

        self.peso_historico = self.peso_hist_var.get() / 100
        self.peso_encuestas = self.peso_enc_var.get() / 100

    def ejecutar_prediccion(self):
        """
        Ejecuta el modelo predictivo, combinando datos históricos y de encuestas
        con los parámetros configurados por el usuario. Calcula la distribución
        de votos y escaños, y luego muestra los resultados.
        """
        try:
            if not self.datos_historicos or not self.encuestas_2025:
                messagebox.showwarning("Datos Faltantes", "Asegúrese de cargar tanto los datos históricos como las encuestas 2025 antes de ejecutar la predicción.")
                return

            self.peso_historico = self.peso_hist_var.get() / 100
            self.peso_encuestas = self.peso_enc_var.get() / 100
            self.margen_error_prediccion = self.margen_error_var.get() / 100
            self.tendencia_ajuste = self.tendencia_var.get()
            self.umbral_minimo = self.umbral_minimo_var.get() / 100

            if (self.peso_historico + self.peso_encuestas) == 0:
                messagebox.showerror("Error de Parámetros", "La suma de los pesos de datos históricos y encuestas no puede ser cero.")
                return

            # Normalizar pesos por si el usuario los manipula por separado
            total_pesos = self.peso_historico + self.peso_encuestas
            if total_pesos > 0: # Avoid division by zero if both weights are 0
                self.peso_historico /= total_pesos
                self.peso_encuestas /= total_pesos


            # Obtener datos históricos más recientes (asumiendo el último año)
            # Ensure years are integers for correct sorting if they are strings
            ultimos_años_historicos_keys = sorted([int(float(y)) for y in self.datos_historicos.keys()], reverse=True)
            if not ultimos_años_historicos_keys:
                messagebox.showerror("Error de Datos", "No hay datos históricos disponibles.")
                return
            datos_historicos_recientes = self.datos_historicos[str(ultimos_años_historicos_keys[0])]

            # Calcular promedio de encuestas 2025
            all_parties = set(datos_historicos_recientes.keys()).union(*[e.keys() for e in self.encuestas_2025.values()])
            promedios_encuestas_2025 = {}

            for p in all_parties:
                valores = [e.get(p, 0) for e in self.encuestas_2025.values()]
                promedios_encuestas_2025[p] = np.mean(valores) if valores else 0

            self.prediccion_2025 = {}

            for p in all_parties:
                hist_val = datos_historicos_recientes.get(p, 0)
                enc_val = promedios_encuestas_2025.get(p, 0)

                # Aplicar ponderación
                prediccion_base = (hist_val * self.peso_historico) + (enc_val * self.peso_encuestas)

                # Aplicar ajuste de tendencia (simplificado)
                if self.tendencia_ajuste == "Acentuar":
                    # Si un partido ha subido históricamente o en encuestas, acentuar un poco más
                    # Esto es una simplificación, un modelo real usaría regresión
                    if enc_val > hist_val:
                        prediccion_base *= 1.05 # Aumenta un 5% si está en tendencia positiva
                    elif enc_val < hist_val:
                        prediccion_base *= 0.95 # Disminuye un 5% si está en tendencia negativa
                elif self.tendencia_ajuste == "Suavizar":
                    # Disminuir la diferencia entre histórico y encuestas
                    prediccion_base = (hist_val + enc_val) / 2 # Un promedio simple para suavizar

                # Aplicar margen de error (variación aleatoria)
                variacion = np.random.uniform(-self.margen_error_prediccion, self.margen_error_prediccion)
                prediccion = max(0, prediccion_base * (1 + variacion)) # Asegurarse que no sea negativo

                self.prediccion_2025[p] = prediccion

            # Normalizar los porcentajes para que sumen exactamente 100%
            total_prediccion = sum(self.prediccion_2025.values())
            if total_prediccion > 0:
                self.prediccion_2025 = {p: (v / total_prediccion) * 100 for p, v in self.prediccion_2025.items()}
            else:
                messagebox.showwarning("Advertencia", "La predicción de votos resultó en 0 para todos los partidos. Revise sus datos y parámetros.")
                return


            # Calcular escaños
            self.calcular_escanos()

            # Marcar predicción como ejecutada y mostrar resultados
            self.prediccion_ejecutada = True
            self.notebook.tab(self.resultados_frame, state='normal')
            self.notebook.tab(self.exportacion_frame, state='normal') # Enable export tab
            self.notebook.select(self.resultados_frame)
            self.mostrar_resultados()
            messagebox.showinfo("Predicción Completa", "El modelo predictivo ha sido ejecutado exitosamente. ¡Consulte la pestaña de Resultados!")

        except ValueError as ve:
            messagebox.showerror("Error de Datos", f"Verifique la exactitud de sus datos: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error en Predicción", f"Ocurrió un error inesperado durante la predicción: {str(e)}")

    def calcular_escanos(self):
        """
        Calcula la distribución de escaños para senadores y diputados
        utilizando el método D'Hondt, considerando el umbral mínimo de votos.
        """
        # Filtrar partidos que superan el umbral mínimo de votos
        # Se convierte a un valor absoluto (0-100) para el umbral
        partidos_validos_votos = {p: v for p, v in self.prediccion_2025.items()
                                  if v >= (self.umbral_minimo * 100)}

        if not partidos_validos_votos:
            self.senadores_2025 = {}
            self.diputados_2025 = {}
            messagebox.showwarning("Advertencia", "Ningún partido alcanzó el umbral mínimo de votos para obtener escaños.")
            return

        # Normalizar los votos de los partidos válidos para que sumen 100% para el cálculo de D'Hondt
        # Esto es crucial, ya que los escaños se distribuyen solo entre los que pasan el umbral
        total_votos_validos = sum(partidos_validos_votos.values())
        if total_votos_validos == 0:
            self.senadores_2025 = {}
            self.diputados_2025 = {}
            messagebox.showwarning("Advertencia", "La suma de los votos de los partidos que superan el umbral es cero. No se pueden asignar escaños.")
            return

        votos_normalizados = {p: v / total_votos_validos for p, v in partidos_validos_votos.items()}

        # Calcular escaños para Senadores (método D'Hondt)
        self.senadores_2025 = self._calcular_dhondt(votos_normalizados, self.total_senadores)

        # Calcular escaños para Diputados (método D'Hondt)
        # Nota: En Bolivia, los diputados se asignan por circunscripción y plurinominal.
        # Una simplificación para este modelo es aplicar D'Hondt al total.
        # Un modelo más complejo requeriría datos por circunscripción.
        self.diputados_2025 = self._calcular_dhondt(votos_normalizados, self.total_diputados)

    def _calcular_dhondt(self, votos_partidos, total_escanos):
        """
        Implementa el método D'Hondt para la asignación de escaños.

        Args:
            votos_partidos (dict): Diccionario con el porcentaje de votos (0-1) por partido.
            total_escanos (int): Número total de escaños a distribuir.

        Returns:
            dict: Diccionario con el número de escaños asignados a cada partido.
        """
        escanos = defaultdict(int)
        cocientes = {}

        # Inicializar cocientes
        for partido, votos in votos_partidos.items():
            cocientes[partido] = votos / 1 # Primera división

        for _ in range(total_escanos):
            if not cocientes:
                break # No hay más partidos con cocientes para asignar escaños

            # Encontrar el partido con el cociente más alto
            ganador_escanio = max(cocientes, key=cocientes.get)
            escanos[ganador_escanio] += 1

            # Recalcular el cociente para el partido ganador
            escanos_actuales = escanos[ganador_escanio]
            votos_originales = votos_partidos[ganador_escanio]
            cocientes[ganador_escanio] = votos_originales / (escanos_actuales + 1)
        return dict(escanos)

    def crear_pestana_resultados(self):
        """
        Crea la pestaña de resultados, mostrando la predicción de votos y la
        distribución de escaños en tablas y gráficos.
        """
        self.resultados_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.resultados_frame, text="Resultados de Predicción")

        main_frame = ttk.Frame(self.resultados_frame)
        main_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Label(scrollable_frame, text="Resultados de la Predicción Electoral 2025",
                  style='Header.TLabel').pack(pady=(10, 20))

        # Sección de resultados de votos
        self.frame_votos = ttk.LabelFrame(scrollable_frame, text="Predicción de Votos 2025")
        self.frame_votos.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)
        self.tree_votos = None
        self.canvas_votos = None

        # Sección de resultados de escaños (Senadores)
        self.frame_senadores = ttk.LabelFrame(scrollable_frame, text=f"Distribución de Senadores (Total: {self.total_senadores})")
        self.frame_senadores.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)
        self.tree_senadores = None
        self.canvas_senadores = None

        # Sección de resultados de escaños (Diputados)
        self.frame_diputados = ttk.LabelFrame(scrollable_frame, text=f"Distribución de Diputados (Total: {self.total_diputados})")
        self.frame_diputados.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)
        self.tree_diputados = None
        self.canvas_diputados = None

        # Botón para refrescar resultados (útil si se cambia de pestaña sin volver a ejecutar)
        ttk.Button(scrollable_frame, text="Actualizar Vista de Resultados", command=self.mostrar_resultados).pack(pady=15)

    def mostrar_resultados(self):
        """
        Muestra los resultados de la predicción en las tablas y gráficos de la pestaña de resultados.
        Se llama después de ejecutar la predicción.
        """
        if not self.prediccion_ejecutada:
            ttk.Label(self.resultados_frame, text="Ejecute el modelo en la pestaña 'Configuración del Modelo' para ver los resultados.",
                      style='Subheader.TLabel').pack(pady=50)
            return

        # Limpiar widgets existentes
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        for widget in [self.tree_votos, self.canvas_votos,
                       self.tree_senadores, self.canvas_senadores,
                       self.tree_diputados, self.canvas_diputados]:
            if widget:
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.get_tk_widget().destroy()
                else:
                    widget.destroy()
        plt.close('all') # Cierra todas las figuras de matplotlib

        self._crear_tabla_votos(self.frame_votos)
        self._crear_grafico_votos(self.frame_votos)

        self._crear_tabla_escanos(self.frame_senadores, self.senadores_2025)
        self._crear_grafico_escanos(self.frame_senadores, self.senadores_2025, "Senadores")

        self._crear_tabla_escanos(self.frame_diputados, self.diputados_2025)
        self._crear_grafico_escanos(self.frame_diputados, self.diputados_2025, "Diputados")


    def _crear_tabla_votos(self, parent_frame):
        """Crea la Treeview para mostrar la predicción de votos."""
        if not self.prediccion_2025:
            ttk.Label(parent_frame, text="No hay predicción de votos disponible.").pack(pady=5)
            return

        columns = ['Partido', 'Porcentaje de Votos (%)']
        self.tree_votos = ttk.Treeview(parent_frame, columns=columns, show='headings', height=len(self.prediccion_2025))
        self.tree_votos.pack(fill='both', expand=True, padx=10, pady=5)

        for col in columns:
            self.tree_votos.heading(col, text=col)
            self.tree_votos.column(col, width=150, anchor='center')

        # Ordenar por porcentaje de votos
        sorted_votos = sorted(self.prediccion_2025.items(), key=lambda item: item[1], reverse=True)
        for party, percentage in sorted_votos:
            self.tree_votos.insert('', 'end', values=(party, f"{percentage:.2f}%"))

    def _crear_grafico_votos(self, parent_frame):
        """Crea el gráfico de barras para la predicción de votos."""
        if not self.prediccion_2025:
            return

        fig_votos, ax_votos = plt.subplots(figsize=(10, 5))
        parties = list(self.prediccion_2025.keys())
        percentages = list(self.prediccion_2025.values())

        # Ordenar para el gráfico
        sorted_indices = np.argsort(percentages)[::-1]
        parties = np.array(parties)[sorted_indices]
        percentages = np.array(percentages)[sorted_indices]

        bars = ax_votos.bar(parties, percentages, color='#3498db') # Azul primario

        ax_votos.set_title("Predicción de Votos para Elecciones 2025")
        ax_votos.set_ylabel("Porcentaje de Votos (%)")
        ax_votos.set_xlabel("Partido Político")
        ax_votos.grid(True, linestyle='--', alpha=0.7, axis='y')
        ax_votos.set_ylim(0, max(percentages) * 1.2 if percentages.size > 0 else 100) # Ajustar límite Y

        for bar in bars:
            height = bar.get_height()
            ax_votos.text(bar.get_x() + bar.get_width() / 2, height,
                          f'{height:.1f}%', ha='center', va='bottom')

        fig_votos.tight_layout()

        self.canvas_votos = FigureCanvasTkAgg(fig_votos, master=parent_frame)
        self.canvas_votos.draw()
        self.canvas_votos.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def _crear_tabla_escanos(self, parent_frame, escanos_data):
        """Crea una Treeview para mostrar la distribución de escaños."""
        if not escanos_data:
            ttk.Label(parent_frame, text="No se asignaron escaños para esta categoría.").pack(pady=5)
            return

        columns = ['Partido', 'Escaños']
        self.current_tree_escanos = ttk.Treeview(parent_frame, columns=columns, show='headings', height=min(10, len(escanos_data)))
        self.current_tree_escanos.pack(fill='both', expand=True, padx=10, pady=5)

        for col in columns:
            self.current_tree_escanos.heading(col, text=col)
            self.current_tree_escanos.column(col, width=150, anchor='center')

        # Ordenar por número de escaños
        sorted_escanos = sorted(escanos_data.items(), key=lambda item: item[1], reverse=True)
        for party, seats in sorted_escanos:
            self.current_tree_escanos.insert('', 'end', values=(party, seats))

    def _crear_grafico_escanos(self, parent_frame, escanos_data, title_suffix):
        """Crea el gráfico de barras para la distribución de escaños."""
        if not escanos_data:
            return

        fig_escanos, ax_escanos = plt.subplots(figsize=(10, 5))
        parties = list(escanos_data.keys())
        seats = list(escanos_data.values())

        # Ordenar para el gráfico
        sorted_indices = np.argsort(seats)[::-1]
        parties = np.array(parties)[sorted_indices]
        seats = np.array(seats)[sorted_indices]

        bars = ax_escanos.bar(parties, seats, color='#e74c3c') # Rojo acento

        ax_escanos.set_title(f"Distribución de {title_suffix} por Partido")
        ax_escanos.set_ylabel(f"Número de {title_suffix}")
        ax_escanos.set_xlabel("Partido Político")
        ax_escanos.grid(True, linestyle='--', alpha=0.7, axis='y')
        ax_escanos.set_ylim(0, max(seats) * 1.2 if seats.size > 0 else 10) # Ajustar límite Y

        for bar in bars:
            height = bar.get_height()
            ax_escanos.text(bar.get_x() + bar.get_width() / 2, height,
                            f'{int(height)}', ha='center', va='bottom')

        fig_escanos.tight_layout()

        canvas_escanos = FigureCanvasTkAgg(fig_escanos, master=parent_frame)
        canvas_escanos.draw()
        canvas_escanos.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)


    def crear_pestana_exportacion(self):
        """
        Crea la pestaña de exportación de resultados, permitiendo guardar
        los datos a Excel o generar informes PDF.
        """
        self.exportacion_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.exportacion_frame, text="Exportar Resultados")

        ttk.Label(self.exportacion_frame, text="Opciones de Exportación de Resultados",
                  style='Header.TLabel').pack(pady=(10, 20))

        export_btn_frame = ttk.Frame(self.exportacion_frame)
        export_btn_frame.pack(pady=20)

        ttk.Button(export_btn_frame, text="Exportar a Excel", command=self.exportar_a_excel,
                   style='TButton').pack(side='left', padx=15, ipadx=10, ipady=5)
        ttk.Button(export_btn_frame, text="Generar Informe PDF", command=self.generar_informe_pdf,
                   style='TButton').pack(side='left', padx=15, ipadx=10, ipady=5)

    def exportar_a_excel(self):
        """
        Exporta los datos de la predicción de votos y la distribución de escaños
        a un archivo Excel.
        """
        if not self.prediccion_ejecutada:
            messagebox.showwarning("Advertencia", "Ejecute la predicción primero para exportar resultados.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx")],
            title="Guardar resultados como Excel"
        )
        if not file_path:
            return

        try:
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                # Predicción de Votos
                df_votos = pd.DataFrame(self.prediccion_2025.items(), columns=['Partido', 'Porcentaje de Votos'])
                df_votos['Porcentaje de Votos'] = df_votos['Porcentaje de Votos'].apply(lambda x: f"{x:.2f}%")
                df_votos.to_excel(writer, sheet_name='Prediccion Votos', index=False)

                # Senadores
                df_senadores = pd.DataFrame(self.senadores_2025.items(), columns=['Partido', 'Escaños'])
                df_senadores.to_excel(writer, sheet_name='Senadores', index=False)

                # Diputados
                df_diputados = pd.DataFrame(self.diputados_2025.items(), columns=['Partido', 'Escaños'])
                df_diputados.to_excel(writer, sheet_name='Diputados', index=False)

            messagebox.showinfo("Éxito", f"Resultados exportados a '{os.path.basename(file_path)}' exitosamente.")
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo exportar a Excel: {e}")

    def generar_informe_pdf(self):
        """
        Genera un informe PDF con los resultados de la predicción, incluyendo
        tablas y gráficos.
        """
        if not self.prediccion_ejecutada:
            messagebox.showwarning("Advertencia", "Ejecute la predicción primero para generar un informe PDF.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar informe PDF"
        )
        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            # Título
            elements.append(Paragraph("Informe de Predicción Electoral Bolivia 2025", styles['h1']))
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph(f"Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 0.4 * inch))

            # Sección de Predicción de Votos
            elements.append(Paragraph("1. Predicción de Votos por Partido", styles['h2']))
            elements.append(Spacer(1, 0.1 * inch))
            data_votos = [['Partido', 'Porcentaje de Votos (%)']]
            sorted_votos = sorted(self.prediccion_2025.items(), key=lambda item: item[1], reverse=True)
            for party, percentage in sorted_votos:
                data_votos.append([party, f"{percentage:.2f}%"])
            table_votos = Table(data_votos)
            table_votos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table_votos)
            elements.append(Spacer(1, 0.2 * inch))

            # Gráfico de Votos
            fig_votos, ax_votos = plt.subplots(figsize=(8, 4))
            parties = list(self.prediccion_2025.keys())
            percentages = list(self.prediccion_2025.values())
            sorted_indices = np.argsort(percentages)[::-1]
            parties = np.array(parties)[sorted_indices]
            percentages = np.array(percentages)[sorted_indices]
            ax_votos.bar(parties, percentages, color='#3498db')
            ax_votos.set_title("Predicción de Votos para Elecciones 2025")
            ax_votos.set_ylabel("Porcentaje de Votos (%)")
            ax_votos.set_xlabel("Partido Político")
            ax_votos.grid(True, linestyle='--', alpha=0.7, axis='y')
            ax_votos.set_ylim(0, max(percentages) * 1.2 if percentages.size > 0 else 100)
            fig_votos.tight_layout()
            
            # Save plot to a temporary image file
            img_path_votos = "temp_votos_prediccion.png"
            fig_votos.savefig(img_path_votos, dpi=100)
            plt.close(fig_votos) # Close the plot to free memory

            elements.append(Image(img_path_votos, width=6 * inch, height=3 * inch))
            elements.append(Spacer(1, 0.4 * inch))

            # Sección de Distribución de Senadores
            elements.append(Paragraph(f"2. Distribución de Senadores (Total: {self.total_senadores})", styles['h2']))
            elements.append(Spacer(1, 0.1 * inch))
            data_senadores = [['Partido', 'Escaños']]
            sorted_senadores = sorted(self.senadores_2025.items(), key=lambda item: item[1], reverse=True)
            for party, seats in sorted_senadores:
                data_senadores.append([party, seats])
            table_senadores = Table(data_senadores)
            table_senadores.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table_senadores)
            elements.append(Spacer(1, 0.2 * inch))

            # Gráfico de Senadores
            fig_senadores, ax_senadores = plt.subplots(figsize=(8, 4))
            parties_sen = list(self.senadores_2025.keys())
            seats_sen = list(self.senadores_2025.values())
            sorted_indices_sen = np.argsort(seats_sen)[::-1]
            parties_sen = np.array(parties_sen)[sorted_indices_sen]
            seats_sen = np.array(seats_sen)[sorted_indices_sen]
            ax_senadores.bar(parties_sen, seats_sen, color='#e74c3c')
            ax_senadores.set_title(f"Distribución de Senadores por Partido")
            ax_senadores.set_ylabel("Número de Senadores")
            ax_senadores.set_xlabel("Partido Político")
            ax_senadores.grid(True, linestyle='--', alpha=0.7, axis='y')
            ax_senadores.set_ylim(0, max(seats_sen) * 1.2 if seats_sen.size > 0 else 10)
            fig_senadores.tight_layout()

            img_path_senadores = "temp_senadores_distribucion.png"
            fig_senadores.savefig(img_path_senadores, dpi=100)
            plt.close(fig_senadores)

            elements.append(Image(img_path_senadores, width=6 * inch, height=3 * inch))
            elements.append(Spacer(1, 0.4 * inch))

            # Sección de Distribución de Diputados
            elements.append(Paragraph(f"3. Distribución de Diputados (Total: {self.total_diputados})", styles['h2']))
            elements.append(Spacer(1, 0.1 * inch))
            data_diputados = [['Partido', 'Escaños']]
            sorted_diputados = sorted(self.diputados_2025.items(), key=lambda item: item[1], reverse=True)
            for party, seats in sorted_diputados:
                data_diputados.append([party, seats])
            table_diputados = Table(data_diputados)
            table_diputados.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table_diputados)
            elements.append(Spacer(1, 0.2 * inch))

            # Gráfico de Diputados
            fig_diputados, ax_diputados = plt.subplots(figsize=(8, 4))
            parties_dip = list(self.diputados_2025.keys())
            seats_dip = list(self.diputados_2025.values())
            sorted_indices_dip = np.argsort(seats_dip)[::-1]
            parties_dip = np.array(parties_dip)[sorted_indices_dip]
            seats_dip = np.array(seats_dip)[sorted_indices_dip]
            ax_diputados.bar(parties_dip, seats_dip, color='#e74c3c')
            ax_diputados.set_title(f"Distribución de Diputados por Partido")
            ax_diputados.set_ylabel("Número de Diputados")
            ax_diputados.set_xlabel("Partido Político")
            ax_diputados.grid(True, linestyle='--', alpha=0.7, axis='y')
            ax_diputados.set_ylim(0, max(seats_dip) * 1.2 if seats_dip.size > 0 else 10)
            fig_diputados.tight_layout()

            img_path_diputados = "temp_diputados_distribucion.png"
            fig_diputados.savefig(img_path_diputados, dpi=100)
            plt.close(fig_diputados)

            elements.append(Image(img_path_diputados, width=6 * inch, height=3 * inch))
            elements.append(Spacer(1, 0.4 * inch))


            doc.build(elements)
            messagebox.showinfo("Éxito", f"Informe PDF generado en '{os.path.basename(file_path)}' exitosamente.")

        except Exception as e:
            messagebox.showerror("Error de PDF", f"No se pudo generar el informe PDF: {e}")
        finally:
            # Clean up temporary image files
            for temp_img in [img_path_votos, img_path_senadores, img_path_diputados]:
                if os.path.exists(temp_img):
                    os.remove(temp_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = PredictorElectoral2025(root)
    root.mainloop()