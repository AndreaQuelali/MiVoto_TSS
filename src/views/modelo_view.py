"""
Vista para la configuración del modelo predictivo
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Callable

from config.settings import (PESO_HISTORICO_DEFAULT, PESO_ENCUESTAS_DEFAULT, 
                              MARGEN_ERROR_PREDICCION_DEFAULT, TENDENCIA_AJUSTE_DEFAULT, 
                              UMBRAL_MINIMO_DEFAULT)


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
        self.frame = ctk.CTkFrame(self.parent)
        
        # Contenedor principal centrado
        contenedor = ctk.CTkFrame(self.frame)
        contenedor.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Título
        titulo_label = ctk.CTkLabel(
            contenedor, 
            text="Ajuste de Parámetros del Modelo Predictivo",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1a237e", "#bbdefb")
        )
        titulo_label.pack(pady=(10, 24))

        # Frame de ponderación
        frame_ponderacion = ctk.CTkFrame(contenedor)
        frame_ponderacion.pack(fill='x', padx=10, pady=12)
        ponderacion_label = ctk.CTkLabel(
            frame_ponderacion,
            text="Ponderación de Datos de Entrada",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#1565c0", "#90caf9")
        )
        ponderacion_label.grid(row=0, column=0, columnspan=3, pady=(12, 10))

        # Peso de datos históricos
        ctk.CTkLabel(frame_ponderacion, text="Peso de datos históricos (%):", font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.peso_hist_scale = ctk.CTkSlider(frame_ponderacion, from_=0, to=100, variable=self.peso_hist_var, command=self._update_pesos)
        self.peso_hist_scale.grid(row=1, column=1, sticky="ew", padx=10, pady=6)
        self.peso_hist_label = ctk.CTkLabel(frame_ponderacion, textvariable=self.peso_hist_var, font=ctk.CTkFont(size=12))
        self.peso_hist_label.grid(row=1, column=2, sticky="e", padx=10, pady=6)

        # Peso de encuestas
        ctk.CTkLabel(frame_ponderacion, text="Peso de encuestas 2025 (%):", font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w", padx=10, pady=6)
        self.peso_enc_scale = ctk.CTkSlider(frame_ponderacion, from_=0, to=100, variable=self.peso_enc_var, command=self._update_pesos)
        self.peso_enc_scale.grid(row=2, column=1, sticky="ew", padx=10, pady=6)
        self.peso_enc_label = ctk.CTkLabel(frame_ponderacion, textvariable=self.peso_enc_var, font=ctk.CTkFont(size=12))
        self.peso_enc_label.grid(row=2, column=2, sticky="e", padx=10, pady=6)
        frame_ponderacion.grid_columnconfigure(1, weight=1)

        # Frame de ajuste fino
        frame_ajuste = ctk.CTkFrame(contenedor)
        frame_ajuste.pack(fill='x', padx=10, pady=12)
        ajuste_label = ctk.CTkLabel(
            frame_ajuste,
            text="Variables de Ajuste Fino",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#1565c0", "#90caf9")
        )
        ajuste_label.grid(row=0, column=0, columnspan=2, pady=(12, 10))

        # Margen de error
        ctk.CTkLabel(frame_ajuste, text="Margen de error de predicción (%):", font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.margen_error_entry = ctk.CTkEntry(frame_ajuste, textvariable=self.margen_error_var, width=100, font=ctk.CTkFont(size=12))
        self.margen_error_entry.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        # Tendencia histórica
        ctk.CTkLabel(frame_ajuste, text="Tendencia histórica:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, sticky="w", padx=10, pady=6)
        self.tendencia_combobox = ctk.CTkOptionMenu(frame_ajuste, values=["Conservar", "Suavizar", "Acentuar"], variable=self.tendencia_var, font=ctk.CTkFont(size=12))
        self.tendencia_combobox.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        # Umbral mínimo
        ctk.CTkLabel(frame_ajuste, text="Umbral mínimo de votos para escaños (%):", font=ctk.CTkFont(size=12)).grid(row=3, column=0, sticky="w", padx=10, pady=6)
        self.umbral_minimo_entry = ctk.CTkEntry(frame_ajuste, textvariable=self.umbral_minimo_var, width=100, font=ctk.CTkFont(size=12))
        self.umbral_minimo_entry.grid(row=3, column=1, sticky="w", padx=10, pady=6)
        frame_ajuste.grid_columnconfigure(1, weight=1)

        # Botón para ejecutar predicción
        ejecutar_btn = ctk.CTkButton(
            contenedor, 
            text="EJECUTAR PREDICCIÓN ELECTORAL 2025",
            command=self.ejecutar_prediccion,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=44,
            width=340
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