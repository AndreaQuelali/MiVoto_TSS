"""
Controlador principal de la aplicación
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Dict

from models.electoral_model import ModeloPredictivoElectoral
from views.introduccion_view import IntroduccionView
from views.datos_view import DatosView
from views.modelo_view import ModeloView
from views.resultados_view import ResultadosView
from views.exportacion_view import ExportacionView
from views.detalle_escanos_view import DetalleEscanosView
from views.partidos_view import PartidosView
from views.reportes_view import ReportesView
from config.settings import (WINDOW_TITLE, WINDOW_SIZE, DATOS_HISTORICOS_DEFAULT, 
                              ENCUESTAS_2025_DEFAULT, TOTAL_SENADORES, TOTAL_DIPUTADOS)
from config.bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD,
    BOLIVIA_TAB_NORMAL, BOLIVIA_TAB_HOVER, BOLIVIA_TAB_SELECTED,
    BOLIVIA_TAB_TEXT_NORMAL, BOLIVIA_TAB_TEXT_SELECTED
)


class MainController:
    """
    Controlador principal que coordina todas las vistas y el modelo.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # Configurar color de fondo de la ventana principal
        self.root.configure(fg_color=BOLIVIA_BG_WARM)
        
        # Inicializar modelo
        self.modelo = ModeloPredictivoElectoral()
        self.modelo.cargar_datos_historicos(DATOS_HISTORICOS_DEFAULT)
        self.modelo.cargar_encuestas(ENCUESTAS_2025_DEFAULT)
        
        # Variables de estado
        self.tabview = None
        self.intro_view = None
        self.datos_view = None
        self.modelo_view = None
        self.resultados_view = None
        self.exportacion_view = None
        self.detalle_escanos_view = None
        self.partidos_view = None
        self.reportes_view = None
        
        # Inicializar interfaz
        self.inicializar_interfaz()
    
    def inicializar_interfaz(self):
        """Inicializa la interfaz principal de la aplicación."""
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configurar colores de las pestañas
        self.tabview.configure(
            fg_color=BOLIVIA_BG_WARM,
            segmented_button_fg_color=BOLIVIA_TAB_NORMAL,
            segmented_button_selected_color=BOLIVIA_TAB_SELECTED,
            segmented_button_selected_hover_color=BOLIVIA_TAB_SELECTED,
            segmented_button_unselected_color=BOLIVIA_TAB_NORMAL,
            segmented_button_unselected_hover_color=BOLIVIA_TAB_HOVER,
            text_color=BOLIVIA_TAB_TEXT_NORMAL,
            text_color_disabled=BOLIVIA_TAB_TEXT_NORMAL
        )
        
        # Crear vistas
        self.crear_vistas()
        
        # Seleccionar pestaña inicial
        self.tabview.set("Introducción")
    
    def crear_vistas(self):
        """Crea todas las vistas de la aplicación."""
        # Introducción
        self.tabview.add("Introducción")
        intro_tab = self.tabview.tab("Introducción")
        self.intro_view = IntroduccionView(intro_tab)
        self.intro_view.obtener_frame().pack(fill="both", expand=True)

        # Datos Históricos y Encuestas
        self.tabview.add("Datos Históricos y Encuestas")
        datos_tab = self.tabview.tab("Datos Históricos y Encuestas")
        self.datos_view = DatosView(
            datos_tab,
            self.modelo.datos_historicos,
            self.modelo.encuestas_2025,
            self.on_datos_actualizados
        )
        self.datos_view.obtener_frame().pack(fill="both", expand=True)

        # Configuración del Modelo
        self.tabview.add("Configuración del Modelo")
        modelo_tab = self.tabview.tab("Configuración del Modelo")
        self.modelo_view = ModeloView(modelo_tab, self.ejecutar_prediccion)
        self.modelo_view.obtener_frame().pack(fill="both", expand=True)

        # Resultados de Predicción
        self.tabview.add("Resultados de Predicción")
        resultados_tab = self.tabview.tab("Resultados de Predicción")
        self.resultados_view = ResultadosView(resultados_tab, self.simular_segunda_vuelta)
        self.resultados_view.obtener_frame().pack(fill="both", expand=True)

        # Detalle de Escaños
        self.tabview.add("Detalle de Escaños")
        detalle_escanos_tab = self.tabview.tab("Detalle de Escaños")
        self.detalle_escanos_view = DetalleEscanosView(detalle_escanos_tab)
        self.detalle_escanos_view.obtener_frame().pack(fill="both", expand=True)

        # Partidos Políticos y Postulantes
        self.tabview.add("Partidos y Postulantes")
        partidos_tab = self.tabview.tab("Partidos y Postulantes")
        self.partidos_view = PartidosView(partidos_tab)
        self.partidos_view.obtener_frame().pack(fill="both", expand=True)

        # Reportes
        self.tabview.add("Reportes")
        reportes_tab = self.tabview.tab("Reportes")
        self.reportes_view = ReportesView(
            reportes_tab,
            self.get_lista_partidos(),
            self.get_datos_filtrados_por_partido
        )
        self.reportes_view.obtener_frame().pack(fill="both", expand=True)

        # Exportar Resultados (movido al final)
        self.tabview.add("Exportar Resultados")
        exportar_tab = self.tabview.tab("Exportar Resultados")
        self.exportacion_view = ExportacionView(exportar_tab)
        self.exportacion_view.obtener_frame().pack(fill="both", expand=True)
    
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
            
            # Cambiar a pestaña de resultados
            self.tabview.set("Resultados de Predicción")
            
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
            resultados['candidatos_segunda_vuelta'],
            resultados.get('diputados_plurinominales'),
            resultados.get('diputados_uninominales'),
            resultados.get('diputados_uninominales_por_depto')
        )
        
        # Actualizar vista de detalle de escaños
        if self.detalle_escanos_view and 'detalle_escanos' in resultados:
            self.detalle_escanos_view.actualizar_detalle(resultados['detalle_escanos'])
        
        # Actualizar vista de exportación con todos los datos de escaños
        self.exportacion_view.actualizar_datos(
            resultados['prediccion_votos'],
            resultados['senadores'],
            resultados['diputados'],
            resultados.get('diputados_plurinominales'),
            resultados.get('diputados_uninominales'),
            resultados.get('diputados_uninominales_por_depto'),
            resultados.get('detalle_escanos')
        )
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.root.mainloop() 
    
    def get_lista_partidos(self):
        # Solo partidos presentes en las encuestas actuales
        if self.modelo.encuestas_2025:
            partidos = set()
            for e in self.modelo.encuestas_2025.values():
                partidos.update(e.keys())
            return list(partidos)
        else:
            return []

    def get_datos_filtrados_por_partido(self, partido):
        # Devuelve los datos relevantes del partido seleccionado
        datos = {}
        if self.modelo.prediccion_2025 and partido in self.modelo.prediccion_2025:
            datos['Predicción de votos (%)'] = round(self.modelo.prediccion_2025[partido], 2)
        if self.modelo.senadores_2025 and partido in self.modelo.senadores_2025:
            datos['Senadores'] = self.modelo.senadores_2025[partido]
        if self.modelo.diputados_2025 and partido in self.modelo.diputados_2025:
            datos['Diputados'] = self.modelo.diputados_2025[partido]
        # Agregar escaños por departamento
        if self.modelo.diputados_uninominales_por_depto_2025:
            for depto, partidos in self.modelo.diputados_uninominales_por_depto_2025.items():
                if partido in partidos:
                    datos[f"Diputados uninominales en {depto}"] = partidos[partido]
        return datos