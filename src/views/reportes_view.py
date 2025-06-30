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
        self.check_vars = {}
        self.checkboxes = []
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
            text="Selecciona uno o más partidos para comparar sus resultados y escaños obtenidos, incluyendo el detalle por departamento.",
            font=ctk.CTkFont(size=13),
            text_color=BOLIVIA_TEXT_DARK,
            wraplength=800,
            justify="center"
        )
        explicacion.pack(pady=(0, 18))

        filtro_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=10)
        filtro_frame.pack(pady=(0, 20), padx=20, fill="x")

        ctk.CTkLabel(
            filtro_frame, 
            text="Selecciona partidos:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=BOLIVIA_TEXT_DARK
        ).pack(anchor="w", padx=(20, 10), pady=(20, 0))

        # Frame para los checkboxes
        checks_frame = ctk.CTkFrame(filtro_frame, fg_color="white")
        checks_frame.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

        self.check_vars = {}
        self.checkboxes = []
        for partido in self.lista_partidos:
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(
                checks_frame, text=partido, variable=var,
                font=ctk.CTkFont(size=13), text_color=BOLIVIA_TEXT_DARK,
                command=self.actualizar_tabla
            )
            chk.pack(anchor="w", pady=2)
            self.check_vars[partido] = var
            self.checkboxes.append(chk)
        # Seleccionar el primero por defecto
        if self.lista_partidos:
            self.check_vars[self.lista_partidos[0]].set(True)

        # Botones seleccionar/deseleccionar todos
        btns_frame = ctk.CTkFrame(filtro_frame, fg_color="white")
        btns_frame.pack(anchor="w", padx=20, pady=(0, 10))
        ctk.CTkButton(btns_frame, text="Seleccionar todos", command=self.seleccionar_todos, width=140, fg_color=BOLIVIA_GREEN, hover_color=BOLIVIA_DARK_GREEN).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btns_frame, text="Deseleccionar todos", command=self.deseleccionar_todos, width=160, fg_color=BOLIVIA_RED, hover_color=BOLIVIA_DARK_GREEN).pack(side="left")

        # Frame para la tabla
        tabla_frame = ctk.CTkFrame(self.frame, fg_color="white", corner_radius=10)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Columnas base
        self.columnas_base = ["Partido", "Predicción de votos (%)", "Senadores", "Diputados"]
        self.tabla = ttk.Treeview(tabla_frame, columns=self.columnas_base, show="headings", height=15)
        for col in self.columnas_base:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=180)
        self.tabla.pack(fill="both", expand=True, padx=20, pady=20)

        self.actualizar_tabla()

    def seleccionar_todos(self):
        for var in self.check_vars.values():
            var.set(True)
        self.actualizar_tabla()

    def deseleccionar_todos(self):
        for var in self.check_vars.values():
            var.set(False)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        seleccion = [p for p, var in self.check_vars.items() if var.get()]
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        # Determinar columnas extra (escaños por departamento)
        columnas_extra = set()
        datos_partidos = {}
        for partido in seleccion:
            datos = self.obtener_datos_filtrados(partido)
            datos_partidos[partido] = datos
            for clave in datos.keys():
                if clave.startswith("Diputados uninominales en "):
                    columnas_extra.add(clave)
        # Actualizar columnas de la tabla
        todas_columnas = self.columnas_base + sorted(columnas_extra)
        self.tabla.config(columns=todas_columnas)
        for col in todas_columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=180)
        # Insertar filas
        for partido in seleccion:
            datos = datos_partidos[partido]
            fila = [partido]
            for col in self.columnas_base[1:]:
                fila.append(datos.get(col, "-"))
            for col in sorted(columnas_extra):
                fila.append(datos.get(col, "-"))
            self.tabla.insert("", "end", values=fila)

    def obtener_frame(self):
        return self.frame 