"""
Controlador principal de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict

from models.electoral_model import ModeloPredictivoElectoral
from views.introduccion_view import IntroduccionView
from views.datos_view import DatosView
from views.modelo_view import ModeloView
from views.resultados_view import ResultadosView
from views.exportacion_view import ExportacionView
from utils.style_utils import configurar_estilos
from config.settings import (WINDOW_TITLE, WINDOW_SIZE, DATOS_HISTORICOS_DEFAULT, 
                              ENCUESTAS_2025_DEFAULT, TOTAL_SENADORES, TOTAL_DIPUTADOS)


class MainController:
    """
    Controlador principal que coordina todas las vistas y el modelo.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.option_add('*tearOff', False)
        
        # Configurar estilos
        self.style = configurar_estilos()
        
        # Inicializar modelo
        self.modelo = ModeloPredictivoElectoral()
        self.modelo.cargar_datos_historicos(DATOS_HISTORICOS_DEFAULT)
        self.modelo.cargar_encuestas(ENCUESTAS_2025_DEFAULT)
        
        # Variables de estado
        self.notebook = None
        self.intro_view = None
        self.datos_view = None
        self.modelo_view = None
        self.resultados_view = None
        self.exportacion_view = None
        
        # Inicializar interfaz
        self.inicializar_interfaz()
    
    def inicializar_interfaz(self):
        """Inicializa la interfaz principal de la aplicación."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear vistas
        self.crear_vistas()
        
        # Configurar pestañas iniciales
        self.notebook.select(0)
        self.notebook.tab(self.resultados_view.obtener_frame(), state='disabled')
        self.notebook.tab(self.exportacion_view.obtener_frame(), state='disabled')
    
    def crear_vistas(self):
        """Crea todas las vistas de la aplicación."""
        # Vista de introducción
        self.intro_view = IntroduccionView(self.notebook)
        self.notebook.add(self.intro_view.obtener_frame(), text="Introducción")
        
        # Vista de datos
        self.datos_view = DatosView(
            self.notebook, 
            self.modelo.datos_historicos, 
            self.modelo.encuestas_2025,
            self.on_datos_actualizados
        )
        self.notebook.add(self.datos_view.obtener_frame(), text="Datos Históricos y Encuestas")
        
        # Vista del modelo
        self.modelo_view = ModeloView(self.notebook, self.ejecutar_prediccion)
        self.notebook.add(self.modelo_view.obtener_frame(), text="Configuración del Modelo")
        
        # Vista de resultados
        self.resultados_view = ResultadosView(self.notebook, self.simular_segunda_vuelta)
        self.notebook.add(self.resultados_view.obtener_frame(), text="Resultados de Predicción")
        
        # Vista de exportación
        self.exportacion_view = ExportacionView(self.notebook)
        self.notebook.add(self.exportacion_view.obtener_frame(), text="Exportar Resultados")
    
    def on_datos_actualizados(self):
        """Callback cuando se actualizan los datos."""
        # Actualizar modelo con nuevos datos
        self.modelo.cargar_datos_historicos(self.datos_view.datos_historicos)
        self.modelo.cargar_encuestas(self.datos_view.encuestas_2025)
    
    def ejecutar_prediccion(self):
        """Ejecuta la predicción electoral."""
        try:
            # Obtener parámetros de la vista
            parametros = self.modelo_view.obtener_parametros()
            
            # Validar parámetros
            if (parametros['peso_historico'] + parametros['peso_encuestas']) == 0:
                messagebox.showerror("Error de Parámetros", 
                                   "La suma de los pesos de datos históricos y encuestas no puede ser cero.")
                return
            
            # Configurar modelo
            self.modelo.configurar_parametros(
                parametros['peso_historico'],
                parametros['peso_encuestas'],
                parametros['margen_error'],
                parametros['tendencia'],
                parametros['umbral_minimo']
            )
            
            # Ejecutar predicción
            self.modelo.ejecutar_prediccion()
            
            # Obtener resultados
            resultados = self.modelo.obtener_resultados()
            
            # Actualizar vistas
            self.actualizar_vistas_con_resultados(resultados)
            
            # Habilitar pestañas de resultados
            self.notebook.tab(self.resultados_view.obtener_frame(), state='normal')
            self.notebook.tab(self.exportacion_view.obtener_frame(), state='normal')
            
            # Cambiar a pestaña de resultados
            self.notebook.select(self.resultados_view.obtener_frame())
            
            messagebox.showinfo("Predicción Completa", 
                              "El modelo predictivo ha sido ejecutado exitosamente. ¡Consulte la pestaña de Resultados!")
            
        except ValueError as ve:
            messagebox.showerror("Error de Datos", f"Verifique la exactitud de sus datos: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error en Predicción", f"Ocurrió un error inesperado durante la predicción: {str(e)}")
    
    def simular_segunda_vuelta(self):
        """Simula la segunda vuelta electoral."""
        try:
            prediccion_segunda_vuelta = self.modelo.simular_segunda_vuelta()
            
            if prediccion_segunda_vuelta:
                # Determinar ganador
                candidatos = list(prediccion_segunda_vuelta.keys())
                votos = list(prediccion_segunda_vuelta.values())
                
                if votos[0] > votos[1]:
                    ganador = candidatos[0]
                else:
                    ganador = candidatos[1]
                
                messagebox.showinfo("Resultado Segunda Vuelta", 
                                  f"Ganador de la segunda vuelta: {ganador}\n\n"
                                  f"{candidatos[0]}: {votos[0]:.1f}%\n"
                                  f"{candidatos[1]}: {votos[1]:.1f}%")
            else:
                messagebox.showwarning("Segunda Vuelta", "No se puede simular la segunda vuelta con los datos actuales.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al simular segunda vuelta: {str(e)}")
    
    def actualizar_vistas_con_resultados(self, resultados: Dict):
        """Actualiza las vistas con los resultados de la predicción."""
        # Actualizar vista de resultados
        self.resultados_view.actualizar_resultados(
            resultados['prediccion_votos'],
            resultados['senadores'],
            resultados['diputados'],
            resultados['segunda_vuelta'],
            resultados['candidatos_segunda_vuelta']
        )
        
        # Actualizar vista de exportación
        self.exportacion_view.actualizar_datos(
            resultados['prediccion_votos'],
            resultados['senadores'],
            resultados['diputados']
        )
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.root.mainloop() 