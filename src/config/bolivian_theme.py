"""
Temática de colores bolivianos para la aplicación
Basada en la bandera de Bolivia y elementos representativos del país
"""

# Colores de la bandera de Bolivia
BOLIVIA_RED = "#DA291C"      # Rojo de la bandera
BOLIVIA_YELLOW = "#F4E400"   # Amarillo de la bandera  
BOLIVIA_GREEN = "#007934"    # Verde de la bandera

# Colores complementarios bolivianos
BOLIVIA_DARK_RED = "#B22222"     # Rojo oscuro
BOLIVIA_DARK_GREEN = "#006400"   # Verde oscuro
BOLIVIA_GOLD = "#FFD700"         # Dorado
BOLIVIA_ORANGE = "#FF8C00"       # Naranja (Wiphala)
BOLIVIA_PURPLE = "#8B008B"       # Púrpura (Wiphala)
BOLIVIA_BLUE = "#0066CC"         # Azul (Wiphala)

# Colores de fondo
BOLIVIA_BG_LIGHT = "#F8F9FA"     # Fondo claro
BOLIVIA_BG_DARK = "#2C3E50"      # Fondo oscuro
BOLIVIA_BG_WARM = "#FFF8DC"      # Fondo cálido (crema suave) - FONDO PRINCIPAL
BOLIVIA_BG_FRAME = "#FFFFFF"     # Fondo para frames (blanco más claro)
BOLIVIA_BG_CONTAINER = "#EBBB8E" # Fondo para contenedores (naranja medio)
BOLIVIA_BG_SECTION = "#F5F5DC"   # Fondo para secciones (crema más oscuro)
BOLIVIA_BG_CARD = "#FFFFFF"      # Fondo para tarjetas (blanco puro)

# Colores de texto
BOLIVIA_TEXT_DARK = "#2C3E50"    # Texto oscuro
BOLIVIA_TEXT_LIGHT = "#FFFFFF"   # Texto claro
BOLIVIA_TEXT_ACCENT = "#DA291C"  # Texto de acento

# Colores de elementos de interfaz
BOLIVIA_PRIMARY = BOLIVIA_RED        # Color primario
BOLIVIA_SECONDARY = BOLIVIA_GREEN    # Color secundario
BOLIVIA_ACCENT = BOLIVIA_YELLOW      # Color de acento
BOLIVIA_SUCCESS = BOLIVIA_GREEN      # Color de éxito
BOLIVIA_WARNING = BOLIVIA_ORANGE     # Color de advertencia
BOLIVIA_ERROR = BOLIVIA_RED          # Color de error

# Colores específicos para pestañas
BOLIVIA_TAB_NORMAL = "#FFE4B5"       # Pestaña normal (crema dorado claro)
BOLIVIA_TAB_HOVER = "#FFDAB9"        # Pestaña al pasar mouse (crema dorado medio)
BOLIVIA_TAB_SELECTED = BOLIVIA_RED   # Pestaña seleccionada (rojo boliviano)
BOLIVIA_TAB_TEXT_NORMAL = "#2C3E50"  # Texto pestaña normal (gris oscuro)
BOLIVIA_TAB_TEXT_SELECTED = "#FFFFFF" # Texto pestaña seleccionada (blanco)

# Gradientes bolivianos
BOLIVIA_GRADIENT_1 = [BOLIVIA_RED, BOLIVIA_YELLOW, BOLIVIA_GREEN]  # Bandera
BOLIVIA_GRADIENT_2 = [BOLIVIA_DARK_GREEN, BOLIVIA_GREEN, BOLIVIA_YELLOW]  # Montañas
BOLIVIA_GRADIENT_3 = [BOLIVIA_BLUE, BOLIVIA_PURPLE, BOLIVIA_ORANGE]  # Wiphala

# Configuración de tema
BOLIVIAN_THEME = {
    'primary_color': BOLIVIA_PRIMARY,
    'secondary_color': BOLIVIA_SECONDARY,
    'accent_color': BOLIVIA_ACCENT,
    'bg_color_light': BOLIVIA_BG_LIGHT,
    'bg_color_dark': BOLIVIA_BG_DARK,
    'bg_color_warm': BOLIVIA_BG_WARM,
    'bg_color_frame': BOLIVIA_BG_FRAME,
    'bg_color_container': BOLIVIA_BG_CONTAINER,
    'bg_color_section': BOLIVIA_BG_SECTION,
    'bg_color_card': BOLIVIA_BG_CARD,
    'text_color_dark': BOLIVIA_TEXT_DARK,
    'text_color_light': BOLIVIA_TEXT_LIGHT,
    'text_color_accent': BOLIVIA_TEXT_ACCENT,
    'success_color': BOLIVIA_SUCCESS,
    'warning_color': BOLIVIA_WARNING,
    'error_color': BOLIVIA_ERROR
} 