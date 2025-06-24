"""
Vista para la configuración del modelo predictivo
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from utils.style_utils import crear_scrollable_frame
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
        self.peso_hist_var = tk.DoubleVar(value=PESO_HISTORICO_DEFAULT * 100)
        self.peso_enc_var = tk.DoubleVar(value=PESO_ENCUESTAS_DEFAULT * 100)
        self.margen_error_var = tk.DoubleVar(value=MARGEN_ERROR_PREDICCION_DEFAULT * 100)
        self.tendencia_var = tk.StringVar(value=TENDENCIA_AJUSTE_DEFAULT)
        self.umbral_minimo_var = tk.DoubleVar(value=UMBRAL_MINIMO_DEFAULT * 100)
        
        # Widgets
        self.frame = None
        self.peso_hist_scale = None
        self.peso_enc_scale = None
        self.peso_hist_label = None
        self.peso_enc_label = None
        self.margen_error_spinbox = None
        self.tendencia_combobox = None
        self.umbral_minimo_spinbox = None
        
        self.crear_vista()
    
    def crear_vista(self):
        """Crea la vista del modelo."""
        self.frame = ttk.Frame(self.parent, padding="10")
        
        # Crear frame con scrollbar
        canvas, scrollbar, scrollable_frame = crear_scrollable_frame(self.frame)
        
        ttk.Label(scrollable_frame, text="Ajuste de Parámetros del Modelo Predictivo",
                  style='Header.TLabel').pack(pady=(10, 20))

        # Sección de ponderación de datos
        frame_ponderacion = ttk.LabelFrame(scrollable_frame, text="Ponderación de Datos de Entrada")
        frame_ponderacion.pack(fill='x', padx=10, pady=10, ipadx=5, ipady=5)

        ttk.Label(frame_ponderacion, text="Peso de datos históricos (%):", anchor='w').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.peso_hist_scale = ttk.Scale(frame_ponderacion, from_=0, to=100, orient='horizontal', 
                                        variable=self.peso_hist_var, command=self._update_pesos)
        self.peso_hist_scale.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.peso_hist_label = ttk.Label(frame_ponderacion, textvariable=self.peso_hist_var, width=5, anchor='e')
        self.peso_hist_label.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(frame_ponderacion, text="Peso de encuestas 2025 (%):", anchor='w').grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.peso_enc_scale = ttk.Scale(frame_ponderacion, from_=0, to=100, orient='horizontal', 
                                       variable=self.peso_enc_var, command=self._update_pesos)
        self.peso_enc_scale.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.peso_enc_label = ttk.Label(frame_ponderacion, textvariable=self.peso_enc_var, width=5, anchor='e')
        self.peso_enc_label.grid(row=1, column=2, padx=5, pady=5)

        frame_ponderacion.columnconfigure(1, weight=1)

        # Sección de variables de ajuste
        frame_ajuste = ttk.LabelFrame(scrollable_frame, text="Variables de Ajuste Fino")
        frame_ajuste.pack(fill='x', padx=10, pady=10, ipadx=5, ipady=5)

        ttk.Label(frame_ajuste, text="Margen de error de predicción (%):", anchor='w').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.margen_error_spinbox = ttk.Spinbox(frame_ajuste, from_=0, to=10, increment=0.1, 
                                               textvariable=self.margen_error_var, width=5)
        self.margen_error_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(frame_ajuste, text="%").grid(row=0, column=2, padx=2, pady=5, sticky='w')

        ttk.Label(frame_ajuste, text="Tendencia histórica:", anchor='w').grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.tendencia_combobox = ttk.Combobox(frame_ajuste, values=["Conservar", "Suavizar", "Acentuar"],
                                              textvariable=self.tendencia_var, state='readonly')
        self.tendencia_combobox.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        self.tendencia_combobox.set(TENDENCIA_AJUSTE_DEFAULT)

        ttk.Label(frame_ajuste, text="Umbral mínimo de votos para escaños (%):", anchor='w').grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        self.umbral_minimo_spinbox = ttk.Spinbox(frame_ajuste, from_=0, to=10, increment=0.1, 
                                                textvariable=self.umbral_minimo_var, width=5)
        self.umbral_minimo_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(frame_ajuste, text="%").grid(row=2, column=2, padx=2, pady=5, sticky='w')

        frame_ajuste.columnconfigure(1, weight=1)

        # Botón para ejecutar predicción
        ttk.Button(scrollable_frame, text="EJECUTAR PREDICCIÓN ELECTORAL 2025",
                   command=self.ejecutar_prediccion, style='TButton').pack(pady=30, ipadx=20, ipady=10)
    
    def _update_pesos(self, event=None):
        """Ajusta automáticamente el peso de la otra escala para que la suma sea 100%."""
        if event == self.peso_hist_scale:
            current_hist_weight = self.peso_hist_var.get()
            self.peso_enc_var.set(100 - current_hist_weight)
        elif event == self.peso_enc_scale:
            current_enc_weight = self.peso_enc_var.get()
            self.peso_hist_var.set(100 - current_enc_weight)
    
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