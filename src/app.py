import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict

class PredictorElectoral2025:
    def __init__(self, root):
        self.root = root
        self.root.title("Predictor Electoral Bolivia 2025")
        self.root.geometry("1200x900")
        
        # Configuración de estilos
        self.configurar_estilos()
        
        # Datos históricos de elecciones en Bolivia
        self.datos_historicos = {
            '2005': {'MAS': 53.7, 'PODEMOS': 28.6, 'UN': 7.8, 'MNR': 6.5, 'Otros': 3.4},
            '2009': {'MAS': 64.2, 'PPB-CN': 26.5, 'UN': 5.7, 'Otros': 3.6},
            '2014': {'MAS': 61.4, 'UD': 24.2, 'PDC': 9.0, 'Otros': 5.4},
            '2019': {'MAS': 47.1, 'CC': 36.5, 'FPV': 8.9, 'Otros': 7.5},
            '2020': {'MAS': 55.1, 'CC': 28.8, 'Creemos': 14.0, 'FPV': 1.6, 'Otros': 0.5}
        }
        
        # Encuestas 2025 (datos de ejemplo - deberías cargar datos reales)
        self.encuestas_2025 = {
            'Encuesta1': {'MAS': 48.0, 'CC': 32.0, 'Creemos': 15.0, 'FPV': 3.0, 'Nuevo': 2.0},
            'Encuesta2': {'MAS': 45.0, 'CC': 35.0, 'Creemos': 12.0, 'FPV': 5.0, 'Nuevo': 3.0},
            'Encuesta3': {'MAS': 50.0, 'CC': 30.0, 'Creemos': 13.0, 'FPV': 4.0, 'Nuevo': 3.0}
        }
        
        # Configuración electoral
        self.total_senadores = 36
        self.total_diputados = 130
        self.umbral_minimo = 0.03  # 3% mínimo para representación
        
        # Variables del modelo
        self.peso_historico = 0.4  # Peso de datos históricos
        self.peso_encuestas = 0.6  # Peso de encuestas actuales
        
        # Inicializar interfaz
        self.inicializar_interfaz()
    
    def configurar_estilos(self):
        """Configura los estilos visuales de la aplicación"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='#f0f0f0', foreground='#333333')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#1a5276')
        self.style.configure('Subheader.TLabel', font=('Arial', 12, 'bold'), foreground='#2874a6')
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TNotebook.Tab', background='#d5d8dc', padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#3498db')], 
                      foreground=[('selected', 'white')])
    
    def inicializar_interfaz(self):
        """Inicializa los componentes de la interfaz gráfica"""
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_pestana_datos()
        self.crear_pestana_modelo()
        self.crear_pestana_resultados()
        self.crear_pestana_exportacion()
        
        # Seleccionar pestaña inicial
        self.notebook.select(0)
    
    def crear_pestana_datos(self):
        """Crea la pestaña de visualización de datos"""
        self.datos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.datos_frame, text="Datos Históricos y Encuestas")
        
        # Frame principal con scroll
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
        
        # Contenido
        ttk.Label(scrollable_frame, text="Datos para el Modelo Predictivo 2025", 
                 style='Header.TLabel').pack(pady=(10, 20))
        
        # Sección de datos históricos
        self.crear_seccion_historicos(scrollable_frame)
        
        # Sección de encuestas 2025
        self.crear_seccion_encuestas(scrollable_frame)
        
        # Botones para cargar nuevos datos
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Cargar Nuevas Encuestas", 
                  command=self.cargar_encuestas).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Cargar Datos Históricos", 
                  command=self.cargar_historicos).pack(side='left', padx=10)
    
    def crear_seccion_historicos(self, parent):
        """Crea la sección de visualización de datos históricos"""
        frame = ttk.LabelFrame(parent, text="Resultados Históricos de Elecciones en Bolivia")
        frame.pack(fill='x', padx=10, pady=5)
        
        # Crear gráfico de tendencias históricas
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Obtener todos los partidos únicos a través de los años
        todos_partidos = set()
        for datos in self.datos_historicos.values():
            todos_partidos.update(datos.keys())
        
        # Para cada partido, trazar su evolución
        for partido in todos_partidos:
            años = []
            porcentajes = []
            
            for año, datos in sorted(self.datos_historicos.items()):
                if partido in datos:
                    años.append(año)
                    porcentajes.append(datos[partido])
            
            if años:  # Solo si hay datos para este partido
                ax.plot(años, porcentajes, 'o-', label=partido)
        
        # Configurar gráfico
        ax.set_title("Evolución Histórica de Votación por Partido")
        ax.set_ylabel("Porcentaje de Votos (%)")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='x', padx=10, pady=10)
    
    def crear_seccion_encuestas(self, parent):
        """Crea la sección de visualización de encuestas 2025"""
        frame = ttk.LabelFrame(parent, text="Encuestas de Intención de Voto 2025")
        frame.pack(fill='x', padx=10, pady=5)
        
        # Crear tabla con datos de encuestas
        columns = ['Encuesta'] + list(next(iter(self.encuestas_2025.values())).keys())
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=5)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        for encuesta, datos in self.encuestas_2025.items():
            row = [encuesta] + [f"{v:.1f}%" for v in datos.values()]
            tree.insert('', 'end', values=row)
        
        tree.pack(fill='x', padx=10, pady=10)
        
        # Gráfico de promedio de encuestas
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Calcular promedios
        partidos = list(next(iter(self.encuestas_2025.values())).keys())
        promedios = {p: np.mean([e[p] for e in self.encuestas_2025.values()]) for p in partidos}
        
        ax.bar(promedios.keys(), promedios.values())
        ax.set_title("Promedio de Encuestas 2025")
        ax.set_ylabel("Porcentaje de Votos (%)")
        ax.grid(True, linestyle='--', alpha=0.7)
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='x', padx=10, pady=10)
    
    def cargar_encuestas(self):
        """Permite cargar nuevas encuestas al sistema desde archivo CSV o Excel"""
        from tkinter import filedialog
        import os
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de encuestas",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")]
        )
        if not file_path:
            return
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            # Validar formato
            if 'Encuesta' not in df.columns:
                raise ValueError("El archivo debe tener una columna llamada 'Encuesta'.")
            partidos = [col for col in df.columns if col != 'Encuesta']
            encuestas = {}
            for _, row in df.iterrows():
                nombre = str(row['Encuesta'])
                datos = {p: float(row[p]) for p in partidos}
                encuestas[nombre] = datos
            self.encuestas_2025 = encuestas
            messagebox.showinfo("Éxito", "Encuestas cargadas correctamente.")
            # Refrescar visualización
            self.crear_seccion_encuestas(self.datos_frame.winfo_children()[0].winfo_children()[0].winfo_children()[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    
    def cargar_historicos(self):
        """Permite cargar datos históricos desde archivo CSV o Excel"""
        from tkinter import filedialog
        import os
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de datos históricos",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")]
        )
        if not file_path:
            return
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            # Validar formato
            if 'Año' not in df.columns:
                raise ValueError("El archivo debe tener una columna llamada 'Año'.")
            partidos = [col for col in df.columns if col != 'Año']
            historicos = {}
            for _, row in df.iterrows():
                año = str(row['Año'])
                datos = {p: float(row[p]) for p in partidos}
                historicos[año] = datos
            self.datos_historicos = historicos
            messagebox.showinfo("Éxito", "Datos históricos cargados correctamente.")
            # Refrescar visualización
            self.crear_seccion_historicos(self.datos_frame.winfo_children()[0].winfo_children()[0].winfo_children()[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    
    def crear_pestana_modelo(self):
        """Crea la pestaña de configuración del modelo predictivo"""
        self.modelo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.modelo_frame, text="Configuración del Modelo")
        
        # Frame principal con scroll
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
        
        # Contenido
        ttk.Label(scrollable_frame, text="Configuración del Modelo Predictivo", 
                 style='Header.TLabel').pack(pady=(10, 20))
        
        # Sección de ponderación de datos
        frame_ponderacion = ttk.LabelFrame(scrollable_frame, text="Ponderación de Datos")
        frame_ponderacion.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_ponderacion, text="Peso de datos históricos:").grid(row=0, column=0, padx=5, pady=5)
        self.peso_hist = ttk.Scale(frame_ponderacion, from_=0, to=100, orient='horizontal')
        self.peso_hist.set(self.peso_historico * 100)
        self.peso_hist.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_ponderacion, text="Peso de encuestas 2025:").grid(row=1, column=0, padx=5, pady=5)
        self.peso_enc = ttk.Scale(frame_ponderacion, from_=0, to=100, orient='horizontal')
        self.peso_enc.set(self.peso_encuestas * 100)
        self.peso_enc.grid(row=1, column=1, padx=5, pady=5)
        
        # Sección de variables de ajuste
        frame_ajuste = ttk.LabelFrame(scrollable_frame, text="Variables de Ajuste")
        frame_ajuste.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_ajuste, text="Margen de error:").grid(row=0, column=0, padx=5, pady=5)
        self.margen_error = ttk.Spinbox(frame_ajuste, from_=0, to=10, increment=0.5)
        self.margen_error.set(3.0)
        self.margen_error.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_ajuste, text="Tendencia histórica:").grid(row=1, column=0, padx=5, pady=5)
        self.tendencia = ttk.Combobox(frame_ajuste, values=["Conservar", "Suavizar", "Acentuar"])
        self.tendencia.set("Conservar")
        self.tendencia.grid(row=1, column=1, padx=5, pady=5)
        
        # Botón para ejecutar predicción
        ttk.Button(scrollable_frame, text="Ejecutar Predicción 2025", 
                  command=self.ejecutar_prediccion).pack(pady=20)
    
    def ejecutar_prediccion(self):
        """Ejecuta el modelo predictivo con los parámetros configurados"""
        try:
            # Obtener parámetros
            self.peso_historico = self.peso_hist.get() / 100
            self.peso_encuestas = self.peso_enc.get() / 100
            margen_error = float(self.margen_error.get()) / 100
            
            # Validar pesos
            if (self.peso_historico + self.peso_encuestas) == 0:
                raise ValueError("La suma de pesos no puede ser cero")
            
            # Normalizar pesos
            total = self.peso_historico + self.peso_encuestas
            self.peso_historico /= total
            self.peso_encuestas /= total
            
            # Obtener datos históricos más recientes (2020)
            datos_2020 = self.datos_historicos['2020']
            
            # Calcular promedio de encuestas 2025
            partidos = set(datos_2020.keys()).union(*[e.keys() for e in self.encuestas_2025.values()])
            promedios_2025 = {}
            
            for p in partidos:
                valores = [e.get(p, 0) for e in self.encuestas_2025.values()]
                promedios_2025[p] = np.mean(valores) if valores else 0
            
            # Aplicar modelo predictivo
            self.prediccion_2025 = {}
            
            for p in partidos:
                hist = datos_2020.get(p, 0)
                enc = promedios_2025.get(p, 0)
                
                # Aplicar ponderación
                prediccion = (hist * self.peso_historico) + (enc * self.peso_encuestas)
                
                # Aplicar margen de error (variación aleatoria)
                variacion = np.random.uniform(-margen_error, margen_error)
                prediccion = max(0, prediccion * (1 + variacion))
                
                self.prediccion_2025[p] = prediccion
            
            # Normalizar para que sumen 100%
            total = sum(self.prediccion_2025.values())
            self.prediccion_2025 = {p: (v/total)*100 for p, v in self.prediccion_2025.items()}
            
            # Calcular escaños
            self.calcular_escanos()
            
            # Mostrar resultados
            self.notebook.tab(self.resultados_frame, state='normal')
            self.notebook.select(self.resultados_frame)
            self.mostrar_resultados()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar la predicción: {str(e)}")
    
    def calcular_escanos(self):
        """Calcula la distribución de escaños usando el método D'Hondt"""
        # Filtrar partidos que superan el umbral
        partidos_validos = {p: v for p, v in self.prediccion_2025.items() 
                          if v >= (self.umbral_minimo * 100)}
        
        # Asignar escaños para senadores
        self.senadores_2025 = self.aplicar_metodo_dhondt(partidos_validos, self.total_senadores)
        
        # Asignar escaños para diputados
        self.diputados_2025 = self.aplicar_metodo_dhondt(partidos_validos, self.total_diputados)
    
    def aplicar_metodo_dhondt(self, votos, total_escanos):
        """Aplica el método D'Hondt para asignar escaños"""
        if not votos:
            return {}

        asignaciones = {p: 0 for p in votos}
        cocientes = {p: v for p, v in votos.items()}  # Cocientes iniciales (V/1)

        for _ in range(total_escanos):
            # Encontrar partido con mayor cociente
            partido_ganador = max(cocientes.items(), key=lambda x: x[1])[0]

            # Asignar escaño
            asignaciones[partido_ganador] += 1

            # Actualizar cociente para el próximo escaño
            cocientes[partido_ganador] = votos[partido_ganador] / (asignaciones[partido_ganador] + 1)

        return asignaciones
    
    def crear_pestana_resultados(self):
        """Crea la pestaña de visualización de resultados"""
        self.resultados_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.resultados_frame, text="Resultados 2025", state='disabled')
        
        # Frame principal con scroll
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
        
        # Contenido inicial (se actualizará con los resultados)
        ttk.Label(scrollable_frame, text="Resultados de la Predicción 2025", 
                 style='Header.TLabel').pack(pady=(10, 20))
        
        self.resultados_container = ttk.Frame(scrollable_frame)
        self.resultados_container.pack(fill='both', expand=True)
    
    def mostrar_resultados(self):
        """Muestra los resultados de la predicción"""
        # Limpiar contenedor
        for widget in self.resultados_container.winfo_children():
            widget.destroy()
        
        # Mostrar predicción de votos
        frame_votos = ttk.LabelFrame(self.resultados_container, text="Predicción de Votos 2025")
        frame_votos.pack(fill='x', padx=10, pady=5)
        
        # Gráfico de pastel
        fig_pastel, ax_pastel = plt.subplots(figsize=(8, 6))
        
        # Filtrar datos pequeños para mejor visualización
        datos_filtrados = {k: v for k, v in self.prediccion_2025.items() if v >= 3.0}
        otros = sum(v for k, v in self.prediccion_2025.items() if v < 3.0)
        
        if otros > 0:
            datos_filtrados['Otros'] = otros
        
        ax_pastel.pie(datos_filtrados.values(), labels=datos_filtrados.keys(),
                     autopct=lambda p: f'{p:.1f}%' if p >= 5 else '',
                     startangle=90)
        ax_pastel.set_title("Distribución Predicha de Votos 2025")
        
        canvas_pastel = FigureCanvasTkAgg(fig_pastel, master=frame_votos)
        canvas_pastel.draw()
        canvas_pastel.get_tk_widget().pack(fill='x', padx=10, pady=10)
        
        # Mostrar distribución de escaños
        frame_escanos = ttk.LabelFrame(self.resultados_container, text="Distribución Predicha de Escaños 2025")
        frame_escanos.pack(fill='x', padx=10, pady=5)
        
        # Gráfico de senadores
        fig_senadores, ax_senadores = plt.subplots(figsize=(10, 5))
        
        partidos_sen = list(self.senadores_2025.keys())
        valores_sen = list(self.senadores_2025.values())
        
        bars_sen = ax_senadores.bar(partidos_sen, valores_sen, color='#3498db')
        ax_senadores.set_title(f"Senadores (Total {self.total_senadores})")
        
        for bar in bars_sen:
            height = bar.get_height()
            ax_senadores.text(bar.get_x() + bar.get_width()/2., height,
                             f'{int(height)}', ha='center', va='bottom')
        
        canvas_sen = FigureCanvasTkAgg(fig_senadores, master=frame_escanos)
        canvas_sen.draw()
        canvas_sen.get_tk_widget().pack(fill='x', padx=10, pady=10)
        
        # Gráfico de diputados
        fig_diputados, ax_diputados = plt.subplots(figsize=(10, 5))
        
        partidos_dip = list(self.diputados_2025.keys())
        valores_dip = list(self.diputados_2025.values())
        
        bars_dip = ax_diputados.bar(partidos_dip, valores_dip, color='#e74c3c')
        ax_diputados.set_title(f"Diputados (Total {self.total_diputados})")
        
        for bar in bars_dip:
            height = bar.get_height()
            ax_diputados.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom')
        
        canvas_dip = FigureCanvasTkAgg(fig_diputados, master=frame_escanos)
        canvas_dip.draw()
        canvas_dip.get_tk_widget().pack(fill='x', padx=10, pady=10)
        
        # Mostrar resumen numérico
        frame_resumen = ttk.LabelFrame(self.resultados_container, text="Resumen Numérico")
        frame_resumen.pack(fill='x', padx=10, pady=5)
        
        # Crear tabla con resultados
        columns = ['Partido', 'Votos (%)', 'Senadores', 'Diputados']
        tree = ttk.Treeview(frame_resumen, columns=columns, show='headings', height=5)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        for partido in sorted(self.prediccion_2025.keys(), key=lambda x: -self.prediccion_2025[x]):
            votos = f"{self.prediccion_2025[partido]:.1f}%"
            sen = self.senadores_2025.get(partido, 0)
            dip = self.diputados_2025.get(partido, 0)
            tree.insert('', 'end', values=(partido, votos, sen, dip))
        
        tree.pack(fill='x', padx=10, pady=10)
    
    def crear_pestana_exportacion(self):
        """Crea la pestaña de exportación de resultados"""
        self.export_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.export_frame, text="Exportar Resultados")
        
        # Frame principal
        main_frame = ttk.Frame(self.export_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(main_frame, text="Exportar Resultados de la Predicción", 
                 style='Header.TLabel').pack(pady=(0, 20))
        
        # Opciones de exportación
        frame = ttk.LabelFrame(main_frame, text="Formatos de Exportación")
        frame.pack(fill='x', pady=5)
        
        ttk.Button(frame, text="Exportar a Excel", 
                  command=self.exportar_excel).pack(pady=10, padx=20, fill='x')
        
        ttk.Button(frame, text="Exportar Gráficos como Imágenes", 
                  command=self.exportar_graficos).pack(pady=10, padx=20, fill='x')
        
        ttk.Button(frame, text="Generar Reporte PDF", 
                  command=self.generar_reporte).pack(pady=10, padx=20, fill='x')
        
        # Área de estado
        self.export_status = ttk.Label(main_frame, text="", foreground='#27ae60')
        self.export_status.pack(pady=10)
    
    def exportar_excel(self):
        """Exporta los resultados a un archivo Excel"""
        try:
            if not hasattr(self, 'prediccion_2025'):
                messagebox.showerror("Error", "No hay resultados para exportar.")
                return
            
            # Crear DataFrames
            df_resultados = pd.DataFrame({
                'Partido': list(self.prediccion_2025.keys()),
                'Votos (%)': list(self.prediccion_2025.values()),
                'Senadores': [self.senadores_2025.get(p, 0) for p in self.prediccion_2025.keys()],
                'Diputados': [self.diputados_2025.get(p, 0) for p in self.prediccion_2025.keys()]
            })
            
            # Crear archivo Excel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"prediccion_electoral_2025_{timestamp}.xlsx"
            
            with pd.ExcelWriter(filename) as writer:
                df_resultados.to_excel(writer, sheet_name='Resultados', index=False)
                
                # Hoja con metadatos
                metadata = {
                    'Fecha': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    'Peso datos históricos': [f"{self.peso_historico*100:.1f}%"],
                    'Peso encuestas 2025': [f"{self.peso_encuestas*100:.1f}%"],
                    'Margen de error': [f"{float(self.margen_error.get())}%"],
                    'Tendencia aplicada': [self.tendencia.get()],
                    'Umbral mínimo': [f"{self.umbral_minimo*100}%"],
                    'Total senadores': [self.total_senadores],
                    'Total diputados': [self.total_diputados]
                }
                pd.DataFrame(metadata).to_excel(writer, sheet_name='Metadatos', index=False)
            
            self.export_status.config(text=f"Archivo guardado como: {filename}")
            messagebox.showinfo("Éxito", f"Resultados exportados a {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    def exportar_graficos(self):
        """Exporta los gráficos como imágenes PNG"""
        try:
            if not hasattr(self, 'prediccion_2025'):
                messagebox.showerror("Error", "No hay gráficos para exportar.")
                return
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Gráfico de pastel
            fig_pastel, ax_pastel = plt.subplots(figsize=(8, 6))
            
            # Filtrar datos pequeños
            datos_filtrados = {k: v for k, v in self.prediccion_2025.items() if v >= 3.0}
            otros = sum(v for v in self.prediccion_2025.values() if v < 3.0)
            
            if otros > 0:
                datos_filtrados['Otros'] = otros
            
            ax_pastel.pie(datos_filtrados.values(), labels=datos_filtrados.keys(), 
                         autopct='%1.1f%%', startangle=90)
            ax_pastel.set_title("Distribución Predicha de Votos 2025")
            fig_pastel.savefig(f"prediccion_votos_{timestamp}.png", bbox_inches='tight')
            plt.close(fig_pastel)
            
            # Gráfico de senadores
            fig_senadores, ax_senadores = plt.subplots(figsize=(10, 6))
            
            partidos = list(self.senadores_2025.keys())
            valores = list(self.senadores_2025.values())
            
            bars = ax_senadores.bar(partidos, valores, color='#3498db')
            ax_senadores.set_title(f"Distribución Predicha de Senadores 2025")
            
            for bar in bars:
                height = bar.get_height()
                ax_senadores.text(bar.get_x() + bar.get_width()/2., height,
                                f'{int(height)}', ha='center', va='bottom')
            
            if len(partidos) > 4:
                plt.xticks(rotation=45, ha='right')
            
            fig_senadores.savefig(f"prediccion_senadores_{timestamp}.png", bbox_inches='tight')
            plt.close(fig_senadores)
            
            self.export_status.config(text=f"Gráficos exportados (_{timestamp}.png)")
            messagebox.showinfo("Éxito", "Gráficos exportados como imágenes PNG")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron exportar los gráficos: {str(e)}")
    
    def generar_reporte(self):
        """Genera un reporte PDF con los resultados"""
        messagebox.showinfo("Información", "Esta funcionalidad está en desarrollo.")
        self.export_status.config(text="Generación de PDF en desarrollo")

if __name__ == "__main__":
    root = tk.Tk()
    app = PredictorElectoral2025(root)
    root.mainloop()