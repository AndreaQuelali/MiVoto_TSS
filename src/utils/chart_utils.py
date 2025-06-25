"""
Utilidades para generación de gráficos y visualizaciones
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
from config.settings import FIGURE_SIZE, DPI
import random
import hashlib

# Diccionario de colores por partido
PARTY_COLORS = {
    'MAS': '#1976d2',        
    'CC': '#ff9800',         
    'APB-Súmate': '#8e24aa', 
}

# Paleta para asignar colores a partidos no definidos
EXTRA_COLORS = [
    '#009688', '#c62828', '#43a047', '#fbc02d', '#5d4037',
    '#00bcd4', '#7e57c2', '#f06292', '#388e3c', '#ffa726',
    '#455a64', '#d4e157', '#6d4c41', '#0288d1', '#cddc39',
]

def get_party_colors(parties):
    colors = []
    used = set(PARTY_COLORS.keys())
    extra_idx = 0
    for p in parties:
        if p in PARTY_COLORS:
            colors.append(PARTY_COLORS[p])
        else:
            hash_idx = int(hashlib.md5(p.encode()).hexdigest(), 16) % len(EXTRA_COLORS)
            colors.append(EXTRA_COLORS[hash_idx])
    return colors

def crear_grafico_historicos(datos_historicos: Dict[str, Dict[str, float]], parent_frame):
    """
    Crea el gráfico de líneas para la evolución histórica de votos.
    
    Args:
        datos_historicos: Diccionario con datos históricos
        parent_frame: Frame padre donde mostrar el gráfico
        
    Returns:
        FigureCanvasTkAgg: Canvas del gráfico
    """
    if not datos_historicos:
        return None

    fig_hist, ax_hist = plt.subplots(figsize=FIGURE_SIZE)

    all_parties = sorted(list(set(p for data in datos_historicos.values() for p in data.keys())))
    years = sorted(list(datos_historicos.keys()))

    for party in all_parties:
        percentages = [datos_historicos.get(year, {}).get(party, 0) for year in years]
        if any(p > 0 for p in percentages):
            ax_hist.plot(years, percentages, 'o-', label=party)

    ax_hist.set_title("Evolución Histórica de Votación por Partido")
    ax_hist.set_ylabel("Porcentaje de Votos (%)")
    ax_hist.set_xlabel("Año Electoral")
    ax_hist.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
    ax_hist.grid(True, linestyle='--', alpha=0.7)
    fig_hist.tight_layout()

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    canvas_historicos = FigureCanvasTkAgg(fig_hist, master=parent_frame)
    canvas_historicos.draw()
    canvas_historicos.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    return canvas_historicos


def crear_grafico_encuestas(encuestas_2025: Dict[str, Dict[str, float]], parent_frame):
    """
    Crea el gráfico de barras para el promedio de las encuestas 2025.
    
    Args:
        encuestas_2025: Diccionario con datos de encuestas
        parent_frame: Frame padre donde mostrar el gráfico
        
    Returns:
        FigureCanvasTkAgg: Canvas del gráfico
    """
    if not encuestas_2025:
        return None

    fig_enc, ax_enc = plt.subplots(figsize=FIGURE_SIZE)

    # Calcular promedios de encuestas
    party_votes = defaultdict(list)
    for data in encuestas_2025.values():
        for party, votes in data.items():
            party_votes[party].append(votes)

    promedios = {p: np.mean(v) for p, v in party_votes.items()}
    sorted_promedios = dict(sorted(promedios.items(), key=lambda item: item[1], reverse=True))

    parties = list(sorted_promedios.keys())
    percentages = list(sorted_promedios.values())

    bars = ax_enc.bar(parties, percentages, color=get_party_colors(parties))

    ax_enc.set_title("Promedio de Encuestas 2025")
    ax_enc.set_ylabel("Porcentaje de Votos (%)")
    ax_enc.set_xlabel("Partido Político")
    ax_enc.grid(True, linestyle='--', alpha=0.7, axis='y')
    ax_enc.set_ylim(0, 100)

    # Mostrar valor sobre cada barra
    for bar in bars:
        height = bar.get_height()
        ax_enc.text(bar.get_x() + bar.get_width() / 2, height,
                    f'{height:.1f}%', ha='center', va='bottom')

    fig_enc.tight_layout()

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    canvas_encuestas = FigureCanvasTkAgg(fig_enc, master=parent_frame)
    canvas_encuestas.draw()
    canvas_encuestas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    return canvas_encuestas


def crear_grafico_votos(prediccion_votos: Dict[str, float], parent_frame):
    """
    Crea el gráfico de barras para la predicción de votos.
    
    Args:
        prediccion_votos: Diccionario con la predicción de votos
        parent_frame: Frame padre donde mostrar el gráfico
        
    Returns:
        FigureCanvasTkAgg: Canvas del gráfico
    """
    if not prediccion_votos:
        return None

    fig_votos, ax_votos = plt.subplots(figsize=FIGURE_SIZE)
    parties = list(prediccion_votos.keys())
    percentages = list(prediccion_votos.values())

    sorted_indices = np.argsort(percentages)[::-1]
    parties = np.array(parties)[sorted_indices]
    percentages = np.array(percentages)[sorted_indices]

    bars = ax_votos.bar(parties, percentages, color=get_party_colors(parties))

    ax_votos.set_title("Predicción de Votos para Elecciones 2025")
    ax_votos.set_ylabel("Porcentaje de Votos (%)")
    ax_votos.set_xlabel("Partido Político")
    ax_votos.grid(True, linestyle='--', alpha=0.7, axis='y')
    ax_votos.set_ylim(0, max(percentages) * 1.2 if percentages.size > 0 else 100)

    for bar in bars:
        height = bar.get_height()
        ax_votos.text(bar.get_x() + bar.get_width() / 2, height,
                      f'{height:.1f}%', ha='center', va='bottom')

    fig_votos.tight_layout()

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    canvas_votos = FigureCanvasTkAgg(fig_votos, master=parent_frame)
    canvas_votos.draw()
    canvas_votos.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    return canvas_votos


def crear_grafico_escanos(escanos_data: Dict[str, int], parent_frame, title_suffix: str):
    """
    Crea el gráfico de barras para la distribución de escaños.
    
    Args:
        escanos_data: Diccionario con la distribución de escaños
        parent_frame: Frame padre donde mostrar el gráfico
        title_suffix: Sufijo para el título del gráfico
        
    Returns:
        FigureCanvasTkAgg: Canvas del gráfico
    """
    if not escanos_data:
        return None

    fig_escanos, ax_escanos = plt.subplots(figsize=FIGURE_SIZE)
    parties = list(escanos_data.keys())
    seats = list(escanos_data.values())

    sorted_indices = np.argsort(seats)[::-1]
    parties = np.array(parties)[sorted_indices]
    seats = np.array(seats)[sorted_indices]

    bars = ax_escanos.bar(parties, seats, color=get_party_colors(parties))

    ax_escanos.set_title(f"Distribución de {title_suffix} por Partido")
    ax_escanos.set_ylabel(f"Número de {title_suffix}")
    ax_escanos.set_xlabel("Partido Político")
    ax_escanos.grid(True, linestyle='--', alpha=0.7, axis='y')
    ax_escanos.set_ylim(0, max(seats) * 1.2 if seats.size > 0 else 10)

    for bar in bars:
        height = bar.get_height()
        ax_escanos.text(bar.get_x() + bar.get_width() / 2, height,
                        f'{int(height)}', ha='center', va='bottom')

    fig_escanos.tight_layout()

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    canvas_escanos = FigureCanvasTkAgg(fig_escanos, master=parent_frame)
    canvas_escanos.draw()
    canvas_escanos.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    return canvas_escanos


def crear_grafico_pdf(prediccion_votos: Dict[str, float], senadores: Dict[str, int], 
                     diputados: Dict[str, int]) -> Tuple[str, str, str]:
    """
    Crea gráficos para exportar a PDF.
    
    Args:
        prediccion_votos: Diccionario con la predicción de votos
        senadores: Diccionario con la distribución de senadores
        diputados: Diccionario con la distribución de diputados
        
    Returns:
        Tuple[str, str, str]: Rutas de los archivos temporales de gráficos
    """
    # Gráfico de Votos
    fig_votos, ax_votos = plt.subplots(figsize=(8, 4))
    parties = list(prediccion_votos.keys())
    percentages = list(prediccion_votos.values())
    sorted_indices = np.argsort(percentages)[::-1]
    parties = np.array(parties)[sorted_indices]
    percentages = np.array(percentages)[sorted_indices]
    ax_votos.bar(parties, percentages, color=get_party_colors(parties))
    ax_votos.set_title("Predicción de Votos para Elecciones 2025")
    ax_votos.set_ylabel("Porcentaje de Votos (%)")
    ax_votos.set_xlabel("Partido Político")
    ax_votos.grid(True, linestyle='--', alpha=0.7, axis='y')
    ax_votos.set_ylim(0, max(percentages) * 1.2 if percentages.size > 0 else 100)
    fig_votos.tight_layout()
    
    img_path_votos = "temp_votos_prediccion.png"
    fig_votos.savefig(img_path_votos, dpi=DPI)
    plt.close(fig_votos)

    # Gráfico de Senadores
    fig_senadores, ax_senadores = plt.subplots(figsize=(8, 4))
    parties_sen = list(senadores.keys())
    seats_sen = list(senadores.values())
    sorted_indices_sen = np.argsort(seats_sen)[::-1]
    parties_sen = np.array(parties_sen)[sorted_indices_sen]
    seats_sen = np.array(seats_sen)[sorted_indices_sen]
    ax_senadores.bar(parties_sen, seats_sen, color=get_party_colors(parties_sen))
    ax_senadores.set_title("Distribución de Senadores por Partido")
    ax_senadores.set_ylabel("Número de Senadores")
    ax_senadores.set_xlabel("Partido Político")
    ax_senadores.grid(True, linestyle='--', alpha=0.7, axis='y')
    ax_senadores.set_ylim(0, max(seats_sen) * 1.2 if seats_sen.size > 0 else 10)
    fig_senadores.tight_layout()

    img_path_senadores = "temp_senadores_distribucion.png"
    fig_senadores.savefig(img_path_senadores, dpi=DPI)
    plt.close(fig_senadores)

    # Gráfico de Diputados
    fig_diputados, ax_diputados = plt.subplots(figsize=(8, 4))
    parties_dip = list(diputados.keys())
    seats_dip = list(diputados.values())
    sorted_indices_dip = np.argsort(seats_dip)[::-1]
    parties_dip = np.array(parties_dip)[sorted_indices_dip]
    seats_dip = np.array(seats_dip)[sorted_indices_dip]
    ax_diputados.bar(parties_dip, seats_dip, color=get_party_colors(parties_dip))
    ax_diputados.set_title("Distribución de Diputados por Partido")
    ax_diputados.set_ylabel("Número de Diputados")
    ax_diputados.set_xlabel("Partido Político")
    ax_diputados.grid(True, linestyle='--', alpha=0.7, axis='y')
    ax_diputados.set_ylim(0, max(seats_dip) * 1.2 if seats_dip.size > 0 else 10)
    fig_diputados.tight_layout()

    img_path_diputados = "temp_diputados_distribucion.png"
    fig_diputados.savefig(img_path_diputados, dpi=DPI)
    plt.close(fig_diputados)

    return img_path_votos, img_path_senadores, img_path_diputados 