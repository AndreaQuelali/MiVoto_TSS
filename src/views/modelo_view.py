"""
Vista para la configuración del modelo predictivo
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Callable

from config.settings import (PESO_HISTORICO_DEFAULT, PESO_ENCUESTAS_DEFAULT, 
                              MARGEN_ERROR_PREDICCION_DEFAULT, TENDENCIA_AJUSTE_DEFAULT, 
                              UMBRAL_MINIMO_DEFAULT)
from utils.logo_utils import logo_manager
from config.bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD,
    BOLIVIA_BG_CONTAINER, BOLIVIA_BG_FRAME
)


class ModeloView:
    """
    Vista para la configuración del modelo predictivo.
    """
    
    def __init__(self, parent, on_ejecutar_prediccion: Callable = None):
        self.parent = parent
        self.on_ejecutar_prediccion = on_ejecutar_prediccion
        
        # Variables de control
        self.peso_hist_var = ctk.DoubleVar(value=PESO_HISTORICO_DEFAULT * 100)
        self.peso_enc_var = ctk.DoubleVar(value=PESO_ENCUESTAS_DEFAULT * 100)
        self.margen_error_var = ctk.DoubleVar(value=MARGEN_ERROR_PREDICCION_DEFAULT * 100)
        self.tendencia_var = ctk.StringVar(value=TENDENCIA_AJUSTE_DEFAULT)
        self.umbral_minimo_var = ctk.DoubleVar(value=UMBRAL_MINIMO_DEFAULT * 100)
        
        # Widgets
        self.frame = None
        self.peso_hist_scale = None
        self.peso_enc_scale = None
        self.peso_hist_label = None
        self.peso_enc_label = None
        self.margen_error_entry = None
        self.tendencia_combobox = None
        self.umbral_minimo_entry = None
        
        self.crear_vista()
    
    def crear_vista(self):
        """Crea la vista del modelo."""
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
            text="Ajuste de Parámetros del Modelo Predictivo",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=(BOLIVIA_RED, BOLIVIA_RED)
        )
        titulo_label.pack(pady=(0, 24))

        # Mensaje explicativo
        explicacion = ctk.CTkLabel(
            contenedor,
            text="Ajusta los parámetros del modelo predictivo según tu criterio. Puedes modificar la ponderación entre datos históricos y encuestas, el margen de error, la tendencia y el umbral mínimo de votos para asignación de escaños.",
            font=ctk.CTkFont(size=13),
            text_color=BOLIVIA_TEXT_DARK,
            wraplength=800,
            justify="center"
        )
        explicacion.pack(pady=(0, 18))

        # Frame de ponderación
        frame_ponderacion = ctk.CTkFrame(contenedor, fg_color=BOLIVIA_BG_FRAME)
        frame_ponderacion.pack(fill='x', padx=10, pady=12)
        ponderacion_label = ctk.CTkLabel(
            frame_ponderacion,
            text="Ponderación de Datos de Entrada",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=(BOLIVIA_DARK_GREEN, BOLIVIA_DARK_GREEN)
        )
        ponderacion_label.grid(row=0, column=0, columnspan=3, pady=(12, 10))

        # Peso de datos históricos
        ctk.CTkLabel(frame_ponderacion, text="Peso de datos históricos (%):", font=ctk.CTkFont(size=12), text_color=(BOLIVIA_TEXT_DARK, BOLIVIA_TEXT_DARK)).grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.peso_hist_scale = ctk.CTkSlider(frame_ponderacion, from_=0, to=100, variable=self.peso_hist_var, command=self._update_pesos, progress_color=BOLIVIA_GREEN, button_color=BOLIVIA_DARK_GREEN)
        self.peso_hist_scale.grid(row=1, column=1, sticky="ew", padx=10, pady=6)
        self.peso_hist_label = ctk.CTkLabel(frame_ponderacion, textvariable=self.peso_hist_var, font=ctk.CTkFont(size=12), text_color=(BOLIVIA_TEXT_DARK, BOLIVIA_TEXT_DARK))
        self.peso_hist_label.grid(row=1, column=2, sticky="e", padx=10, pady=6)

        # Peso de encuestas
        ctk.CTkLabel(frame_ponderacion, text="Peso de encuestas 2025 (%):", font=ctk.CTkFont(size=12), text_color=(BOLIVIA_TEXT_DARK, BOLIVIA_TEXT_DARK)).grid(row=2, column=0, sticky="w", padx=10, pady=6)
        self.peso_enc_scale = ctk.CTkSlider(frame_ponderacion, from_=0, to=100, variable=self.peso_enc_var, command=self._update_pesos, progress_color=BOLIVIA_GREEN, button_color=BOLIVIA_DARK_GREEN)
        self.peso_enc_scale.grid(row=2, column=1, sticky="ew", padx=10, pady=6)
        self.peso_enc_label = ctk.CTkLabel(frame_ponderacion, textvariable=self.peso_enc_var, font=ctk.CTkFont(size=12), text_color=(BOLIVIA_TEXT_DARK, BOLIVIA_TEXT_DARK))
        self.peso_enc_label.grid(row=2, column=2, sticky="e", padx=10, pady=6)
        frame_ponderacion.grid_columnconfigure(1, weight=1)

        # Frame de ajuste fino
        frame_ajuste = ctk.CTkFrame(contenedor, fg_color=BOLIVIA_BG_FRAME)
        frame_ajuste.pack(fill='x', padx=10, pady=12)
        ajuste_label = ctk.CTkLabel(
            frame_ajuste,
            text="Variables de Ajuste Fino",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=(BOLIVIA_DARK_GREEN, BOLIVIA_DARK_GREEN)
        )
        ajuste_label.grid(row=0, column=0, columnspan=2, pady=(12, 10))

        # Margen de error
        ctk.CTkLabel(frame_ajuste, text="Margen de error de predicción (%):", font=ctk.CTkFont(size=12), text_color=(BOLIVIA_TEXT_DARK, BOLIVIA_TEXT_DARK)).grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.margen_error_entry = ctk.CTkEntry(frame_ajuste, textvariable=self.margen_error_var, width=100, font=ctk.CTkFont(size=12), fg_color="white", text_color=BOLIVIA_TEXT_DARK)
        self.margen_error_entry.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        # Tendencia histórica
        ctk.CTkLabel(frame_ajuste, text="Tendencia histórica:", font=ctk.CTkFont(size=12), text_color=(BOLIVIA_TEXT_DARK, BOLIVIA_TEXT_DARK)).grid(row=2, column=0, sticky="w", padx=10, pady=6)
        self.tendencia_combobox = ctk.CTkOptionMenu(frame_ajuste, values=["Conservar", "Suavizar", "Acentuar"], variable=self.tendencia_var, font=ctk.CTkFont(size=12), fg_color=BOLIVIA_GREEN, button_color=BOLIVIA_DARK_GREEN)
        self.tendencia_combobox.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        # Umbral mínimo
        ctk.CTkLabel(frame_ajuste, text="Umbral mínimo de votos para escaños (%):", font=ctk.CTkFont(size=12), text_color=(BOLIVIA_TEXT_DARK, BOLIVIA_TEXT_DARK)).grid(row=3, column=0, sticky="w", padx=10, pady=6)
        self.umbral_minimo_entry = ctk.CTkEntry(frame_ajuste, textvariable=self.umbral_minimo_var, width=100, font=ctk.CTkFont(size=12), fg_color="white", text_color=BOLIVIA_TEXT_DARK)
        self.umbral_minimo_entry.grid(row=3, column=1, sticky="w", padx=10, pady=6)
        frame_ajuste.grid_columnconfigure(1, weight=1)

        # Botón para ejecutar predicción
        ejecutar_btn = ctk.CTkButton(
            contenedor, 
            text="EJECUTAR PREDICCIÓN ELECTORAL 2025",
            command=self.ejecutar_prediccion,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=44,
            width=340,
            fg_color=BOLIVIA_RED,
            hover_color=BOLIVIA_DARK_GREEN
        )
        ejecutar_btn.pack(pady=36)
    
    def _update_pesos(self, value):
        """Ajusta automáticamente el peso de la otra escala para que la suma sea 100%."""
        # Esta función se llamará cuando se mueva cualquiera de los sliders
        # Por simplicidad, no implementamos la lógica automática aquí
        pass
    
    def ejecutar_prediccion(self):
        """Ejecuta la predicción con los parámetros configurados."""
        if self.on_ejecutar_prediccion:
            self.on_ejecutar_prediccion()
    
    def obtener_parametros(self):
        """
        Obtiene los parámetros configurados en la vista.
        
        Returns:
            dict: Diccionario con los parámetros del modelo
        """
        return {
            'peso_historico': self.peso_hist_var.get() / 100,
            'peso_encuestas': self.peso_enc_var.get() / 100,
            'margen_error': self.margen_error_var.get() / 100,
            'tendencia': self.tendencia_var.get(),
            'umbral_minimo': self.umbral_minimo_var.get() / 100
        }
    
    def obtener_frame(self):
        """Retorna el frame de la vista."""
        return self.frame 