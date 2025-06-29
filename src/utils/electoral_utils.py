"""
Utilidades para cálculos electorales
"""
from collections import defaultdict
from typing import Dict, List, Tuple, Any
from config.settings import (
    DIPUTADOS_UNINOMINALES, DIPUTADOS_PLURINOMINALES,
    CIRCUNSCRIPCIONES_UNINOMINALES, DEPARTAMENTOS_BOLIVIA,
    SENADORES_POR_DEPARTAMENTO
)


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


def calcular_escanos_plurinominales(prediccion_votos: Dict[str, float], umbral_minimo: float, 
                                   total_escanos: int) -> Dict[str, int]:
    """
    Calcula la distribución de escaños plurinominales usando el método D'Hondt.
    
    Args:
        prediccion_votos: Diccionario con la predicción de votos por partido
        umbral_minimo: Umbral mínimo de votos para obtener escaños
        total_escanos: Número total de escaños a distribuir
        
    Returns:
        Dict[str, int]: Diccionario con los escaños plurinominales asignados por partido
    """
    partidos_validos_votos = {p: v for p, v in prediccion_votos.items()
                              if v >= (umbral_minimo * 100)}

    if not partidos_validos_votos:
        return {}

    total_votos_validos = sum(partidos_validos_votos.values())
    if total_votos_validos == 0:
        return {}

    votos_normalizados = {p: v / total_votos_validos for p, v in partidos_validos_votos.items()}
    
    return calcular_dhondt(votos_normalizados, total_escanos)


def simular_escanos_uninominales(prediccion_votos: Dict[str, float], 
                                circunscripciones: Dict[str, int]) -> Dict[str, Dict[str, int]]:
    """
    Simula la distribución de escaños uninominales por departamento.
    Esta simulación considera la fuerza electoral de cada partido y las características territoriales.
    
    Args:
        prediccion_votos: Diccionario con la predicción de votos por partido
        circunscripciones: Diccionario con el número de escaños por departamento
        
    Returns:
        Dict[str, Dict[str, int]]: Diccionario con escaños uninominales por departamento y partido
    """
    escanos_uninominales = {}
    
    # Ordenar partidos por fuerza electoral
    partidos_ordenados = sorted(prediccion_votos.items(), key=lambda x: x[1], reverse=True)
    
    for departamento, num_escanos in circunscripciones.items():
        escanos_departamento = {}
        
        # Distribuir escaños basándose en la fuerza electoral nacional
        # pero con variaciones regionales simuladas
        for i, (partido, porcentaje_nacional) in enumerate(partidos_ordenados):
            if i >= num_escanos:
                break
                
            # Simular variación regional (partidos pueden tener diferente fuerza por departamento)
            # Por ejemplo, algunos partidos pueden ser más fuertes en ciertas regiones
            variacion_regional = 1.0
            
            # Simular patrones regionales conocidos
            if departamento in ['La Paz', 'Cochabamba'] and partido in ['MAS', 'ALIANZA UNIDAD']:
                variacion_regional = 1.2  # Más fuertes en el occidente
            elif departamento in ['Santa Cruz', 'Tarija'] and partido in ['LIBRE', 'APB-SÚMATE']:
                variacion_regional = 1.3  # Más fuertes en el oriente
            elif departamento in ['Oruro', 'Potosí'] and partido in ['MAS', 'ALIANZA POPULAR']:
                variacion_regional = 1.1  # Más fuertes en el altiplano
            
            # Calcular escaños asignados considerando la variación regional
            escanos_asignados = max(1, int((porcentaje_nacional / 100) * num_escanos * variacion_regional))
            
            # Asegurar que no se exceda el número de escaños disponibles
            escanos_disponibles = num_escanos - sum(escanos_departamento.values())
            if escanos_disponibles > 0:
                escanos_finales = min(escanos_asignados, escanos_disponibles)
                if escanos_finales > 0:
                    escanos_departamento[partido] = escanos_finales
        
        # Si quedan escaños sin asignar, distribuirlos entre los partidos más fuertes
        escanos_restantes = num_escanos - sum(escanos_departamento.values())
        if escanos_restantes > 0:
            # Dar prioridad a los partidos más fuertes
            for partido, _ in partidos_ordenados:
                if escanos_restantes <= 0:
                    break
                if partido not in escanos_departamento:
                    escanos_departamento[partido] = 1
                    escanos_restantes -= 1
                elif escanos_departamento[partido] < 2:  # Máximo 2 escaños por partido en departamentos pequeños
                    escanos_departamento[partido] += 1
                    escanos_restantes -= 1
        
        escanos_uninominales[departamento] = escanos_departamento
    
    return escanos_uninominales


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
    # Calcular escaños plurinominales (lista nacional)
    diputados_plurinominales = calcular_escanos_plurinominales(
        prediccion_votos, umbral_minimo, DIPUTADOS_PLURINOMINALES
    )
    
    # Simular escaños uninominales
    diputados_uninominales_por_depto = simular_escanos_uninominales(
        prediccion_votos, CIRCUNSCRIPCIONES_UNINOMINALES
    )
    
    # Sumar escaños uninominales totales por partido
    diputados_uninominales = defaultdict(int)
    for depto_escanos in diputados_uninominales_por_depto.values():
        for partido, escanos in depto_escanos.items():
            diputados_uninominales[partido] += escanos
    
    # Combinar escaños uninominales y plurinominales
    diputados_totales = defaultdict(int)
    for partido in set(diputados_plurinominales.keys()) | set(diputados_uninominales.keys()):
        diputados_totales[partido] = (
            diputados_plurinominales.get(partido, 0) + 
            diputados_uninominales.get(partido, 0)
        )
    
    # Calcular escaños para Senadores (método D'Hondt)
    senadores = calcular_escanos_plurinominales(
        prediccion_votos, umbral_minimo, total_senadores
    )

    return dict(senadores), dict(diputados_totales)


