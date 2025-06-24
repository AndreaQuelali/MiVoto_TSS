"""
Vista para la exportación de resultados
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Callable

from utils.file_utils import exportar_a_excel
from utils.pdf_utils import generar_informe_pdf
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
        self.frame = ttk.Frame(self.parent, padding="10")

        ttk.Label(self.frame, text="Opciones de Exportación de Resultados",
                  style='Header.TLabel').pack(pady=(10, 20))

        export_btn_frame = ttk.Frame(self.frame)
        export_btn_frame.pack(pady=20)

        ttk.Button(export_btn_frame, text="Exportar a Excel", command=self.exportar_a_excel,
                   style='TButton').pack(side='left', padx=15, ipadx=10, ipady=5)
        ttk.Button(export_btn_frame, text="Generar Informe PDF", command=self.generar_informe_pdf,
                   style='TButton').pack(side='left', padx=15, ipadx=10, ipady=5)
    
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