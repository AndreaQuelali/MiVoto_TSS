"""
Módulo para generar gráficos y visualizaciones de resultados electorales.
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, List, Union, Any
from ..simulation.dhondt_calculator import SeatAllocation


class ChartGenerator:
    """Clase para generar gráficos electorales"""
    
    @staticmethod
    def create_pie_chart(parent, data: Dict[str, float], title: str) -> FigureCanvasTkAgg:
        """
        Crea un gráfico de pastel
        
        Args:
            parent: Widget padre de Tkinter
            data: Diccionario con datos para el gráfico
            title: Título del gráfico
            
        Returns:
            Canvas de matplotlib integrado en Tkinter
        """
        fig, ax = plt.subplots(figsize=(6, 5))
        
        # Filtrar datos muy pequeños para mejorar la visualización
        datos_filtrados = {k: v for k, v in data.items() if v >= 1.0}
        otros = sum(v for v in data.values() if v < 1.0)
        
        if otros > 0:
            datos_filtrados['Otros'] = otros
        
        if not datos_filtrados:
            # Retornar un canvas vacío para cumplir el tipo
            fig.clf()
            return FigureCanvasTkAgg(fig, master=parent)
        
        # Obtener colores del colormap
        cmap = cm.get_cmap('tab20')
        colores = [cmap(i) for i in range(len(datos_filtrados))]
        
        # Unpacking seguro para pie
        pie_result = ax.pie(
            list(datos_filtrados.values()),
            labels=list(datos_filtrados.keys()),
            autopct=lambda p: f'{p:.1f}%' if p >= 5 else '',
            startangle=90,
            colors=colores,
            wedgeprops=dict(width=0.4, edgecolor='w'),
            pctdistance=0.85
        )
        
        if len(pie_result) == 3:
            wedges, texts, autotexts = pie_result
            plt.setp(autotexts, size=8, weight="bold")
            plt.setp(texts, size=8)
        else:
            wedges, texts = pie_result
            plt.setp(texts, size=8)
        
        ax.set_title(title)
        
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        return canvas
    
    @staticmethod
    def create_bar_chart(parent, data: Dict[str, Union[int, SeatAllocation]], 
                        title: str, color: str) -> FigureCanvasTkAgg:
        """
        Crea un gráfico de barras
        
        Args:
            parent: Widget padre de Tkinter
            data: Diccionario con datos para el gráfico
            title: Título del gráfico
            color: Color de las barras
            
        Returns:
            Canvas de matplotlib integrado en Tkinter
        """
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Extraer valores totales
        def get_total_value(value):
            if isinstance(value, int):
                return value
            return value.total
        
        # Ordenar datos
        partidos = [p for p, _ in sorted(data.items(), key=lambda x: -get_total_value(x[1]))]
        valores = [get_total_value(v) for _, v in sorted(data.items(), key=lambda x: -get_total_value(x[1]))]
        
        # Crear gráfico
        bars = ax.bar(partidos, valores, color=color)
        
        # Añadir valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Configurar ejes
        ax.set_title(title)
        ax.set_ylabel('Cantidad')
        if valores:
            ax.set_ylim(0, max(valores) * 1.2)
        
        # Rotar etiquetas si son muchas
        if len(partidos) > 4:
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        return canvas
    
    @staticmethod
    def create_trends_chart(parent, historical_data: Dict[str, List[tuple]]) -> FigureCanvasTkAgg:
        """
        Crea un gráfico de tendencias históricas
        
        Args:
            parent: Widget padre de Tkinter
            historical_data: Datos históricos por partido
            
        Returns:
            Canvas de matplotlib integrado en Tkinter
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Para cada partido, trazar su evolución
        for partido, data_points in historical_data.items():
            if data_points:  # Solo si hay datos para este partido
                años = [point[0] for point in data_points]
                porcentajes = [point[1] for point in data_points]
                ax.plot(años, porcentajes, 'o-', label=partido)
        
        # Configurar gráfico
        ax.set_title("Evolución Histórica de Votación por Partido")
        ax.set_ylabel("Porcentaje de Votos (%)")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        return canvas
    
    @staticmethod
    def create_distribution_chart(parent, simulation_results: List[Dict[str, float]]) -> FigureCanvasTkAgg:
        """
        Crea un gráfico de distribución de resultados de simulaciones
        
        Args:
            parent: Widget padre de Tkinter
            simulation_results: Lista de resultados de simulaciones
            
        Returns:
            Canvas de matplotlib integrado en Tkinter
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Preparar datos
        todos_partidos = set()
        for sim in simulation_results:
            todos_partidos.update(sim.keys())
        
        datos = {partido: [] for partido in todos_partidos}
        for sim in simulation_results:
            for partido in todos_partidos:
                datos[partido].append(sim.get(partido, 0))
        
        # Crear boxplot
        box = ax.boxplot(list(datos.values()), patch_artist=True)
        
        # Configurar gráfico
        ax.set_title("Distribución de Resultados en Simulaciones")
        ax.set_ylabel("Porcentaje de Votos")
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xticklabels(list(datos.keys()), rotation=45, ha='right')
        
        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        return canvas
    
    @staticmethod
    def save_chart_as_image(fig, filename: str):
        """
        Guarda un gráfico como imagen
        
        Args:
            fig: Figura de matplotlib
            filename: Nombre del archivo
        """
        fig.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close(fig) 