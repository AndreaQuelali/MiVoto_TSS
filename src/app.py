import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import pandas as pd
import random
import numpy as np
from datetime import datetime

class SimuladorElectoralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Electoral Bolivia 2025 - Modelo Mejorado")
        self.root.geometry("1200x900")
        
        # Configuración de estilos
        self.configurar_estilos()
        
        # Datos históricos completos
        self.datos_historicos = {
            '2014': {'MAS': 61.36, 'UD': 24.23, 'PDC': 9.04, 'Otros': 5.37},
            '2019': {'MAS': 47.08, 'CC': 36.51, 'FPV': 8.86, 'Otros': 7.55},
            '2020': {'MAS': 54.10, 'CC': 28.83, 'Creemos': 14.00, 'FPV': 1.55, 'PAN-BOL': 0.52}
        }
        
        # Configuración electoral
        self.total_senadores = 36
        self.total_diputados = 130
        self.umbral_minimo = 0.03  # 3% mínimo para representación
        self.umbral_segunda_vuelta = 0.40  # 40% con 10% de diferencia
        
        # Variables de simulación
        self.variacion_maxima = 5.0  # Variación máxima para simulaciones
        
        # Inicializar interfaz
        self.inicializar_interfaz()
        
    def configurar_estilos(self):
        """Configura los estilos visuales de la aplicación"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores base
        self.style.configure('.', background='#f0f0f0', foreground='#333333')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#1a5276')
        self.style.configure('Subheader.TLabel', font=('Arial', 12, 'bold'), foreground='#2874a6')
        
        # Configurar colores para los notebooks
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TNotebook.Tab', background='#d5d8dc', padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#3498db')], 
                      foreground=[('selected', 'white')])
    
    def inicializar_interfaz(self):
        """Inicializa los componentes de la interfaz gráfica"""
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestañas
        self.crear_pestana_configuracion()
        self.crear_pestana_resultados()
        self.crear_pestana_analisis()
        self.crear_pestana_exportacion()
        
        # Seleccionar pestaña inicial
        self.notebook.select(self.config_frame)
    
    def crear_pestana_configuracion(self):
        """Crea la pestaña de configuración de la simulación"""
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configuración")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(self.config_frame)
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
        ttk.Label(scrollable_frame, text="Configuración de Simulación Electoral", 
                 style='Header.TLabel').pack(pady=(10, 20))
        
        # Sección de datos históricos
        self.crear_seccion_historicos(scrollable_frame)
        
        # Sección de simulación
        self.crear_seccion_simulacion(scrollable_frame)
        
        # Sección de configuración avanzada
        self.crear_seccion_avanzada(scrollable_frame)
    
    def crear_seccion_historicos(self, parent):
        """Crea la sección de selección de datos históricos"""
        frame = ttk.LabelFrame(parent, text="Datos Históricos de Referencia")
        frame.pack(fill='x', padx=10, pady=5)
        
        # Selector de año
        ttk.Label(frame, text="Seleccione año histórico:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.anio_combobox = ttk.Combobox(frame, values=list(self.datos_historicos.keys()), state='readonly')
        self.anio_combobox.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.anio_combobox.set('2020')
        
        # Mostrar partidos del año seleccionado
        self.partidos_frame = ttk.Frame(frame)
        self.partidos_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # Actualizar lista de partidos
        self.actualizar_lista_partidos()
        
        # Botón para cargar histórico
        ttk.Button(frame, text="Cargar Datos Históricos", 
                  command=self.cargar_datos_historicos).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Configurar grid
        frame.columnconfigure(1, weight=1)
    
    def actualizar_lista_partidos(self):
        """Actualiza la lista de partidos según el año seleccionado"""
        for widget in self.partidos_frame.winfo_children():
            widget.destroy()
            
        anio = self.anio_combobox.get()
        partidos = self.datos_historicos.get(anio, {})
        
        if not partidos:
            ttk.Label(self.partidos_frame, text="No hay datos para el año seleccionado").pack()
            return
        
        ttk.Label(self.partidos_frame, text="Partidos disponibles:").pack(anchor='w')
        
        for partido, porcentaje in partidos.items():
            ttk.Label(self.partidos_frame, 
                     text=f"{partido}: {porcentaje}%").pack(anchor='w', padx=10)
    
    def crear_seccion_simulacion(self, parent):
        """Crea la sección de configuración de simulación"""
        frame = ttk.LabelFrame(parent, text="Configuración de Simulación")
        frame.pack(fill='x', padx=10, pady=5)
        
        # Variación máxima
        ttk.Label(frame, text="Variación máxima (%):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.variacion_spinbox = ttk.Spinbox(frame, from_=0, to=20, increment=0.5, width=8)
        self.variacion_spinbox.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.variacion_spinbox.set('5.0')
        
        # Número de simulaciones
        ttk.Label(frame, text="Número de simulaciones:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.num_simulaciones_spinbox = ttk.Spinbox(frame, from_=1, to=100, increment=1, width=8)
        self.num_simulaciones_spinbox.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.num_simulaciones_spinbox.set('10')
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Simular Elección", 
                  command=self.simular_eleccion).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Simular Múltiples Escenarios", 
                  command=self.simular_multiples_escenarios).pack(side='left', padx=5)
        
        # Configurar grid
        frame.columnconfigure(1, weight=1)
    
    def crear_seccion_avanzada(self, parent):
        """Crea la sección de configuración avanzada"""
        frame = ttk.LabelFrame(parent, text="Configuración Avanzada")
        frame.pack(fill='x', padx=10, pady=5)
        
        # Umbral mínimo
        ttk.Label(frame, text="Umbral mínimo para representación (%):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.umbral_entry = ttk.Entry(frame, width=8)
        self.umbral_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.umbral_entry.insert(0, '3.0')
        
        # Reglas segunda vuelta
        ttk.Label(frame, text="Reglas segunda vuelta:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.segunda_vuelta_var = tk.StringVar(value="40% con 10% diferencia")
        ttk.OptionMenu(frame, self.segunda_vuelta_var, 
                       "40% con 10% diferencia", 
                       "40% con 10% diferencia", 
                       "50% + 1 voto").grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Paridad de género
        self.paridad_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Aplicar paridad de género (50/50)", 
                       variable=self.paridad_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        # Configurar grid
        frame.columnconfigure(1, weight=1)
    
    def crear_pestana_resultados(self):
        """Crea la pestaña de visualización de resultados"""
        self.resultados_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.resultados_frame, text="Resultados", state='disabled')
        
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
        
        # Contenido
        ttk.Label(scrollable_frame, text="Resultados de la Simulación", 
                 style='Header.TLabel').pack(pady=(10, 20))
        
        # Gráficos
        self.resultados_graficos_frame = ttk.Frame(scrollable_frame)
        self.resultados_graficos_frame.pack(fill='x', padx=10, pady=5)
        
        # Resultados detallados
        self.crear_seccion_resultados_detallados(scrollable_frame)
    
    def crear_seccion_resultados_detallados(self, parent):
        """Crea la sección de resultados detallados"""
        frame = ttk.LabelFrame(parent, text="Resultados Detallados")
        frame.pack(fill='x', padx=10, pady=5)
        
        # Texto con resultados
        self.resultados_text = tk.Text(frame, height=15, wrap='word', font=('Arial', 10))
        self.resultados_text.pack(fill='x', padx=5, pady=5)
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(frame, command=self.resultados_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.resultados_text.config(yscrollcommand=scrollbar.set)
    
    def crear_pestana_analisis(self):
        """Crea la pestaña de análisis de tendencias"""
        self.analisis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analisis_frame, text="Análisis", state='disabled')
        
        # Frame principal con scroll
        main_frame = ttk.Frame(self.analisis_frame)
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
        ttk.Label(scrollable_frame, text="Análisis de Tendencias", 
                 style='Header.TLabel').pack(pady=(10, 20))
        
        # Gráfico de tendencias
        self.tendencias_frame = ttk.Frame(scrollable_frame)
        self.tendencias_frame.pack(fill='x', padx=10, pady=5)
        
        # Análisis estadístico
        self.crear_seccion_estadisticos(scrollable_frame)
    
    def crear_seccion_estadisticos(self, parent):
        """Crea la sección de análisis estadístico"""
        frame = ttk.LabelFrame(parent, text="Estadísticas")
        frame.pack(fill='x', padx=10, pady=5)
        
        # Texto con análisis
        self.analisis_text = tk.Text(frame, height=10, wrap='word', font=('Arial', 10))
        self.analisis_text.pack(fill='x', padx=5, pady=5)
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(frame, command=self.analisis_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.analisis_text.config(yscrollcommand=scrollbar.set)
    
    def crear_pestana_exportacion(self):
        """Crea la pestaña de exportación de resultados"""
        self.export_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.export_frame, text="Exportar")
        
        # Frame principal
        main_frame = ttk.Frame(self.export_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(main_frame, text="Exportar Resultados", 
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
    
    def cargar_datos_historicos(self):
        """Carga los datos históricos del año seleccionado"""
        anio = self.anio_combobox.get()
        self.partidos_hist = self.datos_historicos.get(anio, {})
        self.actualizar_lista_partidos()
        messagebox.showinfo("Datos Cargados", f"Datos históricos de {anio} cargados correctamente.")
    
    def simular_eleccion(self):
        """Ejecuta una simulación electoral"""
        try:
            # Validar datos
            if not self.partidos_hist:
                messagebox.showerror("Error", "No hay datos históricos cargados.")
                return
            
            # Obtener parámetros de simulación
            variacion = float(self.variacion_spinbox.get())
            umbral = float(self.umbral_entry.get()) / 100
            
            # Simular elección
            self.resultados = self.simular_resultados(variacion)
            
            # Aplicar umbral mínimo
            self.umbral_minimo = umbral
            
            # Verificar segunda vuelta
            self.verificar_segunda_vuelta()
            
            # Asignar escaños
            self.asignar_escanos()
            
            # Mostrar resultados
            self.mostrar_resultados()
            
            # Habilitar pestañas de resultados y análisis
            self.notebook.tab(self.resultados_frame, state='normal')
            self.notebook.tab(self.analisis_frame, state='normal')
            self.notebook.select(self.resultados_frame)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros: {str(e)}")
    
    def simular_resultados(self, variacion_maxima):
        """Simula resultados electorales con variación aleatoria"""
        resultados = {}
        
        for partido, porcentaje in self.partidos_hist.items():
            # Aplicar variación aleatoria (distribución normal)
            variacion = random.gauss(0, variacion_maxima/3)  # 99.7% dentro de ±variacion_maxima
            nuevo_porcentaje = max(0.0, porcentaje + variacion)
            resultados[partido] = nuevo_porcentaje
        
        # Normalizar para que sumen 100%
        total = sum(resultados.values())
        if total > 0:
            resultados = {p: (v/total)*100 for p, v in resultados.items()}
        
        return resultados
    
    def verificar_segunda_vuelta(self):
        """Determina si se necesita segunda vuelta según las reglas configuradas"""
        total_votos = sum(self.resultados.values())
        if total_votos == 0:
            return
        
        # Determinar reglas según configuración
        regla = self.segunda_vuelta_var.get()
        
        if regla == "50% + 1 voto":
            umbral = 50.0
            # Verificar si algún partido supera el 50%
            if not any(voto > umbral for voto in self.resultados.values()):
                self.preparar_segunda_vuelta()
        else:  # "40% con 10% diferencia"
            primer_partido, segundo_partido = self.obtener_dos_mas_votados()
            
            # Verificar si el primero tiene 40% y 10% más que el segundo
            if (primer_partido[1] < 40.0 or 
                (primer_partido[1] - segundo_partido[1]) < 10.0):
                self.preparar_segunda_vuelta()
    
    def obtener_dos_mas_votados(self):
        """Devuelve los dos partidos más votados"""
        partidos_ordenados = sorted(self.resultados.items(), key=lambda x: -x[1])
        return partidos_ordenados[0], partidos_ordenados[1]
    
    def preparar_segunda_vuelta(self):
        """Prepara los datos para una segunda vuelta"""
        primer_partido, segundo_partido = self.obtener_dos_mas_votados()
        
        # Crear nuevo diccionario solo con los dos partidos
        self.resultados = {
            primer_partido[0]: primer_partido[1],
            segundo_partido[0]: segundo_partido[1]
        }
        
        messagebox.showinfo("Segunda Vuelta", 
                          f"Se realizará segunda vuelta entre:\n"
                          f"{primer_partido[0]} ({primer_partido[1]:.2f}%)\n"
                          f"{segundo_partido[0]} ({segundo_partido[1]:.2f}%)")
    
    def asignar_escanos(self):
        """Asigna escaños usando el método D'Hondt"""
        total_votos = sum(self.resultados.values())
        if total_votos == 0:
            self.senadores = {}
            self.diputados = {}
            return
        
        # Filtrar partidos que superan el umbral
        partidos_validos = {p: v for p, v in self.resultados.items() 
                          if (v / total_votos) >= self.umbral_minimo}
        
        # Asignar escaños para senadores
        self.senadores = self.aplicar_metodo_dhondt(partidos_validos, self.total_senadores)
        
        # Asignar escaños para diputados
        self.diputados = self.aplicar_metodo_dhondt(partidos_validos, self.total_diputados)
        
        # Aplicar paridad de género si está activado
        if self.paridad_var.get():
            self.aplicar_paridad_genero()
    
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
    
    def aplicar_paridad_genero(self):
        """Ajusta la asignación de escaños para cumplir con paridad de género"""
        # Para senadores
        for partido in self.senadores:
            total = self.senadores[partido]
            if total > 0:
                mujeres = total // 2
                hombres = total - mujeres
                self.senadores[partido] = {'Total': total, 'Mujeres': mujeres, 'Hombres': hombres}
        
        # Para diputados
        for partido in self.diputados:
            total = self.diputados[partido]
            if total > 0:
                mujeres = total // 2
                hombres = total - mujeres
                self.diputados[partido] = {'Total': total, 'Mujeres': mujeres, 'Hombres': hombres}
    
    def mostrar_resultados(self):
        """Muestra los resultados de la simulación"""
        # Calcular porcentajes
        total_votos = sum(self.resultados.values())
        porcentajes = {p: (v/total_votos)*100 for p, v in self.resultados.items()}
        
        # Mostrar en texto
        self.mostrar_resultados_texto(total_votos, porcentajes)
        
        # Mostrar gráficos
        self.mostrar_graficos(porcentajes)
        
        # Actualizar análisis
        self.actualizar_analisis()
    
    def mostrar_resultados_texto(self, total_votos, porcentajes):
        """Muestra los resultados en el área de texto"""
        self.resultados_text.config(state='normal')
        self.resultados_text.delete('1.0', 'end')
        
        # Encabezado
        self.resultados_text.insert('end', "RESULTADOS DE LA SIMULACIÓN\n", 'header')
        self.resultados_text.insert('end', f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Resultados generales
        self.resultados_text.insert('end', "RESULTADOS GENERALES\n", 'subheader')
        self.resultados_text.insert('end', f"Total de votos simulados: {total_votos:.2f}\n\n")
        
        # Por partido
        self.resultados_text.insert('end', "Por Partido:\n", 'bold')
        for partido, votos in sorted(self.resultados.items(), key=lambda x: -x[1]):
            self.resultados_text.insert('end', 
                                      f"- {partido}: {votos:.2f} votos ({porcentajes[partido]:.2f}%)\n")
        
        # Senadores
        self.resultados_text.insert('end', "\nDISTRIBUCIÓN DE SENADORES\n", 'subheader')
        self.resultados_text.insert('end', f"Total escaños: {self.total_senadores}\n\n")
        
        if self.paridad_var.get():
            for partido, datos in sorted(self.senadores.items(), key=lambda x: -x[1]['Total']):
                self.resultados_text.insert('end', 
                                          f"- {partido}: {datos['Total']} ({datos['Mujeres']} mujeres, {datos['Hombres']} hombres)\n")
        else:
            for partido, escanos in sorted(self.senadores.items(), key=lambda x: -x[1]):
                self.resultados_text.insert('end', f"- {partido}: {escanos}\n")
        
        # Diputados
        self.resultados_text.insert('end', "\nDISTRIBUCIÓN DE DIPUTADOS\n", 'subheader')
        self.resultados_text.insert('end', f"Total escaños: {self.total_diputados}\n\n")
        
        if self.paridad_var.get():
            for partido, datos in sorted(self.diputados.items(), key=lambda x: -x[1]['Total']):
                self.resultados_text.insert('end', 
                                          f"- {partido}: {datos['Total']} ({datos['Mujeres']} mujeres, {datos['Hombres']} hombres)\n")
        else:
            for partido, escanos in sorted(self.diputados.items(), key=lambda x: -x[1]):
                self.resultados_text.insert('end', f"- {partido}: {escanos}\n")
        
        # Configurar tags para estilos
        self.resultados_text.tag_config('header', font=('Arial', 12, 'bold'))
        self.resultados_text.tag_config('subheader', font=('Arial', 11, 'bold'))
        self.resultados_text.tag_config('bold', font=('Arial', 10, 'bold'))
        
        self.resultados_text.config(state='disabled')
    
    def mostrar_graficos(self, porcentajes):
        """Muestra los gráficos de resultados"""
        # Limpiar frames anteriores
        for widget in self.resultados_graficos_frame.winfo_children():
            widget.destroy()
        
        # Crear notebook para gráficos
        graficos_notebook = ttk.Notebook(self.resultados_graficos_frame)
        graficos_notebook.pack(fill='both', expand=True)
        
        # Gráfico de resultados generales
        frame_pastel = ttk.Frame(graficos_notebook)
        graficos_notebook.add(frame_pastel, text="Distribución de Votos")
        self.crear_grafico_pastel(frame_pastel, porcentajes, "Distribución de Votos por Partido")
        
        # Gráfico de senadores
        frame_senadores = ttk.Frame(graficos_notebook)
        graficos_notebook.add(frame_senadores, text="Distribución de Senadores")
        
        if self.paridad_var.get():
            datos_senadores = {p: d['Total'] for p, d in self.senadores.items()}
        else:
            datos_senadores = self.senadores
            
        self.crear_grafico_barras(frame_senadores, datos_senadores, 
                                 f"Distribución de Senadores (Total {self.total_senadores})", 
                                 "#3498db")
        
        # Gráfico de diputados
        frame_diputados = ttk.Frame(graficos_notebook)
        graficos_notebook.add(frame_diputados, text="Distribución de Diputados")
        
        if self.paridad_var.get():
            datos_diputados = {p: d['Total'] for p, d in self.diputados.items()}
        else:
            datos_diputados = self.diputados
            
        self.crear_grafico_barras(frame_diputados, datos_diputados, 
                                 f"Distribución de Diputados (Total {self.total_diputados})", 
                                 "#e74c3c")
    
    def crear_grafico_pastel(self, parent, datos, titulo):
        """Crea un gráfico de pastel"""
        fig, ax = plt.subplots(figsize=(6, 5))
        
        # Filtrar datos muy pequeños para mejorar la visualización
        datos_filtrados = {k: v for k, v in datos.items() if v >= 1.0}
        otros = sum(v for v in datos.values() if v < 1.0)
        
        if otros > 0:
            datos_filtrados['Otros'] = otros
        
        # Colores
        colores = plt.cm.Pastel1(range(len(datos_filtrados)))
        
        # Crear gráfico
        wedges, texts, autotexts = ax.pie(
            datos_filtrados.values(),
            labels=datos_filtrados.keys(),
            autopct=lambda p: f'{p:.1f}%' if p >= 5 else '',
            startangle=90,
            colors=colores,
            wedgeprops=dict(width=0.4, edgecolor='w'),
            pctdistance=0.85
        )
        
        # Configurar etiquetas
        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(texts, size=8)
        
        ax.set_title(titulo)
        
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def crear_grafico_barras(self, parent, datos, titulo, color):
        """Crea un gráfico de barras"""
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Ordenar datos
        partidos = [p for p, _ in sorted(datos.items(), key=lambda x: -x[1])]
        valores = [v for _, v in sorted(datos.items(), key=lambda x: -x[1])]
        
        # Crear gráfico
        bars = ax.bar(partidos, valores, color=color)
        
        # Añadir valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Configurar ejes
        ax.set_title(titulo)
        ax.set_ylabel('Cantidad')
        ax.set_ylim(0, max(valores) * 1.2)
        
        # Rotar etiquetas si son muchas
        if len(partidos) > 4:
            plt.xticks(rotation=45, ha='right')
        
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def actualizar_analisis(self):
        """Actualiza el análisis de tendencias"""
        # Limpiar frame de tendencias
        for widget in self.tendencias_frame.winfo_children():
            widget.destroy()
        
        # Crear gráfico de tendencias históricas
        self.crear_grafico_tendencias()
        
        # Actualizar texto de análisis
        self.analisis_text.config(state='normal')
        self.analisis_text.delete('1.0', 'end')
        
        # Análisis básico
        partido_ganador = max(self.resultados.items(), key=lambda x: x[1])
        
        self.analisis_text.insert('end', "ANÁLISIS DE RESULTADOS\n\n", 'header')
        self.analisis_text.insert('end', 
                                f"Partido con mayor votación: {partido_ganador[0]} ({partido_ganador[1]:.2f}%)\n\n", 
                                'bold')
        
        # Análisis de representación
        self.analisis_text.insert('end', "REPRESENTACIÓN PARLAMENTARIA\n\n", 'subheader')
        
        # Senadores
        senador_mayoria = max(self.senadores.items(), key=lambda x: x[1]['Total'] if isinstance(x[1], dict) else x[1])
        self.analisis_text.insert('end', 
                                f"Mayoría en Senado: {senador_mayoria[0]} " 
                                f"({senador_mayoria[1]['Total'] if isinstance(senador_mayoria[1], dict) else senador_mayoria[1]} escaños)\n")
        
        # Diputados
        diputado_mayoria = max(self.diputados.items(), key=lambda x: x[1]['Total'] if isinstance(x[1], dict) else x[1])
        self.analisis_text.insert('end', 
                                f"Mayoría en Cámara de Diputados: {diputado_mayoria[0]} " 
                                f"({diputado_mayoria[1]['Total'] if isinstance(diputado_mayoria[1], dict) else diputado_mayoria[1]} escaños)\n\n")
        
        # Configurar estilos
        self.analisis_text.tag_config('header', font=('Arial', 12, 'bold'))
        self.analisis_text.tag_config('subheader', font=('Arial', 11, 'bold'))
        self.analisis_text.tag_config('bold', font=('Arial', 10, 'bold'))
        
        self.analisis_text.config(state='disabled')
    
    def crear_grafico_tendencias(self):
        """Crea un gráfico de tendencias históricas"""
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
        canvas = FigureCanvasTkAgg(fig, master=self.tendencias_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def simular_multiples_escenarios(self):
        """Ejecuta múltiples simulaciones para análisis estadístico"""
        try:
            num_simulaciones = int(self.num_simulaciones_spinbox.get())
            if num_simulaciones < 1:
                raise ValueError("El número de simulaciones debe ser al menos 1")
            
            variacion = float(self.variacion_spinbox.get())
            umbral = float(self.umbral_entry.get()) / 100
            
            # Configurar
            self.umbral_minimo = umbral
            
            # Ejecutar simulaciones
            resultados_simulaciones = []
            senadores_simulaciones = []
            diputados_simulaciones = []
            
            for _ in range(num_simulaciones):
                # Simular
                resultados = self.simular_resultados(variacion)
                
                # Verificar segunda vuelta
                if self.verificar_segunda_vuelta_simulacion(resultados):
                    primer_partido, segundo_partido = self.obtener_dos_mas_votados_simulacion(resultados)
                    resultados = {
                        primer_partido[0]: primer_partido[1],
                        segundo_partido[0]: segundo_partido[1]
                    }
                
                # Asignar escaños
                senadores = self.aplicar_metodo_dhondt_simulacion(resultados, self.total_senadores, umbral)
                diputados = self.aplicar_metodo_dhondt_simulacion(resultados, self.total_diputados, umbral)
                
                # Guardar resultados
                resultados_simulaciones.append(resultados)
                senadores_simulaciones.append(senadores)
                diputados_simulaciones.append(diputados)
            
            # Analizar resultados
            self.analizar_simulaciones(resultados_simulaciones, senadores_simulaciones, diputados_simulaciones)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros: {str(e)}")
    
    def verificar_segunda_vuelta_simulacion(self, resultados):
        """Verifica si se necesita segunda vuelta para una simulación"""
        total_votos = sum(resultados.values())
        if total_votos == 0:
            return False
        
        regla = self.segunda_vuelta_var.get()
        
        if regla == "50% + 1 voto":
            umbral = 50.0
            return not any(voto > umbral for voto in resultados.values())
        else:  # "40% con 10% diferencia"
            partidos_ordenados = sorted(resultados.items(), key=lambda x: -x[1])
            primer_partido = partidos_ordenados[0]
            segundo_partido = partidos_ordenados[1]
            
            return (primer_partido[1] < 40.0 or 
                   (primer_partido[1] - segundo_partido[1]) < 10.0)
    
    def obtener_dos_mas_votados_simulacion(self, resultados):
        """Obtiene los dos partidos más votados para una simulación"""
        partidos_ordenados = sorted(resultados.items(), key=lambda x: -x[1])
        return partidos_ordenados[0], partidos_ordenados[1]
    
    def aplicar_metodo_dhondt_simulacion(self, votos, total_escanos, umbral):
        """Aplica D'Hondt para una simulación específica"""
        total_votos = sum(votos.values())
        if total_votos == 0:
            return {}
        
        partidos_validos = {p: v for p, v in votos.items() if (v / total_votos) >= umbral}
        if not partidos_validos:
            return {}
        
        asignaciones = {p: 0 for p in partidos_validos}
        cocientes = {p: v for p, v in partidos_validos.items()}
        
        for _ in range(total_escanos):
            partido_ganador = max(cocientes.items(), key=lambda x: x[1])[0]
            asignaciones[partido_ganador] += 1
            cocientes[partido_ganador] = partidos_validos[partido_ganador] / (asignaciones[partido_ganador] + 1)
        
        return asignaciones
    
    def analizar_simulaciones(self, resultados_simulaciones, senadores_simulaciones, diputados_simulaciones):
        """Analiza los resultados de múltiples simulaciones"""
        # Habilitar pestaña de análisis
        self.notebook.tab(self.analisis_frame, state='normal')
        self.notebook.select(self.analisis_frame)
        
        # Limpiar frames anteriores
        for widget in self.tendencias_frame.winfo_children():
            widget.destroy()
        
        # Crear gráfico de distribución de resultados
        self.crear_grafico_distribucion(resultados_simulaciones)
        
        # Actualizar texto de análisis
        self.analisis_text.config(state='normal')
        self.analisis_text.delete('1.0', 'end')
        
        # Análisis estadístico
        self.analisis_text.insert('end', "ANÁLISIS ESTADÍSTICO DE SIMULACIONES\n\n", 'header')
        
        # Calcular promedios
        todos_partidos = set()
        for sim in resultados_simulaciones:
            todos_partidos.update(sim.keys())
        
        promedios = {}
        for partido in todos_partidos:
            valores = [sim.get(partido, 0) for sim in resultados_simulaciones]
            promedios[partido] = sum(valores) / len(valores)
        
        self.analisis_text.insert('end', "Promedio de votación:\n", 'subheader')
        for partido, promedio in sorted(promedios.items(), key=lambda x: -x[1]):
            self.analisis_text.insert('end', f"- {partido}: {promedio:.2f}%\n")
        
        # Frecuencia de mayoría en senadores
        frec_senadores = defaultdict(int)
        for sim in senadores_simulaciones:
            if sim:
                mayor = max(sim.items(), key=lambda x: x[1])[0]
                frec_senadores[mayor] += 1
        
        self.analisis_text.insert('end', "\nFrecuencia de mayoría en Senado:\n", 'subheader')
        for partido, freq in sorted(frec_senadores.items(), key=lambda x: -x[1]):
            self.analisis_text.insert('end', f"- {partido}: {freq}/{len(senadores_simulaciones)} ({freq/len(senadores_simulaciones):.1%})\n")
        
        # Frecuencia de mayoría en diputados
        frec_diputados = defaultdict(int)
        for sim in diputados_simulaciones:
            if sim:
                mayor = max(sim.items(), key=lambda x: x[1])[0]
                frec_diputados[mayor] += 1
        
        self.analisis_text.insert('end', "\nFrecuencia de mayoría en Diputados:\n", 'subheader')
        for partido, freq in sorted(frec_diputados.items(), key=lambda x: -x[1]):
            self.analisis_text.insert('end', f"- {partido}: {freq}/{len(diputados_simulaciones)} ({freq/len(diputados_simulaciones):.1%})\n")
        
        self.analisis_text.config(state='disabled')
    
    def crear_grafico_distribucion(self, resultados_simulaciones):
        """Crea un gráfico de distribución de resultados de simulaciones"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Preparar datos
        todos_partidos = set()
        for sim in resultados_simulaciones:
            todos_partidos.update(sim.keys())
        
        datos = {partido: [] for partido in todos_partidos}
        for sim in resultados_simulaciones:
            for partido in todos_partidos:
                datos[partido].append(sim.get(partido, 0))
        
        # Crear boxplot
        ax.boxplot(datos.values(), labels=datos.keys())
        
        # Configurar gráfico
        ax.set_title("Distribución de Resultados en Simulaciones")
        ax.set_ylabel("Porcentaje de Votos")
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.tendencias_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def exportar_excel(self):
        """Exporta los resultados a un archivo Excel"""
        try:
            if not hasattr(self, 'resultados') or not self.resultados:
                messagebox.showerror("Error", "No hay resultados para exportar.")
                return
            
            # Crear DataFrames
            df_resultados = pd.DataFrame({
                'Partido': list(self.resultados.keys()),
                'Votos': list(self.resultados.values()),
                'Porcentaje': [v/sum(self.resultados.values())*100 for v in self.resultados.values()]
            })
            
            # Preparar datos de escaños
            if self.paridad_var.get():
                senadores_data = []
                for partido, datos in self.senadores.items():
                    senadores_data.append({
                        'Partido': partido,
                        'Total': datos['Total'],
                        'Mujeres': datos['Mujeres'],
                        'Hombres': datos['Hombres']
                    })
                
                diputados_data = []
                for partido, datos in self.diputados.items():
                    diputados_data.append({
                        'Partido': partido,
                        'Total': datos['Total'],
                        'Mujeres': datos['Mujeres'],
                        'Hombres': datos['Hombres']
                    })
            else:
                senadores_data = [{'Partido': p, 'Total': v} for p, v in self.senadores.items()]
                diputados_data = [{'Partido': p, 'Total': v} for p, v in self.diputados.items()]
            
            df_senadores = pd.DataFrame(senadores_data)
            df_diputados = pd.DataFrame(diputados_data)
            
            # Crear archivo Excel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resultados_electorales_{timestamp}.xlsx"
            
            with pd.ExcelWriter(filename) as writer:
                df_resultados.to_excel(writer, sheet_name='Resultados', index=False)
                df_senadores.to_excel(writer, sheet_name='Senadores', index=False)
                df_diputados.to_excel(writer, sheet_name='Diputados', index=False)
                
                # Hoja con metadatos
                metadata = {
                    'Fecha': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    'Umbral mínimo': [f"{self.umbral_minimo*100}%"],
                    'Regla segunda vuelta': [self.segunda_vuelta_var.get()],
                    'Paridad de género': ['Sí' if self.paridad_var.get() else 'No'],
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
            if not hasattr(self, 'resultados') or not self.resultados:
                messagebox.showerror("Error", "No hay gráficos para exportar.")
                return
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Gráfico de pastel
            fig_pastel, ax_pastel = plt.subplots(figsize=(8, 6))
            porcentajes = {p: (v/sum(self.resultados.values()))*100 for p, v in self.resultados.items()}
            
            # Filtrar datos pequeños
            datos_filtrados = {k: v for k, v in porcentajes.items() if v >= 1.0}
            otros = sum(v for v in porcentajes.values() if v < 1.0)
            
            if otros > 0:
                datos_filtrados['Otros'] = otros
            
            ax_pastel.pie(datos_filtrados.values(), labels=datos_filtrados.keys(), 
                         autopct='%1.1f%%', startangle=90)
            ax_pastel.set_title("Distribución de Votos por Partido")
            fig_pastel.savefig(f"grafico_pastel_{timestamp}.png", bbox_inches='tight')
            plt.close(fig_pastel)
            
            # Gráfico de barras para senadores
            fig_senadores, ax_senadores = plt.subplots(figsize=(10, 6))
            
            if self.paridad_var.get():
                datos_senadores = {p: d['Total'] for p, d in self.senadores.items()}
            else:
                datos_senadores = self.senadores
            
            partidos = list(datos_senadores.keys())
            valores = list(datos_senadores.values())
            
            bars = ax_senadores.bar(partidos, valores, color='#3498db')
            ax_senadores.set_title(f"Distribución de Senadores (Total {self.total_senadores})")
            
            for bar in bars:
                height = bar.get_height()
                ax_senadores.text(bar.get_x() + bar.get_width()/2., height,
                                f'{int(height)}', ha='center', va='bottom')
            
            if len(partidos) > 4:
                plt.xticks(rotation=45, ha='right')
            
            fig_senadores.savefig(f"grafico_senadores_{timestamp}.png", bbox_inches='tight')
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
    app = SimuladorElectoralApp(root)
    root.mainloop()