import customtkinter as ctk
from tkinter import ttk

from config.bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD,
    BOLIVIA_TAB_NORMAL, BOLIVIA_TAB_HOVER, BOLIVIA_TAB_SELECTED
)

class ReportesView:
    def __init__(self, parent, lista_partidos, obtener_datos_filtrados):
        self.parent = parent
        self.lista_partidos = lista_partidos
        self.obtener_datos_filtrados = obtener_datos_filtrados
        self.frame = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_WARM)
        self._crear_interfaz()

    def _crear_interfaz(self):
        titulo = ctk.CTkLabel(
            self.frame, 
            text="Reportes Filtrados por Partido", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=BOLIVIA_TEXT_DARK
        )
        titulo.pack(pady=(20, 10))

        # Mensaje explicativo
        explicacion = ctk.CTkLabel(
            self.frame,
            text="Filtra la información por partido para ver sus resultados y escaños obtenidos, incluyendo el detalle por departamento.",
            font=ctk.CTkFont(size=13),
            text_color=BOLIVIA_TEXT_DARK,
            wraplength=800,
            justify="center"
        )
        explicacion.pack(pady=(0, 18))

        descripcion = ctk.CTkLabel(
            self.frame,
            text="Selecciona un partido para ver su información detallada",
            font=ctk.CTkFont(size=14),
            text_color=BOLIVIA_TEXT_DARK
        )
        descripcion.pack(pady=(0, 20))

        filtro_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=10)
        filtro_frame.pack(pady=(0, 20), padx=20, fill="x")

        ctk.CTkLabel(
            filtro_frame, 
            text="Selecciona un partido:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=BOLIVIA_TEXT_DARK
        ).pack(side="left", padx=(20, 10), pady=20)
        
        self.combo_partidos = ctk.CTkComboBox(
            filtro_frame, 
            values=self.lista_partidos, 
            command=self.actualizar_tabla,
            width=200
        )
        self.combo_partidos.pack(side="left", padx=(0, 20), pady=20)
        
        if self.lista_partidos:
            self.combo_partidos.set(self.lista_partidos[0])

        # Frame para la tabla
        tabla_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=10)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tabla = ttk.Treeview(tabla_frame, columns=("clave", "valor"), show="headings", height=15)
        self.tabla.heading("clave", text="Dato")
        self.tabla.heading("valor", text="Valor")
        self.tabla.column("clave", width=300)
        self.tabla.column("valor", width=200)
        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)

        self.actualizar_tabla(self.combo_partidos.get())

    def actualizar_tabla(self, partido):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        datos = self.obtener_datos_filtrados(partido)
        if isinstance(datos, dict):
            for clave, valor in datos.items():
                self.tabla.insert("", "end", values=(clave, valor))
        elif isinstance(datos, list):
            for item in datos:
                self.tabla.insert("", "end", values=item)

    def obtener_frame(self):
        return self.frame 