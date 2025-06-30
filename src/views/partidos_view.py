"""
Vista para mostrar información de partidos políticos y postulantes 2025
"""
import customtkinter as ctk
from typing import Dict, List
import webbrowser
from PIL import Image, ImageTk
import os

from config.bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD,
    BOLIVIA_TAB_NORMAL, BOLIVIA_TAB_HOVER, BOLIVIA_TAB_SELECTED
)
from config.settings import DEPARTAMENTOS_BOLIVIA


class PartidosView:
    """
    Vista para mostrar información detallada de partidos políticos y postulantes 2025
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color=BOLIVIA_BG_WARM)
        
        # Datos de partidos políticos 2025
        self.partidos_2025 = {
            'MAS': {
                'nombre_completo': 'Movimiento al Socialismo - Instrumento Político por la Soberanía de los Pueblos',
                'candidato_presidencial': 'Eduardo Del Castillo',
                'candidato_vicepresidencial': 'Milán Berna',
            },
            'UNIDAD': {
                'nombre_completo': 'Bloque de Unidad',
                'candidato_presidencial': 'Samuel Doria Medina',
                'candidato_vicepresidencial': 'José Luis Lupo',
            },
            'LIBRE': {
                'nombre_completo': 'Libertad y Democracia (Alianza Libre)',
                'candidato_presidencial': 'Jorge Quiroga',
                'candidato_vicepresidencial': 'Juan Pablo Velasco',
            },
            'ALIANZA_POPULAR': {
                'nombre_completo': 'Alianza Popular',
                'candidato_presidencial': 'Andrónico Rodríguez',
                'candidato_vicepresidencial': 'Mariana Prado',
            },
            'APB_SUMATE': {
                'nombre_completo': 'Autonomía Para Bolivia – Súmate',
                'candidato_presidencial': 'Manfred Reyes Villa',
                'candidato_vicepresidencial': 'Juan Carlos Medrano',
            },
            'PDC': {
                'nombre_completo': 'Partido Demócrata Cristiano',
                'candidato_presidencial': 'Rodrigo Paz Pereira',
                'candidato_vicepresidencial': 'Edman Lara',
            },
            'FP': {
                'nombre_completo': 'La Fuerza del Pueblo',
                'candidato_presidencial': 'Jhonny Fernández',
                'candidato_vicepresidencial': None,
            },
            'MORENA': {
                'nombre_completo': 'Movimiento de Renovación Nacional',
                'candidato_presidencial': 'Eva Copa',
                'candidato_vicepresidencial': 'Jorge Richter',
            },
            'NGP': {
                'nombre_completo': 'Nueva Generación Patriótica',
                'candidato_presidencial': 'Fidel Tapia',
                'candidato_vicepresidencial': None,
            },
            'LYP_ADN': {
                'nombre_completo': 'Libertad y Progreso (ADN)',
                'candidato_presidencial': 'Pavel Arancena Vargas',
                'candidato_vicepresidencial': 'Antonio Saravia',
            }
        }
        
        # Colores para cada partido
        self.colores_partidos = {
            'MAS': '#FF6B35',  # Naranja
            'UNIDAD': '#1E40AF',  # Azul
            'LIBRE': '#DC2626',  # Rojo
            'ALIANZA_POPULAR': '#059669',  # Verde
            'APB_SUMATE': '#7C3AED',  # Púrpura
            'PDC': '#1F2937',  # Gris oscuro
            'FP': '#F59E0B',  # Amarillo
            'MORENA': '#EF4444',  # Rojo claro
            'NGP': '#10B981',  # Verde claro
            'LYP_ADN': '#6366F1',  # Índigo
        }
        
        self.inicializar_interfaz()
    
    def inicializar_interfaz(self):
        """Inicializa la interfaz de la vista."""
        # Título principal
        titulo = ctk.CTkLabel(
            self.frame,
            text="Partidos Políticos y Candidatos",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=BOLIVIA_TEXT_DARK
        )
        titulo.pack(pady=(20, 10))
        
        # Mensaje explicativo
        explicacion = ctk.CTkLabel(
            self.frame,
            text="Consulta la información básica de los partidos políticos y sus principales candidatos para las elecciones generales 2025.",
            font=ctk.CTkFont(size=13),
            text_color=BOLIVIA_TEXT_DARK,
            wraplength=800,
            justify="center"
        )
        explicacion.pack(pady=(0, 18))
        
        # Descripción
        descripcion = ctk.CTkLabel(
            self.frame,
            text="Información de los principales partidos políticos de Bolivia",
            font=ctk.CTkFont(size=14),
            text_color=BOLIVIA_TEXT_DARK
        )
        descripcion.pack(pady=(0, 20))
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(
            self.frame,
            fg_color=BOLIVIA_BG_WARM,
            width=1200,
            height=700
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Crear secciones para cada partido
        for i, (partido_key, partido_data) in enumerate(self.partidos_2025.items()):
            self.crear_seccion_partido(main_frame, partido_key, partido_data, i)
    
    def crear_seccion_partido(self, parent, partido_key, partido_data, index):
        """Crea una sección para mostrar información de un partido."""
        # Frame principal del partido
        partido_frame = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=10
        )
        partido_frame.pack(fill="x", padx=10, pady=10)
        
        # Header del partido
        header_frame = ctk.CTkFrame(
            partido_frame,
            fg_color=self.colores_partidos[partido_key],
            corner_radius=10
        )
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Nombre del partido
        nombre_label = ctk.CTkLabel(
            header_frame,
            text=partido_data['nombre_completo'],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        nombre_label.pack(pady=10)
        
        # Información básica
        info_frame = ctk.CTkFrame(partido_frame, fg_color="white")
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Grid para información básica
        info_grid = ctk.CTkFrame(info_frame, fg_color="white")
        info_grid.pack(fill="x", padx=10, pady=10)
        
        # Candidatos presidenciales
        candidatos_frame = ctk.CTkFrame(info_grid, fg_color="#F3F4F6")
        candidatos_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            candidatos_frame,
            text="Candidatos Presidenciales:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=BOLIVIA_TEXT_DARK
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            candidatos_frame,
            text=f"Presidente: {partido_data['candidato_presidencial']}",
            font=ctk.CTkFont(size=12),
            text_color=BOLIVIA_TEXT_DARK
        ).pack()
        
        if partido_data['candidato_vicepresidencial']:
            ctk.CTkLabel(
                candidatos_frame,
                text=f"Vicepresidente: {partido_data['candidato_vicepresidencial']}",
                font=ctk.CTkFont(size=12),
                text_color=BOLIVIA_TEXT_DARK
            ).pack(pady=(0, 10))
        else:
            ctk.CTkLabel(
                candidatos_frame,
                text="Vicepresidente: No especificado",
                font=ctk.CTkFont(size=12),
                text_color=BOLIVIA_TEXT_DARK
            ).pack(pady=(0, 10))
    
    def obtener_frame(self):
        """Retorna el frame principal de la vista."""
        return self.frame 