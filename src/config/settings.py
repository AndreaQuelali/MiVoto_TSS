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
    '2005': {
        'MAS': 53.7,
        'PODEMOS': 28.6,
        'UN': 7.8,
        'MNR': 6.5,
        'Otros': 3.4
    },
    '2009': {
        'MAS': 64.2,
        'PPB-CN': 26.5,
        'UN': 5.7,
        'AS': 2.3,
        'Otros': 1.3
    },
    '2014': {
        'MAS': 61.0,
        'UD': 24.5,
        'PDC': 9.1,
        'MSM': 2.7,
        'PVB-IEP': 2.7
    },
    '2019': {
        'MAS': 47.1,
        'CC': 36.5,
        '21F': 8.8,
        'PDC': 6.2,
        'Otros': 1.4
    },
    '2020': {
        'MAS IPSP': 54.73,
        'CC': 29.16,
        'CREEMOS': 14.06,
        'FVP': 1.54,
        'PAN BOL': 0.50
    }
}

# Encuestas 2025 por defecto
ENCUESTAS_2025_DEFAULT = {
    'Encuesta1': {
        'ALIANZA UNIDAD': 26.1,
        'LIBRE': 25.2,
        'ALIANZA POPULAR': 19.4,
        'APB-SÚMATE': 10.8,
        'PDC': 5.9,
        'ALIANZA LA FUERZA DEL PUEBLO': 5.1,
        'MAS': 3.1,
        'MORENA': 2.3,
        'NGP': 1.4,
        'ADN': 0.7
    },
    'Encuesta2': {
        'APB-SÚMATE': 23.22,
        'LIBRE': 22.8,
        'NGP': 21.0,
        'ALIANZA UNIDAD': 19.8,
        'MAS': 13.18
    }
}

# Configuración de archivos
EXCEL_FILE_TYPES = [("Archivos Excel", "*.xlsx")]
CSV_FILE_TYPES = [("Archivos CSV", "*.csv")]
EXCEL_CSV_FILE_TYPES = [("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls")]
PDF_FILE_TYPES = [("Archivos PDF", "*.pdf")]

# Configuración de gráficos
FIGURE_SIZE = (10, 5)
DPI = 100 