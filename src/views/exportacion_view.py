"""
Vista para la exportación de resultados
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, Callable

from utils.file_utils import exportar_a_excel
from utils.pdf_utils import generar_informe_pdf
from utils.logo_utils import logo_manager
from config.settings import EXCEL_FILE_TYPES, PDF_FILE_TYPES


class ExportacionView:
    """
    Vista para la exportación de resultados.
    """
    
    def __init__(self, parent, prediccion_votos: Dict = None, senadores: Dict = None, 
                 diputados: Dict = None):
        self.parent = parent
        self.prediccion_votos = prediccion_votos or {}
        self.senadores = senadores or {}
        self.diputados = diputados or {}
        
        self.frame = None
        self.crear_vista()
    
    def crear_vista(self):
        """Crea la vista de exportación."""
        self.frame = ctk.CTkFrame(self.parent)

        # Contenedor principal centrado
        contenedor = ctk.CTkFrame(self.frame)
        contenedor.pack(fill='both', expand=True, padx=30, pady=30)

        # Logo del sistema encima del título, sin borde
        logo_label = logo_manager.obtener_logo_widget(contenedor, size=(100, 100))
        logo_label.pack(pady=(0, 15))
        
        # Título debajo del logo, centrado
        titulo_label = ctk.CTkLabel(
            contenedor, 
            text="Opciones de Exportación de Resultados",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1a237e", "#bbdefb")
        )
        titulo_label.pack(pady=(0, 24))

        # Frame para botones
        export_btn_frame = ctk.CTkFrame(contenedor)
        export_btn_frame.pack(pady=30)

        # Botón para exportar a Excel
        excel_btn = ctk.CTkButton(
            export_btn_frame, 
            text="Exportar a Excel", 
            command=self.exportar_a_excel,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=44,
            width=220
        )
        excel_btn.pack(side='left', padx=24, pady=10)
        
        # Botón para generar PDF
        pdf_btn = ctk.CTkButton(
            export_btn_frame, 
            text="Generar Informe PDF", 
            command=self.generar_informe_pdf,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=44,
            width=220
        )
        pdf_btn.pack(side='left', padx=24, pady=10)
        
        # Información adicional
        info_label = ctk.CTkLabel(
            contenedor,
            text="Nota: Ejecute la predicción en la pestaña 'Configuración del Modelo' antes de exportar.",
            font=ctk.CTkFont(size=12),
            text_color=("#263238", "#b0bec5"),
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
            exportar_a_excel(file_path, self.prediccion_votos, self.senadores, self.diputados)
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
            generar_informe_pdf(file_path, self.prediccion_votos, self.senadores, self.diputados)
            messagebox.showinfo("Éxito", f"Informe PDF generado en '{file_path}' exitosamente.")
        except Exception as e:
            messagebox.showerror("Error de PDF", str(e))
    
    def actualizar_datos(self, prediccion_votos: Dict, senadores: Dict, diputados: Dict):
        """Actualiza los datos para exportación."""
        self.prediccion_votos = prediccion_votos
        self.senadores = senadores
        self.diputados = diputados
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame 