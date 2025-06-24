"""
Configuración y constantes de la aplicación Predictor Electoral Bolivia 2025
"""

# Configuración de la ventana principal
WINDOW_TITLE = "Predictor Electoral Bolivia 2025"
WINDOW_SIZE = "1400x950"

# Configuración electoral
TOTAL_SENADORES = 36
TOTAL_DIPUTADOS = 130
UMBRAL_MINIMO_DEFAULT = 0.03

# Variables del modelo predictivo por defecto
PESO_HISTORICO_DEFAULT = 0.4
PESO_ENCUESTAS_DEFAULT = 0.6
MARGEN_ERROR_PREDICCION_DEFAULT = 0.03
TENDENCIA_AJUSTE_DEFAULT = "Conservar"

# Configuración de estilos visuales - Temática Boliviana
from .bolivian_theme import (
    BOLIVIA_RED, BOLIVIA_GREEN, BOLIVIA_YELLOW, BOLIVIA_BG_WARM,
    BOLIVIA_TEXT_DARK, BOLIVIA_DARK_GREEN, BOLIVIA_GOLD
)

PRIMARY_COLOR = BOLIVIA_RED
SECONDARY_COLOR = BOLIVIA_DARK_GREEN
ACCENT_COLOR = BOLIVIA_YELLOW
BG_COLOR = BOLIVIA_BG_WARM
TEXT_COLOR = BOLIVIA_TEXT_DARK

# Datos históricos de elecciones en Bolivia
DATOS_HISTORICOS_DEFAULT = {
    '2005': {'MAS': 53.7, 'PODEMOS': 28.6, 'UN': 7.8, 'MNR': 6.5, 'Otros': 3.4},
    '2009': {'MAS': 64.2, 'PPB-CN': 26.5, 'UN': 5.7, 'Otros': 3.6},
    '2014': {'MAS': 61.4, 'UD': 24.2, 'PDC': 9.0, 'Otros': 5.4},
    '2019': {'MAS': 47.1, 'CC': 36.5, 'FPV': 8.9, 'Otros': 7.5},
    '2020': {'MAS': 55.1, 'CC': 28.8, 'Creemos': 14.0, 'FPV': 1.6, 'Otros': 0.5}
}

# Encuestas 2025 por defecto
ENCUESTAS_2025_DEFAULT = {
    'Encuesta1': {'MAS': 48.0, 'CC': 32.0, 'Creemos': 15.0, 'FPV': 3.0, 'Nuevo': 2.0},
    'Encuesta2': {'MAS': 45.0, 'CC': 35.0, 'Creemos': 12.0, 'FPV': 5.0, 'Nuevo': 3.0},
    'Encuesta3': {'MAS': 50.0, 'CC': 30.0, 'Creemos': 13.0, 'FPV': 4.0, 'Nuevo': 3.0}
}

# Configuración de archivos
EXCEL_FILE_TYPES = [("Archivos Excel", "*.xlsx")]
CSV_FILE_TYPES = [("Archivos CSV", "*.csv")]
EXCEL_CSV_FILE_TYPES = [("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")]
PDF_FILE_TYPES = [("Archivos PDF", "*.pdf")]

# Configuración de gráficos
FIGURE_SIZE = (10, 5)
DPI = 100 