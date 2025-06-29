"""
Vista para la exportación de resultados
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, Callable, Optional

from utils.file_utils import exportar_a_excel
from utils.pdf_utils import generar_informe_pdf
from utils.logo_utils import logo_manager
from config.settings import EXCEL_FILE_TYPES, PDF_FILE_TYPES
from config.bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD,
    BOLIVIA_BG_CONTAINER, BOLIVIA_BG_FRAME
)


class ExportacionView:
    """
    Vista para la exportación de resultados.
    """
    
    def __init__(self, parent, prediccion_votos: Optional[Dict] = None, senadores: Optional[Dict] = None, 
                 diputados: Optional[Dict] = None):
        self.parent = parent
        self.prediccion_votos = prediccion_votos or {}
        self.senadores = senadores or {}
        self.diputados = diputados or {}
        self.diputados_plurinominales: Dict = {}
        self.diputados_uninominales: Dict = {}
        self.diputados_uninominales_por_depto: Dict = {}
        self.detalle_escanos: Dict = {}
        
        self.frame = None
        self.crear_vista()
    
    def crear_vista(self):
        """Crea la vista de exportación."""
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
            text="Opciones de Exportación de Resultados",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=(BOLIVIA_RED, BOLIVIA_RED)
        )
        titulo_label.pack(pady=(0, 24))

        # Frame para botones
        export_btn_frame = ctk.CTkFrame(contenedor, fg_color=BOLIVIA_BG_FRAME)
        export_btn_frame.pack(pady=30)

        # Botón para exportar a Excel
        excel_btn = ctk.CTkButton(
            export_btn_frame, 
            text="Exportar a Excel", 
            command=self.exportar_a_excel,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=44,
            width=220,
            fg_color=BOLIVIA_GREEN,
            hover_color=BOLIVIA_DARK_GREEN
        )
        excel_btn.pack(side='left', padx=24, pady=10)
        
        # Botón para generar PDF
        pdf_btn = ctk.CTkButton(
            export_btn_frame, 
            text="Generar Informe PDF", 
            command=self.generar_informe_pdf,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=44,
            width=220,
            fg_color=BOLIVIA_GREEN,
            hover_color=BOLIVIA_DARK_GREEN
        )
        pdf_btn.pack(side='left', padx=24, pady=10)
        
        # Información adicional
        info_label = ctk.CTkLabel(
            contenedor,
            text="Nota: Ejecute la predicción en la pestaña 'Configuración del Modelo' antes de exportar.\n\nLa exportación incluirá:\n• Resultados de votación\n• Distribución de senadores\n• Distribución de diputados (plurinominales y uninominales)\n• Detalle de escaños por departamento",
            font=ctk.CTkFont(size=12),
            text_color=(BOLIVIA_TEXT_DARK, BOLIVIA_TEXT_DARK),
            wraplength=500,
            justify="center"
        )
        info_label.pack(pady=30)
    
    def exportar_a_excel(self):
        """Exporta los resultados a un archivo Excel."""
        if not self.prediccion_votos:
            messagebox.showwarning("Advertencia", "Ejecute la predicción primero para exportar resultados.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=EXCEL_FILE_TYPES,
            title="Guardar resultados como Excel"
        )
        if not file_path:
            return

        try:
            # Crear diccionario con todos los datos de escaños
            datos_completos = {
                'prediccion_votos': self.prediccion_votos,
                'senadores': self.senadores,
                'diputados': self.diputados,
                'diputados_plurinominales': self.diputados_plurinominales,
                'diputados_uninominales': self.diputados_uninominales,
                'diputados_uninominales_por_depto': self.diputados_uninominales_por_depto,
                'detalle_escanos': self.detalle_escanos
            }
            
            exportar_a_excel(file_path, datos_completos)
            messagebox.showinfo("Éxito", f"Resultados exportados a '{file_path}' exitosamente.")
        except Exception as e:
            messagebox.showerror("Error de Exportación", str(e))
    
    def generar_informe_pdf(self):
        """Genera un informe PDF con los resultados."""
        if not self.prediccion_votos:
            messagebox.showwarning("Advertencia", "Ejecute la predicción primero para generar un informe PDF.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=PDF_FILE_TYPES,
            title="Guardar informe PDF"
        )
        if not file_path:
            return

        try:
            # Crear diccionario con todos los datos de escaños
            datos_completos = {
                'prediccion_votos': self.prediccion_votos,
                'senadores': self.senadores,
                'diputados': self.diputados,
                'diputados_plurinominales': self.diputados_plurinominales,
                'diputados_uninominales': self.diputados_uninominales,
                'diputados_uninominales_por_depto': self.diputados_uninominales_por_depto,
                'detalle_escanos': self.detalle_escanos
            }
            
            generar_informe_pdf(file_path, datos_completos)
            messagebox.showinfo("Éxito", f"Informe PDF generado en '{file_path}' exitosamente.")
        except Exception as e:
            messagebox.showerror("Error de PDF", str(e))
    
    def actualizar_datos(self, prediccion_votos: Dict, senadores: Dict, diputados: Dict, 
                        diputados_plurinominales: Optional[Dict] = None, 
                        diputados_uninominales: Optional[Dict] = None,
                        diputados_uninominales_por_depto: Optional[Dict] = None, 
                        detalle_escanos: Optional[Dict] = None):
        """Actualiza los datos para exportación incluyendo información detallada de escaños."""
        self.prediccion_votos = prediccion_votos
        self.senadores = senadores
        self.diputados = diputados
        self.diputados_plurinominales = diputados_plurinominales or {}
        self.diputados_uninominales = diputados_uninominales or {}
        self.diputados_uninominales_por_depto = diputados_uninominales_por_depto or {}
        self.detalle_escanos = detalle_escanos or {}
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame 