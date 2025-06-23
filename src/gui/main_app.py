import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
import pandas as pd
from datetime import datetime
from src.models import ElectoralData, ElectoralConfig
from src.simulation import ElectoralSimulator, DHondtCalculator
from src.visualization import ChartGenerator

class SimuladorElectoralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Electoral Bolivia 2025 - Modelo Mejorado")
        self.root.geometry("1200x900")

        # Modelos y lógica
        self.electoral_data = ElectoralData()
        self.simulator = ElectoralSimulator(self.electoral_data)
        self.dhondt = DHondtCalculator()
        self.config = self.electoral_data.config

        # Variables de simulación
        self.resultados = {}
        self.senadores = {}
        self.diputados = {}
        self.partidos_hist = {}

        # Inicializar interfaz
        self.configurar_estilos()
        self.inicializar_interfaz()

    def configurar_estilos(self):
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
        self.style.map('TNotebook.Tab', background=[('selected', '#3498db')], foreground=[('selected', 'white')])

    def inicializar_interfaz(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        self.crear_pestana_configuracion()
        self.crear_pestana_resultados()
        self.crear_pestana_analisis()
        self.crear_pestana_exportacion()
        self.notebook.select(0)

    def crear_pestana_configuracion(self):
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configuración")
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
        ttk.Label(scrollable_frame, text="Configuración de Simulación Electoral", style='Header.TLabel').pack(pady=(10, 20))
        self.crear_seccion_historicos(scrollable_frame)
        self.crear_seccion_simulacion(scrollable_frame)
        self.crear_seccion_avanzada(scrollable_frame)

    def crear_seccion_historicos(self, parent):
        frame = ttk.LabelFrame(parent, text="Datos Históricos de Referencia")
        frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(frame, text="Seleccione año histórico:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.anio_combobox = ttk.Combobox(frame, values=self.electoral_data.get_available_years(), state='readonly')
        self.anio_combobox.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.anio_combobox.set('2020')
        self.partidos_frame = ttk.Frame(frame)
        self.partidos_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        self.actualizar_lista_partidos()
        ttk.Button(frame, text="Cargar Datos Históricos", command=self.cargar_datos_historicos).grid(row=2, column=0, columnspan=2, pady=10)
        frame.columnconfigure(1, weight=1)

    def actualizar_lista_partidos(self):
        for widget in self.partidos_frame.winfo_children():
            widget.destroy()
        anio = self.anio_combobox.get()
        partidos = self.electoral_data.get_parties_by_year(anio)
        if not partidos:
            ttk.Label(self.partidos_frame, text="No hay datos para el año seleccionado").pack()
            return
        ttk.Label(self.partidos_frame, text="Partidos disponibles:").pack(anchor='w')
        for partido, porcentaje in partidos.items():
            ttk.Label(self.partidos_frame, text=f"{partido}: {porcentaje}%").pack(anchor='w', padx=10)

    def crear_seccion_simulacion(self, parent):
        frame = ttk.LabelFrame(parent, text="Configuración de Simulación")
        frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(frame, text="Variación máxima (%):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.variacion_spinbox = ttk.Spinbox(frame, from_=0, to=20, increment=0.5, width=8)
        self.variacion_spinbox.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.variacion_spinbox.set(str(self.config.variacion_maxima))
        ttk.Label(frame, text="Número de simulaciones:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.num_simulaciones_spinbox = ttk.Spinbox(frame, from_=1, to=100, increment=1, width=8)
        self.num_simulaciones_spinbox.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.num_simulaciones_spinbox.set('10')
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Simular Elección", command=self.simular_eleccion).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Simular Múltiples Escenarios", command=self.simular_multiples_escenarios).pack(side='left', padx=5)
        frame.columnconfigure(1, weight=1)

    def crear_seccion_avanzada(self, parent):
        frame = ttk.LabelFrame(parent, text="Configuración Avanzada")
        frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(frame, text="Umbral mínimo para representación (%):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.umbral_entry = ttk.Entry(frame, width=8)
        self.umbral_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.umbral_entry.insert(0, str(self.config.umbral_minimo * 100))
        ttk.Label(frame, text="Reglas segunda vuelta:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.segunda_vuelta_var = tk.StringVar(value="40% con 10% diferencia")
        ttk.OptionMenu(frame, self.segunda_vuelta_var, "40% con 10% diferencia", "40% con 10% diferencia", "50% + 1 voto").grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.paridad_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Aplicar paridad de género (50/50)", variable=self.paridad_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        frame.columnconfigure(1, weight=1)

    def cargar_datos_historicos(self):
        anio = self.anio_combobox.get()
        self.partidos_hist = self.electoral_data.load_historical_data(anio)
        self.actualizar_lista_partidos()
        messagebox.showinfo("Datos Cargados", f"Datos históricos de {anio} cargados correctamente.")

    def crear_pestana_resultados(self):
        self.resultados_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.resultados_frame, text="Resultados", state='disabled')
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
        ttk.Label(scrollable_frame, text="Resultados de la Simulación", style='Header.TLabel').pack(pady=(10, 20))
        self.resultados_graficos_frame = ttk.Frame(scrollable_frame)
        self.resultados_graficos_frame.pack(fill='x', padx=10, pady=5)
        self.crear_seccion_resultados_detallados(scrollable_frame)

    def crear_seccion_resultados_detallados(self, parent):
        frame = ttk.LabelFrame(parent, text="Resultados Detallados")
        frame.pack(fill='x', padx=10, pady=5)
        self.resultados_text = tk.Text(frame, height=15, wrap='word', font=('Arial', 10))
        self.resultados_text.pack(fill='x', padx=5, pady=5)
        scrollbar = ttk.Scrollbar(frame, command=self.resultados_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.resultados_text.config(yscrollcommand=scrollbar.set)

    def crear_pestana_analisis(self):
        self.analisis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analisis_frame, text="Análisis", state='disabled')
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
        ttk.Label(scrollable_frame, text="Análisis de Tendencias", style='Header.TLabel').pack(pady=(10, 20))
        self.tendencias_frame = ttk.Frame(scrollable_frame)
        self.tendencias_frame.pack(fill='x', padx=10, pady=5)
        self.crear_seccion_estadisticos(scrollable_frame)

    def crear_seccion_estadisticos(self, parent):
        frame = ttk.LabelFrame(parent, text="Estadísticas")
        frame.pack(fill='x', padx=10, pady=5)
        self.analisis_text = tk.Text(frame, height=10, wrap='word', font=('Arial', 10))
        self.analisis_text.pack(fill='x', padx=5, pady=5)
        scrollbar = ttk.Scrollbar(frame, command=self.analisis_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.analisis_text.config(yscrollcommand=scrollbar.set)

    def crear_pestana_exportacion(self):
        self.export_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.export_frame, text="Exportar")
        main_frame = ttk.Frame(self.export_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        ttk.Label(main_frame, text="Exportar Resultados", style='Header.TLabel').pack(pady=(0, 20))
        frame = ttk.LabelFrame(main_frame, text="Formatos de Exportación")
        frame.pack(fill='x', pady=5)
        ttk.Button(frame, text="Exportar a Excel", command=self.exportar_excel).pack(pady=10, padx=20, fill='x')
        ttk.Button(frame, text="Exportar Gráficos como Imágenes", command=self.exportar_graficos).pack(pady=10, padx=20, fill='x')
        ttk.Button(frame, text="Generar Reporte PDF", command=self.generar_reporte).pack(pady=10, padx=20, fill='x')
        self.export_status = ttk.Label(main_frame, text="", foreground='#27ae60')
        self.export_status.pack(pady=10)

    def simular_eleccion(self):
        try:
            if not self.partidos_hist:
                messagebox.showerror("Error", "No hay datos históricos cargados.")
                return
            variacion = float(self.variacion_spinbox.get())
            umbral = float(self.umbral_entry.get()) / 100
            self.resultados = self.simulator.simulate_election(variacion)
            self.config.umbral_minimo = umbral
            self.verificar_segunda_vuelta()
            self.asignar_escanos()
            self.mostrar_resultados()
            self.notebook.tab(self.resultados_frame, state='normal')
            self.notebook.tab(self.analisis_frame, state='normal')
            self.notebook.select(self.resultados_frame)
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros: {str(e)}")

    def simular_multiples_escenarios(self):
        try:
            num_simulaciones = int(self.num_simulaciones_spinbox.get())
            if num_simulaciones < 1:
                raise ValueError("El número de simulaciones debe ser al menos 1")
            variacion = float(self.variacion_spinbox.get())
            umbral = float(self.umbral_entry.get()) / 100
            self.config.umbral_minimo = umbral
            resultados_simulaciones = []
            senadores_simulaciones = []
            diputados_simulaciones = []
            for _ in range(num_simulaciones):
                resultados = self.simulator.simulate_election(variacion)
                if self.simulator.check_second_round_needed(resultados, self.segunda_vuelta_var.get()):
                    top1, top2 = self.simulator.get_top_two_parties(resultados)
                    resultados = {top1[0]: top1[1], top2[0]: top2[1]}
                seats = self.dhondt.calculate_seats_for_chambers(
                    resultados,
                    self.config.total_senadores,
                    self.config.total_diputados,
                    self.config.umbral_minimo,
                    self.paridad_var.get()
                )
                resultados_simulaciones.append(resultados)
                senadores_simulaciones.append(seats['senadores'])
                diputados_simulaciones.append(seats['diputados'])
            self.analizar_simulaciones(resultados_simulaciones, senadores_simulaciones, diputados_simulaciones)
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros: {str(e)}")

    def verificar_segunda_vuelta(self):
        if self.simulator.check_second_round_needed(self.resultados, self.segunda_vuelta_var.get()):
            self.resultados = self.simulator.prepare_second_round(self.resultados)
            top1, top2 = self.simulator.get_top_two_parties(self.resultados)
            messagebox.showinfo("Segunda Vuelta", f"Se realizará segunda vuelta entre:\n{top1[0]} ({top1[1]:.2f}%)\n{top2[0]} ({top2[1]:.2f}%)")

    def asignar_escanos(self):
        seats = self.dhondt.calculate_seats_for_chambers(
            self.resultados,
            self.config.total_senadores,
            self.config.total_diputados,
            self.config.umbral_minimo,
            self.paridad_var.get()
        )
        self.senadores = seats['senadores']
        self.diputados = seats['diputados']

    def mostrar_resultados(self):
        total_votos = sum(self.resultados.values())
        porcentajes = {p: (v/total_votos)*100 for p, v in self.resultados.items()}
        self.mostrar_resultados_texto(total_votos, porcentajes)
        self.mostrar_graficos(porcentajes)
        self.actualizar_analisis()

    def mostrar_resultados_texto(self, total_votos, porcentajes):
        self.resultados_text.config(state='normal')
        self.resultados_text.delete('1.0', 'end')
        self.resultados_text.insert('end', "RESULTADOS DE LA SIMULACIÓN\n", 'header')
        self.resultados_text.insert('end', f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        self.resultados_text.insert('end', "RESULTADOS GENERALES\n", 'subheader')
        self.resultados_text.insert('end', f"Total de votos simulados: {total_votos:.2f}\n\n")
        self.resultados_text.insert('end', "Por Partido:\n", 'bold')
        for partido, votos in sorted(self.resultados.items(), key=lambda x: -x[1]):
            self.resultados_text.insert('end', f"- {partido}: {votos:.2f} votos ({porcentajes[partido]:.2f}%)\n")
        self.resultados_text.insert('end', "\nDISTRIBUCIÓN DE SENADORES\n", 'subheader')
        self.resultados_text.insert('end', f"Total escaños: {self.config.total_senadores}\n\n")
        if self.paridad_var.get():
            for partido, datos in sorted(self.senadores.items(), key=lambda x: -getattr(x[1], 'total', x[1])):
                self.resultados_text.insert('end', f"- {partido}: {datos.total} ({datos.mujeres} mujeres, {datos.hombres} hombres)\n")
        else:
            for partido, escanos in sorted(self.senadores.items(), key=lambda x: -x[1]):
                self.resultados_text.insert('end', f"- {partido}: {escanos}\n")
        self.resultados_text.insert('end', "\nDISTRIBUCIÓN DE DIPUTADOS\n", 'subheader')
        self.resultados_text.insert('end', f"Total escaños: {self.config.total_diputados}\n\n")
        if self.paridad_var.get():
            for partido, datos in sorted(self.diputados.items(), key=lambda x: -getattr(x[1], 'total', x[1])):
                self.resultados_text.insert('end', f"- {partido}: {datos.total} ({datos.mujeres} mujeres, {datos.hombres} hombres)\n")
        else:
            for partido, escanos in sorted(self.diputados.items(), key=lambda x: -x[1]):
                self.resultados_text.insert('end', f"- {partido}: {escanos}\n")
        self.resultados_text.tag_config('header', font=('Arial', 12, 'bold'))
        self.resultados_text.tag_config('subheader', font=('Arial', 11, 'bold'))
        self.resultados_text.tag_config('bold', font=('Arial', 10, 'bold'))
        self.resultados_text.config(state='disabled')

    def mostrar_graficos(self, porcentajes):
        for widget in self.resultados_graficos_frame.winfo_children():
            widget.destroy()
        graficos_notebook = ttk.Notebook(self.resultados_graficos_frame)
        graficos_notebook.pack(fill='both', expand=True)
        frame_pastel = ttk.Frame(graficos_notebook)
        graficos_notebook.add(frame_pastel, text="Distribución de Votos")
        ChartGenerator.create_pie_chart(frame_pastel, porcentajes, "Distribución de Votos por Partido").get_tk_widget().pack(fill='both', expand=True)
        frame_senadores = ttk.Frame(graficos_notebook)
        graficos_notebook.add(frame_senadores, text="Distribución de Senadores")
        ChartGenerator.create_bar_chart(frame_senadores, self.senadores, f"Distribución de Senadores (Total {self.config.total_senadores})", "#3498db").get_tk_widget().pack(fill='both', expand=True)
        frame_diputados = ttk.Frame(graficos_notebook)
        graficos_notebook.add(frame_diputados, text="Distribución de Diputados")
        ChartGenerator.create_bar_chart(frame_diputados, self.diputados, f"Distribución de Diputados (Total {self.config.total_diputados})", "#e74c3c").get_tk_widget().pack(fill='both', expand=True)

    def actualizar_analisis(self):
        for widget in self.tendencias_frame.winfo_children():
            widget.destroy()
        ChartGenerator.create_trends_chart(self.tendencias_frame, self.electoral_data.get_historical_trends()).get_tk_widget().pack(fill='both', expand=True)
        self.analisis_text.config(state='normal')
        self.analisis_text.delete('1.0', 'end')
        partido_ganador = max(self.resultados.items(), key=lambda x: x[1])
        self.analisis_text.insert('end', "ANÁLISIS DE RESULTADOS\n\n", 'header')
        self.analisis_text.insert('end', f"Partido con mayor votación: {partido_ganador[0]} ({partido_ganador[1]:.2f}%)\n\n", 'bold')
        self.analisis_text.insert('end', "REPRESENTACIÓN PARLAMENTARIA\n\n", 'subheader')
        senador_mayoria = max(self.senadores.items(), key=lambda x: getattr(x[1], 'total', x[1]))
        self.analisis_text.insert('end', f"Mayoría en Senado: {senador_mayoria[0]} ({getattr(senador_mayoria[1], 'total', senador_mayoria[1])} escaños)\n")
        diputado_mayoria = max(self.diputados.items(), key=lambda x: getattr(x[1], 'total', x[1]))
        self.analisis_text.insert('end', f"Mayoría en Cámara de Diputados: {diputado_mayoria[0]} ({getattr(diputado_mayoria[1], 'total', diputado_mayoria[1])} escaños)\n\n")
        self.analisis_text.tag_config('header', font=('Arial', 12, 'bold'))
        self.analisis_text.tag_config('subheader', font=('Arial', 11, 'bold'))
        self.analisis_text.tag_config('bold', font=('Arial', 10, 'bold'))
        self.analisis_text.config(state='disabled')

    def analizar_simulaciones(self, resultados_simulaciones, senadores_simulaciones, diputados_simulaciones):
        self.notebook.tab(self.analisis_frame, state='normal')
        self.notebook.select(self.analisis_frame)
        for widget in self.tendencias_frame.winfo_children():
            widget.destroy()
        ChartGenerator.create_distribution_chart(self.tendencias_frame, resultados_simulaciones).get_tk_widget().pack(fill='both', expand=True)
        self.analisis_text.config(state='normal')
        self.analisis_text.delete('1.0', 'end')
        self.analisis_text.insert('end', "ANÁLISIS ESTADÍSTICO DE SIMULACIONES\n\n", 'header')
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
        from collections import defaultdict
        frec_senadores = defaultdict(int)
        for sim in senadores_simulaciones:
            if sim:
                mayor = max(sim.items(), key=lambda x: getattr(x[1], 'total', x[1]))[0]
                frec_senadores[mayor] += 1
        self.analisis_text.insert('end', "\nFrecuencia de mayoría en Senado:\n", 'subheader')
        for partido, freq in sorted(frec_senadores.items(), key=lambda x: -x[1]):
            self.analisis_text.insert('end', f"- {partido}: {freq}/{len(senadores_simulaciones)} ({freq/len(senadores_simulaciones):.1%})\n")
        frec_diputados = defaultdict(int)
        for sim in diputados_simulaciones:
            if sim:
                mayor = max(sim.items(), key=lambda x: getattr(x[1], 'total', x[1]))[0]
                frec_diputados[mayor] += 1
        self.analisis_text.insert('end', "\nFrecuencia de mayoría en Diputados:\n", 'subheader')
        for partido, freq in sorted(frec_diputados.items(), key=lambda x: -x[1]):
            self.analisis_text.insert('end', f"- {partido}: {freq}/{len(diputados_simulaciones)} ({freq/len(diputados_simulaciones):.1%})\n")
        self.analisis_text.config(state='disabled')

    def exportar_excel(self):
        try:
            if not hasattr(self, 'resultados') or not self.resultados:
                messagebox.showerror("Error", "No hay resultados para exportar.")
                return
            df_resultados = pd.DataFrame({
                'Partido': list(self.resultados.keys()),
                'Votos': list(self.resultados.values()),
                'Porcentaje': [v/sum(self.resultados.values())*100 for v in self.resultados.values()]
            })
            if self.paridad_var.get():
                senadores_data = []
                for partido, datos in self.senadores.items():
                    senadores_data.append({
                        'Partido': partido,
                        'Total': datos.total,
                        'Mujeres': datos.mujeres,
                        'Hombres': datos.hombres
                    })
                diputados_data = []
                for partido, datos in self.diputados.items():
                    diputados_data.append({
                        'Partido': partido,
                        'Total': datos.total,
                        'Mujeres': datos.mujeres,
                        'Hombres': datos.hombres
                    })
            else:
                senadores_data = [{'Partido': p, 'Total': v} for p, v in self.senadores.items()]
                diputados_data = [{'Partido': p, 'Total': v} for p, v in self.diputados.items()]
            df_senadores = pd.DataFrame(senadores_data)
            df_diputados = pd.DataFrame(diputados_data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resultados_electorales_{timestamp}.xlsx"
            with pd.ExcelWriter(filename) as writer:
                df_resultados.to_excel(writer, sheet_name='Resultados', index=False)
                df_senadores.to_excel(writer, sheet_name='Senadores', index=False)
                df_diputados.to_excel(writer, sheet_name='Diputados', index=False)
                metadata = {
                    'Fecha': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    'Umbral mínimo': [f"{self.config.umbral_minimo*100}%"],
                    'Regla segunda vuelta': [self.segunda_vuelta_var.get()],
                    'Paridad de género': ['Sí' if self.paridad_var.get() else 'No'],
                    'Total senadores': [self.config.total_senadores],
                    'Total diputados': [self.config.total_diputados]
                }
                pd.DataFrame(metadata).to_excel(writer, sheet_name='Metadatos', index=False)
            self.export_status.config(text=f"Archivo guardado como: {filename}")
            messagebox.showinfo("Éxito", f"Resultados exportados a {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    def exportar_graficos(self):
        try:
            if not hasattr(self, 'resultados') or not self.resultados:
                messagebox.showerror("Error", "No hay gráficos para exportar.")
                return
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            import matplotlib.pyplot as plt
            porcentajes = {p: (v/sum(self.resultados.values()))*100 for p, v in self.resultados.items()}
            fig_pastel, ax_pastel = plt.subplots(figsize=(8, 6))
            datos_filtrados = {k: v for k, v in porcentajes.items() if v >= 1.0}
            otros = sum(v for v in porcentajes.values() if v < 1.0)
            if otros > 0:
                datos_filtrados['Otros'] = otros
            ax_pastel.pie(list(datos_filtrados.values()), labels=list(datos_filtrados.keys()), autopct='%1.1f%%', startangle=90)
            ax_pastel.set_title("Distribución de Votos por Partido")
            fig_pastel.savefig(f"grafico_pastel_{timestamp}.png", bbox_inches='tight')
            plt.close(fig_pastel)
            fig_senadores, ax_senadores = plt.subplots(figsize=(10, 6))
            if self.paridad_var.get():
                datos_senadores = {p: d.total for p, d in self.senadores.items()}
            else:
                datos_senadores = self.senadores
            partidos = list(datos_senadores.keys())
            valores = list(datos_senadores.values())
            bars = ax_senadores.bar(partidos, valores, color='#3498db')
            ax_senadores.set_title(f"Distribución de Senadores (Total {self.config.total_senadores})")
            for bar in bars:
                height = bar.get_height()
                ax_senadores.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom')
            if len(partidos) > 4:
                plt.setp(ax_senadores.get_xticklabels(), rotation=45, ha='right')
            fig_senadores.savefig(f"grafico_senadores_{timestamp}.png", bbox_inches='tight')
            plt.close(fig_senadores)
            self.export_status.config(text=f"Gráficos exportados (_{timestamp}.png)")
            messagebox.showinfo("Éxito", "Gráficos exportados como imágenes PNG")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron exportar los gráficos: {str(e)}")

    def generar_reporte(self):
        messagebox.showinfo("Información", "Esta funcionalidad está en desarrollo.")
        self.export_status.config(text="Generación de PDF en desarrollo") 