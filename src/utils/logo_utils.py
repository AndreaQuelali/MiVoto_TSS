"""
Utilidades para el manejo del logo del sistema
"""
import os
import customtkinter as ctk
from PIL import Image, ImageTk


class LogoManager:
    """
    Clase para manejar el logo del sistema de manera centralizada.
    """
    
    def __init__(self):
        self.logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'logo.png')
        self.logo_image = None
        self.logo_photo = None
        self._cargar_logo()
    
    def _cargar_logo(self):
        """Carga el logo desde el archivo."""
        try:
            if os.path.exists(self.logo_path):
                # Cargar imagen con PIL
                self.logo_image = Image.open(self.logo_path)
                print(f"Logo cargado: {self.logo_image.size[0]}x{self.logo_image.size[1]} píxeles")
            else:
                print(f"Advertencia: No se encontró el logo en {self.logo_path}")
                print("Por favor, coloca tu archivo de logo como 'logo.png' en la carpeta src/assets/images/")
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
    
    def _redimensionar_manteniendo_proporciones(self, image, target_size):
        """
        Redimensiona la imagen manteniendo las proporciones originales.
        
        Args:
            image: Imagen PIL
            target_size: Tupla (ancho, alto) objetivo
        
        Returns:
            Imagen redimensionada
        """
        # Obtener dimensiones originales
        original_width, original_height = image.size
        target_width, target_height = target_size
        
        # Calcular proporciones
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        
        # Usar la proporción más pequeña para mantener aspect ratio
        ratio = min(width_ratio, height_ratio)
        
        # Calcular nuevas dimensiones
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # Redimensionar la imagen con mejor calidad
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crear una imagen cuadrada con fondo transparente
        square_image = Image.new('RGBA', target_size, (0, 0, 0, 0))
        
        # Centrar la imagen redimensionada en el cuadrado
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        
        # Pegar la imagen redimensionada en el centro
        square_image.paste(resized_image, (x_offset, y_offset), resized_image if resized_image.mode == 'RGBA' else None)
        
        return square_image
    
    def obtener_logo_widget(self, parent, size=(100, 100)):
        """
        Retorna un widget CTkLabel con el logo.
        
        Args:
            parent: Widget padre
            size: Tamaño del logo (ancho, alto)
        
        Returns:
            CTkLabel con el logo
        """
        if self.logo_image:
            try:
                # Usar tamaños más grandes para mejor calidad
                # Multiplicar el tamaño por 2 para mejor resolución
                high_res_size = (size[0] * 2, size[1] * 2)
                
                # Redimensionar manteniendo proporciones con alta resolución
                resized_image = self._redimensionar_manteniendo_proporciones(self.logo_image, high_res_size)
                
                # Convertir para CTk con el tamaño original
                logo_photo = ctk.CTkImage(light_image=resized_image, 
                                        dark_image=resized_image, 
                                        size=size)
                
                # Crear label sin borde y con fondo transparente
                logo_label = ctk.CTkLabel(parent, image=logo_photo, text="")
                logo_label.configure(fg_color="transparent")
                
                return logo_label
            except Exception as e:
                print(f"Error al procesar el logo: {e}")
                # Fallback a texto
                return self._crear_fallback_label(parent)
        else:
            # Fallback: crear un label con texto si no hay logo
            return self._crear_fallback_label(parent)
    
    def _crear_fallback_label(self, parent):
        """Crea un label de fallback con texto."""
        fallback_label = ctk.CTkLabel(
            parent, 
            text="LOGO", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1a237e", "#bbdefb")
        )
        fallback_label.configure(fg_color="transparent")
        return fallback_label
    
    def logo_disponible(self):
        """Retorna True si el logo está disponible."""
        return self.logo_image is not None


# Instancia global del logo manager
logo_manager = LogoManager() 