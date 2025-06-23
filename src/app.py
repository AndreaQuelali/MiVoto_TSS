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
from collections import defaultdict

class PredictorElectoral2025:
    """
    Aplicación de Escritorio para la Predicción Electoral en Bolivia 2025.
    Incluye implementación de segunda vuelta según Ley 026.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Predictor Electoral Bolivia 2025")
        self.root.geometry("1400x950")
        self.root.option_add('*tearOff', False)

        # Configuración de estilos visuales
        self.configurar_estilos()

        # Datos históricos de elecciones en Bolivia
        self.datos_historicos = {
            '2005': {'MAS': 53.7, 'PODEMOS': 28.6, 'UN': 7.8, 'MNR': 6.5, 'Otros': 3.4},
            '2009': {'MAS': 64.2, 'PPB-CN': 26.5, 'UN': 5.7, 'Otros': 3.6},
            '2014': {'MAS': 61.4, 'UD': 24.2, 'PDC': 9.0, 'Otros': 5.4},
            '2019': {'MAS': 47.1, 'CC': 36.5, 'FPV': 8.9, 'Otros': 7.5},
            '2020': {'MAS': 55.1, 'CC': 28.8, 'Creemos': 14.0, 'FPV': 1.6, 'Otros': 0.5}
        }

        # Encuestas 2025
        self.encuestas_2025 = {
            'Encuesta1': {'MAS': 48.0, 'CC': 32.0, 'Creemos': 15.0, 'FPV': 3.0, 'Nuevo': 2.0},
            'Encuesta2': {'MAS': 45.0, 'CC': 35.0, 'Creemos': 12.0, 'FPV': 5.0, 'Nuevo': 3.0},
            'Encuesta3': {'MAS': 50.0, 'CC': 30.0, 'Creemos': 13.0, 'FPV': 4.0, 'Nuevo': 3.0}
        }

        # Configuración electoral
        self.total_senadores = 36
        self.total_diputados = 130
        self.umbral_minimo = 0.03

        # Variables del modelo predictivo
        self.peso_historico = 0.4
        self.peso_encuestas = 0.6
        self.margen_error_prediccion = 0.03
        self.tendencia_ajuste = "Conservar"

        # Resultados de la predicción
        self.prediccion_2025 = {}
        self.senadores_2025 = {}
        self.diputados_2025 = {}
        self.prediccion_ejecutada = False
        
        # Variables para segunda vuelta
        self.segunda_vuelta = False
        self.candidatos_segunda_vuelta = []
        self.prediccion_segunda_vuelta = {}

        # Inicializar la interfaz gráfica
        self.inicializar_interfaz()
        self.actualizar_tablas_datos()

    def configurar_estilos(self):
        """Configura los estilos visuales de la aplicación."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        primary_color = '#3498db'
        secondary_color = '#2c3e50'
        accent_color = '#e74c3c'
        bg_color = '#ecf0f1'
        text_color = '#2c3e50'

        self.style.configure('.', background=bg_color, foreground=text_color, font=('Arial', 10))
        self.style.configure('TFrame', background=bg_color)
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

    def verificar_segunda_vuelta(self, votos):
        """
        Verifica si se requiere segunda vuelta según la Ley 026 de Bolivia.
        
        Args:
            votos (dict): Diccionario con los porcentajes de votos por partido
            
        Returns:
            bool: True si se requiere segunda vuelta, False si hay ganador en primera vuelta
            list: Lista con los dos partidos que pasan a segunda vuelta (si aplica)
        """
        votos_ordenados = sorted(votos.items(), key=lambda item: item[1], reverse=True)
        
        # Caso 1: Mayoría absoluta (50% + 1)
        if votos_ordenados[0][1] > 50.0:
            return False, []
            
        # Caso 2: 40% con 10% de diferencia
        if len(votos_ordenados) >= 2:
            if votos_ordenados[0][1] >= 40.0 and (votos_ordenados[0][1] - votos_ordenados[1][1]) >= 10.0:
                return False, []
        
        # Si no cumple ninguno de los casos anteriores, hay segunda vuelta
        return True, [votos_ordenados[0][0], votos_ordenados[1][0]]

    def simular_segunda_vuelta(self):
        """
        Simula los resultados de la segunda vuelta electoral.
        """
        if not self.segunda_vuelta or len(self.candidatos_segunda_vuelta) < 2:
            return
            
        # Redistribuir votos considerando solo los dos partidos principales
        total_votos = sum(self.prediccion_2025.values())
        votos_primer_lugar = self.prediccion_2025[self.candidatos_segunda_vuelta[0]]
        votos_segundo_lugar = self.prediccion_2025[self.candidatos_segunda_vuelta[1]]
        
        # Calcular porcentaje de votos no asignados a estos dos partidos
        otros_votos = total_votos - votos_primer_lugar - votos_segundo_lugar
        
        # Simular redistribución (70% al primero, 30% al segundo como ejemplo)
        votos_primer_lugar += otros_votos * 0.7
        votos_segundo_lugar += otros_votos * 0.3
        
        # Actualizar predicción para mostrar solo los dos candidatos
        self.prediccion_segunda_vuelta = {
            self.candidatos_segunda_vuelta[0]: votos_primer_lugar,
            self.candidatos_segunda_vuelta[1]: votos_segundo_lugar
        }
        
        # Determinar ganador
        if votos_primer_lugar > votos_segundo_lugar:
            ganador = self.candidatos_segunda_vuelta[0]
        else:
            ganador = self.candidatos_segunda_vuelta[1]
            
        messagebox.showinfo("Resultado Segunda Vuelta", 
                          f"Ganador de la segunda vuelta: {ganador}\n\n"
                          f"{self.candidatos_segunda_vuelta[0]}: {votos_primer_lugar:.1f}%\n"
                          f"{self.candidatos_segunda_vuelta[1]}: {votos_segundo_lugar:.1f}%")

    def inicializar_interfaz(self):
        """Crea y organiza los componentes principales de la interfaz gráfica."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.crear_pestana_introduccion()
        self.crear_pestana_datos()
        self.crear_pestana_modelo()
        self.crear_pestana_resultados()
        self.crear_pestana_exportacion()

        self.notebook.select(0)
        self.notebook.tab(self.resultados_frame, state='disabled')
        self.notebook.tab(self.exportacion_frame, state='disabled')

    def crear_pestana_introduccion(self):
        """Crea la pestaña de introducción con información general."""
        self.intro_frame = ttk.Frame(self.notebook, padding="15 15 15 15")
        self.notebook.add(self.intro_frame, text="Introducción")

        ttk.Label(self.intro_frame, 
                 text="MODELO MATEMÁTICO PARA LAS ELECCIONES GENERALES EN BOLIVIA 2025", 
                 style='Header.TLabel', wraplength=800, justify='center').pack(pady=(20, 10))
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

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

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
        self.tree_historicos = None
        self.canvas_historicos = None

        # Sección de encuestas 2025
        self.frame_encuestas = ttk.LabelFrame(scrollable_frame, text="Encuestas de Intención de Voto 2025")
        self.frame_encuestas.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)
        self.tree_encuestas = None
        self.canvas_encuestas = None

        # Botones para cargar nuevos datos
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Cargar Nuevas Encuestas (CSV/Excel)",
                   command=self.cargar_encuestas).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Cargar Datos Históricos (CSV/Excel)",
                   command=self.cargar_historicos).pack(side='left', padx=10)

        self.actualizar_tablas_datos()

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
        plt.close('all')

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
            if any(p > 0 for p in percentages):
                ax_hist.plot(years, percentages, 'o-', label=party)

        ax_hist.set_title("Evolución Histórica de Votación por Partido")
        ax_hist.set_ylabel("Porcentaje de Votos (%)")
        ax_hist.set_xlabel("Año Electoral")
        ax_hist.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
        ax_hist.grid(True, linestyle='--', alpha=0.7)
        fig_hist.tight_layout()

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

        bars = ax_enc.bar(parties, percentages, color='#2ecc71')

        ax_enc.set_title("Promedio de Encuestas 2025")
        ax_enc.set_ylabel("Porcentaje de Votos (%)")
        ax_enc.set_xlabel("Partido Político")
        ax_enc.grid(True, linestyle='--', alpha=0.7, axis='y')
        ax_enc.set_ylim(0, 100)

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
                partido_data = {col: float(row[col]) if pd.notna(row[col]) else 0.0 for col in df.columns if col != 'Encuesta'}
                
                if not partido_data:
                    raise ValueError(f"La encuesta '{encuesta_nombre}' no contiene datos de partidos.")

                current_sum = sum(partido_data.values())
                if abs(current_sum - 100) > 0.1:
                    messagebox.showwarning("Advertencia de Formato", f"Los porcentajes de la encuesta '{encuesta_nombre}' no suman exactamente 100%. Suma actual: {current_sum:.1f}%. Se utilizarán los valores tal cual.")
                
                encuestas_cargadas[encuesta_nombre] = partido_data

            self.encuestas_2025 = encuestas_cargadas
            messagebox.showinfo("Éxito", f"Encuestas cargadas correctamente desde '{os.path.basename(file_path)}'.")
            self.actualizar_tablas_datos()
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
                año = str(int(float(row['Año'])))
                partido_data = {col: float(row[col]) if pd.notna(row[col]) else 0.0 for col in df.columns if col != 'Año'}
                if not partido_data:
                    raise ValueError(f"Los datos históricos del año '{año}' no contienen datos de partidos.")
                current_sum = sum(partido_data.values())
                if abs(current_sum - 100) > 0.1:
                    messagebox.showwarning("Advertencia de Formato", f"Los porcentajes del año '{año}' no suman exactamente 100%. Suma actual: {current_sum:.1f}%. Se utilizarán los valores tal cual.")
                historicos_cargados[año] = partido_data

            self.datos_historicos = historicos_cargados
            messagebox.showinfo("Éxito", f"Datos históricos cargados correctamente desde '{os.path.basename(file_path)}'.")
            self.actualizar_tablas_datos()
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

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

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

        frame_ponderacion.columnconfigure(1, weight=1)

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
        Ejecuta el modelo predictivo, incluyendo verificación de segunda vuelta.
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

            total_pesos = self.peso_historico + self.peso_encuestas
            if total_pesos > 0:
                self.peso_historico /= total_pesos
                self.peso_encuestas /= total_pesos

            ultimos_años_historicos_keys = sorted([int(float(y)) for y in self.datos_historicos.keys()], reverse=True)
            if not ultimos_años_historicos_keys:
                messagebox.showerror("Error de Datos", "No hay datos históricos disponibles.")
                return
            datos_historicos_recientes = self.datos_historicos[str(ultimos_años_historicos_keys[0])]

            all_parties = set(datos_historicos_recientes.keys()).union(*[e.keys() for e in self.encuestas_2025.values()])
            promedios_encuestas_2025 = {}

            for p in all_parties:
                valores = [e.get(p, 0) for e in self.encuestas_2025.values()]
                promedios_encuestas_2025[p] = np.mean(valores) if valores else 0

            self.prediccion_2025 = {}

            for p in all_parties:
                hist_val = datos_historicos_recientes.get(p, 0)
                enc_val = promedios_encuestas_2025.get(p, 0)

                prediccion_base = (hist_val * self.peso_historico) + (enc_val * self.peso_encuestas)

                if self.tendencia_ajuste == "Acentuar":
                    if enc_val > hist_val:
                        prediccion_base *= 1.05
                    elif enc_val < hist_val:
                        prediccion_base *= 0.95
                elif self.tendencia_ajuste == "Suavizar":
                    prediccion_base = (hist_val + enc_val) / 2

                variacion = np.random.uniform(-self.margen_error_prediccion, self.margen_error_prediccion)
                prediccion = max(0, prediccion_base * (1 + variacion))
                self.prediccion_2025[p] = prediccion

            total_prediccion = sum(self.prediccion_2025.values())
            if total_prediccion > 0:
                self.prediccion_2025 = {p: (v / total_prediccion) * 100 for p, v in self.prediccion_2025.items()}
            else:
                messagebox.showwarning("Advertencia", "La predicción de votos resultó en 0 para todos los partidos. Revise sus datos y parámetros.")
                return

            # Verificar si se requiere segunda vuelta
            self.segunda_vuelta, self.candidatos_segunda_vuelta = self.verificar_segunda_vuelta(self.prediccion_2025)
            
            if self.segunda_vuelta:
                messagebox.showinfo("Segunda Vuelta", 
                                  f"Se requerirá segunda vuelta entre {self.candidatos_segunda_vuelta[0]} y {self.candidatos_segunda_vuelta[1]}")

            # Calcular escaños
            self.calcular_escanos()

            self.prediccion_ejecutada = True
            self.notebook.tab(self.resultados_frame, state='normal')
            self.notebook.tab(self.exportacion_frame, state='normal')
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
        partidos_validos_votos = {p: v for p, v in self.prediccion_2025.items()
                                  if v >= (self.umbral_minimo * 100)}

        if not partidos_validos_votos:
            self.senadores_2025 = {}
            self.diputados_2025 = {}
            messagebox.showwarning("Advertencia", "Ningún partido alcanzó el umbral mínimo de votos para obtener escaños.")
            return

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
        self.diputados_2025 = self._calcular_dhondt(votos_normalizados, self.total_diputados)

    def _calcular_dhondt(self, votos_partidos, total_escanos):
        """
        Implementa el método D'Hondt para la asignación de escaños.
        """
        escanos = defaultdict(int)
        cocientes = {}

        for partido, votos in votos_partidos.items():
            cocientes[partido] = votos / 1

        for _ in range(total_escanos):
            if not cocientes:
                break

            ganador_escanio = max(cocientes, key=cocientes.get)
            escanos[ganador_escanio] += 1

            escanos_actuales = escanos[ganador_escanio]
            votos_originales = votos_partidos[ganador_escanio]
            cocientes[ganador_escanio] = votos_originales / (escanos_actuales + 1)
        return dict(escanos)

    def crear_pestana_resultados(self):
        """
        Crea la pestaña de resultados con opción para segunda vuelta.
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

        # Botón para simular segunda vuelta si aplica
        self.btn_segunda_vuelta = ttk.Button(scrollable_frame, 
                                           text="Simular Segunda Vuelta", 
                                           command=self.simular_segunda_vuelta,
                                           state='disabled')
        self.btn_segunda_vuelta.pack(pady=10)

        # Botón para refrescar resultados
        ttk.Button(scrollable_frame, text="Actualizar Vista de Resultados", command=self.mostrar_resultados).pack(pady=15)

    def mostrar_resultados(self):
        """Muestra los resultados de la predicción, incluyendo opción para segunda vuelta."""
        if not self.prediccion_ejecutada:
            ttk.Label(self.resultados_frame, text="Ejecute el modelo en la pestaña 'Configuración del Modelo' para ver los resultados.",
                     style='Subheader.TLabel').pack(pady=50)
            return

        # Actualizar estado del botón de segunda vuelta
        if self.segunda_vuelta:
            self.btn_segunda_vuelta.config(state='normal')
        else:
            self.btn_segunda_vuelta.config(state='disabled')

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
        plt.close('all')

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

        sorted_indices = np.argsort(percentages)[::-1]
        parties = np.array(parties)[sorted_indices]
        percentages = np.array(percentages)[sorted_indices]

        bars = ax_votos.bar(parties, percentages, color='#3498db')

        ax_votos.set_title("Predicción de Votos para Elecciones 2025")
        ax_votos.set_ylabel("Porcentaje de Votos (%)")
        ax_votos.set_xlabel("Partido Político")
        ax_votos.grid(True, linestyle='--', alpha=0.7, axis='y')
        ax_votos.set_ylim(0, max(percentages) * 1.2 if percentages.size > 0 else 100)

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

        sorted_indices = np.argsort(seats)[::-1]
        parties = np.array(parties)[sorted_indices]
        seats = np.array(seats)[sorted_indices]

        bars = ax_escanos.bar(parties, seats, color='#e74c3c')

        ax_escanos.set_title(f"Distribución de {title_suffix} por Partido")
        ax_escanos.set_ylabel(f"Número de {title_suffix}")
        ax_escanos.set_xlabel("Partido Político")
        ax_escanos.grid(True, linestyle='--', alpha=0.7, axis='y')
        ax_escanos.set_ylim(0, max(seats) * 1.2 if seats.size > 0 else 10)

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
            
            img_path_votos = "temp_votos_prediccion.png"
            fig_votos.savefig(img_path_votos, dpi=100)
            plt.close(fig_votos)

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