def obtener_detalle_escanos(prediccion_votos: Dict[str, float], umbral_minimo: float) -> Dict[str, Any]:
    """
    Obtiene el detalle completo de la distribución de escaños.
    
    Args:
        prediccion_votos: Diccionario con la predicción de votos por partido
        umbral_minimo: Umbral mínimo de votos para obtener escaños
        
    Returns:
        Dict con el detalle completo de escaños
    """
    # Calcular escaños plurinominales
    diputados_plurinominales = calcular_escanos_plurinominales(
        prediccion_votos, umbral_minimo, DIPUTADOS_PLURINOMINALES
    )
    
    # Simular escaños uninominales por departamento
    diputados_uninominales_por_depto = simular_escanos_uninominales(
        prediccion_votos, CIRCUNSCRIPCIONES_UNINOMINALES
    )
    
    # Sumar escaños uninominales totales
    diputados_uninominales = defaultdict(int)
    for depto_escanos in diputados_uninominales_por_depto.values():
        for partido, escanos in depto_escanos.items():
            diputados_uninominales[partido] += escanos
    
    # Calcular senadores (lista nacional)
    senadores = calcular_escanos_plurinominales(
        prediccion_votos, umbral_minimo, len(DEPARTAMENTOS_BOLIVIA) * SENADORES_POR_DEPARTAMENTO
    )
    
    # Simular senadores por departamento
    senadores_por_depto = simular_senadores_por_departamento(prediccion_votos)
    
    return {
        'diputados_plurinominales': dict(diputados_plurinominales),
        'diputados_uninominales': dict(diputados_uninominales),
        'diputados_uninominales_por_depto': diputados_uninominales_por_depto,
        'senadores': dict(senadores),
        'senadores_por_depto': senadores_por_depto,
        'total_diputados': {
            partido: diputados_plurinominales.get(partido, 0) + diputados_uninominales.get(partido, 0)
            for partido in set(diputados_plurinominales.keys()) | set(diputados_uninominales.keys())
        }
    }


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


def simular_senadores_por_departamento(prediccion_votos: Dict[str, float]) -> Dict[str, Dict[str, int]]:
    """
    Simula la distribución de senadores por departamento.
    Cada departamento tiene 4 senadores que pueden ser de diferentes partidos.
    
    Args:
        prediccion_votos: Diccionario con la predicción de votos por partido
        
    Returns:
        Dict[str, Dict[str, int]]: Diccionario con senadores por departamento y partido
    """
    senadores_por_depto = {}
    
    # Ordenar partidos por fuerza electoral
    partidos_ordenados = sorted(prediccion_votos.items(), key=lambda x: x[1], reverse=True)
    
    for departamento in DEPARTAMENTOS_BOLIVIA:
        senadores_departamento = {}
        
        # Distribuir 4 senadores por departamento
        for i, (partido, porcentaje) in enumerate(partidos_ordenados):
            if i >= 4:  # Máximo 4 partidos por departamento
                break
                
            # Simular variación regional para senadores
            variacion_regional = 1.0
            
            # Patrones regionales para senadores (similar a diputados pero más equilibrado)
            if departamento in ['La Paz', 'Cochabamba'] and partido in ['MAS', 'ALIANZA UNIDAD']:
                variacion_regional = 1.1
            elif departamento in ['Santa Cruz', 'Tarija'] and partido in ['LIBRE', 'APB-SÚMATE']:
                variacion_regional = 1.2
            elif departamento in ['Oruro', 'Potosí'] and partido in ['MAS', 'ALIANZA POPULAR']:
                variacion_regional = 1.05
            
            # Calcular senadores asignados
            senadores_asignados = max(1, int((porcentaje / 100) * 4 * variacion_regional))
            
            # Asegurar que no se exceda el número de senadores disponibles
            senadores_disponibles = 4 - sum(senadores_departamento.values())
            if senadores_disponibles > 0:
                senadores_finales = min(senadores_asignados, senadores_disponibles)
                if senadores_finales > 0:
                    senadores_departamento[partido] = senadores_finales
        
        # Si quedan senadores sin asignar, distribuirlos
        senadores_restantes = 4 - sum(senadores_departamento.values())
        if senadores_restantes > 0:
            for partido, _ in partidos_ordenados:
                if senadores_restantes <= 0:
                    break
                if partido not in senadores_departamento:
                    senadores_departamento[partido] = 1
                    senadores_restantes -= 1
        
        senadores_por_depto[departamento] = senadores_departamento
    
    return senadores_por_depto