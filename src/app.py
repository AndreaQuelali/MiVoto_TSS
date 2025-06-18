import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import pandas as pd
from openpyxl.drawing.image import Image
import random

class SimuladorElectoralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Electoral Bolivia 2025")
        self.root.geometry("1100x800")
        
        # Datos históricos de las elecciones 2020
        self.partidos_hist = {
            'MAS': 55.10,
            'CC': 28.83,
            'Creemos': 14.00,
            'FPV': 1.55,
            'PAN-BOL': 0.52
        }
        
        # Inicialización de las listas de votantes, resultados y escaños
        self.partidos = list(self.partidos_hist.keys())  # Lista de partidos pre-cargados
        self.resultados = defaultdict(int)
        self.senadores = defaultdict(int)
        self.diputados = defaultdict(int)
        
        # Configuración de la interfaz de Tkinter
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Número de escaños
        self.total_senadores = 36
        self.total_diputados = 130
        self.umbral_minimo = 0.03  # 3% mínimo para representación
        
        # Notebooks para las diferentes pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Resultados Históricos")
        self.setup_config_tab()
        
        self.resultados_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.resultados_frame, text="Gráficas Resultados", state='disabled')
        self.setup_resultados_tab()
        
        self.notebook.select(self.config_frame)
        self.mostrar_btn = ttk.Button(self.config_frame, 
                                      text="Mostrar Resultados Históricos", 
                                      command=self.mostrar_resultados_hist)
        self.mostrar_btn.pack(pady=10)
    
    def setup_config_tab(self):
        """Configura la pestaña de resultados históricos"""
        header = ttk.Label(self.config_frame, text="Resultados Históricos de Elecciones", style='Header.TLabel')
        header.pack(pady=10)
        
        partidos_frame = ttk.Frame(self.config_frame)
        partidos_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(partidos_frame, text="Partidos Cargados (Historico):").pack(anchor='w')
        
        # Mostrar los partidos históricos
        for partido in self.partidos_hist:
            ttk.Label(partidos_frame, text=partido).pack(anchor='w')

        # Campo para agregar nuevos partidos
        ttk.Label(partidos_frame, text="Agregar Nuevo Partido:").pack(anchor='w')
        
        self.nuevo_partido_entry = ttk.Entry(partidos_frame)
        self.nuevo_partido_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        add_btn = ttk.Button(partidos_frame, text="Agregar", command=self.agregar_partido)
        add_btn.pack(side='left', padx=5)
    
    def setup_resultados_tab(self):
        """Configura la pestaña de gráficos de resultados"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.resultados_frame)
        main_frame.pack(fill='both', expand=True)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Gráfico de pastel
        self.pie_frame = ttk.Frame(scrollable_frame)
        self.pie_frame.pack(fill='x', padx=20, pady=10)
        
        # Gráfico de senadores
        self.senadores_frame = ttk.Frame(scrollable_frame)
        self.senadores_frame.pack(fill='x', padx=20, pady=10)
        
        # Gráfico de diputados
        self.diputados_frame = ttk.Frame(scrollable_frame)
        self.diputados_frame.pack(fill='x', padx=20, pady=10)
        
        # Frame para detalles de resultados
        detalles_frame = ttk.Frame(scrollable_frame)
        detalles_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(detalles_frame, text="Resumen de Resultados:", style='Header.TLabel').pack(anchor='w')
        
        self.resultados_text = tk.Text(detalles_frame, height=12, state='disabled')
        self.resultados_text.pack(fill='x')
    
    def agregar_partido(self):
        """Agrega un nuevo partido a la lista"""
        nuevo_partido = self.nuevo_partido_entry.get().strip()
        if nuevo_partido:
            if nuevo_partido not in self.partidos_hist:
                # Asignar un porcentaje aleatorio entre 0% y 10% para el nuevo partido
                porcentaje_aleatorio = round(random.uniform(0, 10), 2)
                self.partidos_hist[nuevo_partido] = porcentaje_aleatorio
                self.partidos.append(nuevo_partido)
                
                # Actualizar la interfaz de la lista de partidos
                self.setup_config_tab()  # Vuelve a cargar la lista de partidos con el nuevo agregado
                
                messagebox.showinfo("Partido Agregado", f"El partido {nuevo_partido} ha sido agregado con un porcentaje de {porcentaje_aleatorio}%.")
                self.nuevo_partido_entry.delete(0, 'end')
            else:
                messagebox.showwarning("Partido Existente", "Este partido ya ha sido agregado.")
        else:
            messagebox.showwarning("Campo Vacío", "Por favor ingrese el nombre del partido.")
    
    def mostrar_resultados_hist(self):
        """Muestra los resultados históricos con gráficos"""
        # Calcular los resultados de los votos históricos
        self.resultados = defaultdict(int, self.partidos_hist)
        
        # Verificar si es necesario una segunda vuelta
        self.resultados_segunda_vuelta()
        
        # Asignar escaños utilizando el método D'Hondt
        self.senadores = self.asignar_escanos(self.resultados, self.total_senadores)
        self.diputados = self.asignar_escanos(self.resultados, self.total_diputados)
        
        # Habilitar pestaña de resultados
        self.notebook.tab(self.resultados_frame, state='normal')
        self.notebook.select(self.resultados_frame)
        
        # Mostrar resultados históricos en texto
        self.resultados_text.config(state='normal')
        self.resultados_text.delete('1.0', 'end')
        
        total_votos = sum(self.resultados.values())
        resultados_porcentaje = {p: (v / total_votos) * 100 for p, v in self.resultados.items()}
        
        self.resultados_text.insert('end', "RESULTADOS HISTÓRICOS - BOLIVIA 2020\n\n")
        self.resultados_text.insert('end', f"Total de votantes: {total_votos}\n\n")
        
        # Resultados por partido
        self.resultados_text.insert('end', "Resultados por Partido:\n")
        for partido, votos in sorted(self.resultados.items(), key=lambda x: -x[1]):
            porcentaje = resultados_porcentaje[partido]
            self.resultados_text.insert('end', f"- {partido}: {votos} votos ({porcentaje:.2f}%)\n")
        
        # Senadores
        self.resultados_text.insert('end', f"\nDistribución de Senadores (Total {self.total_senadores}):\n")
        for partido, escanos in sorted(self.senadores.items(), key=lambda x: -x[1]):
            self.resultados_text.insert('end', f"- {partido}: {escanos} senadores\n")
        
        # Diputados
        self.resultados_text.insert('end', f"\nDistribución de Diputados (Total {self.total_diputados}):\n")
        for partido, escanos in sorted(self.diputados.items(), key=lambda x: -x[1]):
            self.resultados_text.insert('end', f"- {partido}: {escanos} diputados\n")
        
        self.resultados_text.config(state='disabled')
        
        # Crear gráficos
        self.mostrar_graficos(resultados_porcentaje)
    
    def resultados_segunda_vuelta(self):
        """Verifica si es necesaria una segunda vuelta y ajusta los resultados"""
        total_votos = sum(self.resultados.values())
        umbral_primera_vuelta = 50  # 50% de los votos para ganar en la primera vuelta
        
        # Verificar si se necesita segunda vuelta
        if not any(voto > umbral_primera_vuelta for voto in self.resultados.values()):
            # Ordenar por votos y seleccionar los dos partidos más votados
            partidos_ordenados = sorted(self.resultados.items(), key=lambda x: x[1], reverse=True)
            primer_partido = partidos_ordenados[0]
            segundo_partido = partidos_ordenados[1]
            
            # Simular una segunda vuelta con solo estos dos partidos
            self.resultados = {
                primer_partido[0]: primer_partido[1],
                segundo_partido[0]: segundo_partido[1]
            }
            messagebox.showinfo("Segunda Vuelta", f"Se realizará una segunda vuelta entre {primer_partido[0]} y {segundo_partido[0]}.")
    
    def asignar_escanos(self, votos: dict, total_escanos: int) -> dict:
        """Asigna escaños usando el método D'Hondt"""
        total_votos = sum(votos.values())
        partidos_validos = {p: v for p, v in votos.items() if (v / total_votos) >= self.umbral_minimo}
        
        if not partidos_validos:
            return {}
        
        asignaciones = {p: 0 for p in partidos_validos}
        cocientes = {p: [] for p in partidos_validos}
        
        for _ in range(total_escanos):
            for partido in partidos_validos:
                n = asignaciones[partido] + 1
                cociente = votos[partido] / n
                cocientes[partido].append(cociente)
            
            max_cociente = -1
            partido_ganador = None
            
            for partido in partidos_validos:
                if cocientes[partido] and cocientes[partido][-1] > max_cociente:
                    max_cociente = cocientes[partido][-1]
                    partido_ganador = partido
            
            if partido_ganador:
                asignaciones[partido_ganador] += 1
        
        return asignaciones
    
    def mostrar_graficos(self, resultados_porcentaje):
        """Muestra todos los gráficos de resultados"""
        for widget in self.pie_frame.winfo_children():
            widget.destroy()
        for widget in self.senadores_frame.winfo_children():
            widget.destroy()
        for widget in self.diputados_frame.winfo_children():
            widget.destroy()
        
        # Gráfico de pastel para resultados generales
        self.crear_grafico_pastel(
            self.pie_frame,
            resultados_porcentaje,
            "Distribución General de Votos"
        )
        
        # Gráfico de barras para senadores
        self.crear_grafico_barras(
            self.senadores_frame,
            self.senadores,
            f"Distribución de Senadores (Total {self.total_senadores})",
            "#1f77b4"
        )
        
        # Gráfico de barras para diputados
        self.crear_grafico_barras(
            self.diputados_frame,
            self.diputados,
            f"Distribución de Diputados (Total {self.total_diputados})",
            "#ff7f0e"
        )
    
    def crear_grafico_pastel(self, frame, datos, titulo):
        """Crea un gráfico de pastel en el frame especificado"""
        fig, ax = plt.subplots(figsize=(6, 5))
        
        colores = plt.cm.Pastel1(range(len(datos)))
        
        wedges, texts, autotexts = ax.pie(
            datos.values(),
            labels=datos.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=colores,
            wedgeprops=dict(width=0.4, edgecolor='w'),
            pctdistance=0.85
        )
        
        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title(titulo)
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='x')
    
    def crear_grafico_barras(self, frame, datos, titulo, color):
        """Crea un gráfico de barras en el frame especificado"""
        partidos = [p for p, _ in sorted(datos.items(), key=lambda x: -x[1])]
        valores = [v for _, v in sorted(datos.items(), key=lambda x: -x[1])]
        
        fig, ax = plt.subplots(figsize=(8, 4))
        
        bars = ax.bar(partidos, valores, color=color)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        ax.set_title(titulo)
        ax.set_ylabel('Cantidad')
        ax.set_ylim(0, max(valores) * 1.2)
        
        if len(partidos) > 4:
            plt.xticks(rotation=45, ha='right')
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='x')

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorElectoralApp(root)
    root.mainloop()

