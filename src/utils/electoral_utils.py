"""
Utilidades para cálculos electorales
"""
from collections import defaultdict
from typing import Dict, List, Tuple, Any


def verificar_segunda_vuelta(votos: Dict[str, float]) -> Tuple[bool, List[str]]:
    """
    Verifica si se requiere segunda vuelta según la Ley 026 de Bolivia.
    
    Args:
        votos: Diccionario con los porcentajes de votos por partido
        
    Returns:
        Tuple[bool, List[str]]: (True si se requiere segunda vuelta, lista con los dos partidos que pasan a segunda vuelta)
    """
    votos_ordenados = sorted(votos.items(), key=lambda item: item[1], reverse=True)
    
    # Caso 1: Mayoría absoluta (50% + 1)
    if votos_ordenados[0][1] > 50.0:
        return False, []
        
    # Caso 2: 40% con 10% de diferencia
    if len(votos_ordenados) >= 2:
        if votos_ordenados[0][1] >= 40.0 and (votos_ordenados[0][1] - votos_ordenados[1][1]) >= 10.0:
            return False, []
    
    # Si no cumple ninguno de los casos anteriores, hay segunda vuelta
    return True, [votos_ordenados[0][0], votos_ordenados[1][0]]


def calcular_dhondt(votos_partidos: Dict[str, float], total_escanos: int) -> Dict[str, int]:
    """
    Implementa el método D'Hondt para la asignación de escaños.
    
    Args:
        votos_partidos: Diccionario con los votos normalizados por partido
        total_escanos: Número total de escaños a distribuir
        
    Returns:
        Dict[str, int]: Diccionario con los escaños asignados por partido
    """
    escanos = defaultdict(int)
    cocientes = {}

    for partido, votos in votos_partidos.items():
        cocientes[partido] = votos / 1

    for _ in range(total_escanos):
        if not cocientes:
            break

        ganador_escanio = max(cocientes, key=lambda k: cocientes[k])
        escanos[ganador_escanio] += 1

        escanos_actuales = escanos[ganador_escanio]
        votos_originales = votos_partidos[ganador_escanio]
        cocientes[ganador_escanio] = votos_originales / (escanos_actuales + 1)
    
    return dict(escanos)


def calcular_escanos(prediccion_votos: Dict[str, float], umbral_minimo: float, 
                    total_senadores: int, total_diputados: int) -> Tuple[Dict[str, int], Dict[str, int]]:
    """
    Calcula la distribución de escaños para senadores y diputados
    utilizando el método D'Hondt, considerando el umbral mínimo de votos.
    
    Args:
        prediccion_votos: Diccionario con la predicción de votos por partido
        umbral_minimo: Umbral mínimo de votos para obtener escaños
        total_senadores: Número total de senadores
        total_diputados: Número total de diputados
        
    Returns:
        Tuple[Dict[str, int], Dict[str, int]]: (escaños_senadores, escaños_diputados)
    """
    partidos_validos_votos = {p: v for p, v in prediccion_votos.items()
                              if v >= (umbral_minimo * 100)}

    if not partidos_validos_votos:
        return {}, {}

    total_votos_validos = sum(partidos_validos_votos.values())
    if total_votos_validos == 0:
        return {}, {}

    votos_normalizados = {p: v / total_votos_validos for p, v in partidos_validos_votos.items()}

    # Calcular escaños para Senadores (método D'Hondt)
    senadores = calcular_dhondt(votos_normalizados, total_senadores)

    # Calcular escaños para Diputados (método D'Hondt)
    diputados = calcular_dhondt(votos_normalizados, total_diputados)

    return senadores, diputados


def simular_segunda_vuelta(prediccion_2025: Dict[str, float], 
                          candidatos_segunda_vuelta: List[str]) -> Dict[str, float]:
    """
    Simula los resultados de la segunda vuelta electoral.
    
    Args:
        prediccion_2025: Predicción de votos de la primera vuelta
        candidatos_segunda_vuelta: Lista con los dos candidatos que pasan a segunda vuelta
        
    Returns:
        Dict[str, float]: Predicción de votos para la segunda vuelta
    """
    if len(candidatos_segunda_vuelta) < 2:
        return {}
        
    # Redistribuir votos considerando solo los dos partidos principales
    total_votos = sum(prediccion_2025.values())
    votos_primer_lugar = prediccion_2025[candidatos_segunda_vuelta[0]]
    votos_segundo_lugar = prediccion_2025[candidatos_segunda_vuelta[1]]
    
    # Calcular porcentaje de votos no asignados a estos dos partidos
    otros_votos = total_votos - votos_primer_lugar - votos_segundo_lugar
    
    # Simular redistribución (70% al primero, 30% al segundo como ejemplo)
    votos_primer_lugar += otros_votos * 0.7
    votos_segundo_lugar += otros_votos * 0.3
    
    # Actualizar predicción para mostrar solo los dos candidatos
    prediccion_segunda_vuelta = {
        candidatos_segunda_vuelta[0]: votos_primer_lugar,
        candidatos_segunda_vuelta[1]: votos_segundo_lugar
    }
    
    return prediccion_segunda_vuelta 