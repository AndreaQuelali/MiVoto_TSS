"""
Módulo para simular elecciones con variaciones aleatorias.
"""

import random
from typing import Dict, List, Tuple, Optional
from ..models.electoral_data import ElectoralData


class ElectoralSimulator:
    """Clase para simular elecciones electorales"""
    
    def __init__(self, electoral_data: ElectoralData):
        self.electoral_data = electoral_data
    
    def simulate_election(self, variation_max: float) -> Dict[str, float]:
        """
        Simula una elección con variación aleatoria
        
        Args:
            variation_max: Variación máxima en porcentaje
            
        Returns:
            Diccionario con partidos y sus porcentajes simulados
        """
        if not self.electoral_data.partidos_hist:
            return {}
        
        resultados = {}
        
        for partido, porcentaje in self.electoral_data.partidos_hist.items():
            # Aplicar variación aleatoria (distribución normal)
            variacion = random.gauss(0, variation_max/3)  # 99.7% dentro de ±variacion_max
            nuevo_porcentaje = max(0.0, porcentaje + variacion)
            resultados[partido] = nuevo_porcentaje
        
        # Normalizar para que sumen 100%
        total = sum(resultados.values())
        if total > 0:
            resultados = {p: (v/total)*100 for p, v in resultados.items()}
        
        return resultados
    
    def simulate_multiple_scenarios(self, num_simulations: int, variation_max: float) -> List[Dict[str, float]]:
        """
        Ejecuta múltiples simulaciones
        
        Args:
            num_simulations: Número de simulaciones a ejecutar
            variation_max: Variación máxima en porcentaje
            
        Returns:
            Lista de resultados de simulaciones
        """
        resultados_simulaciones = []
        
        for _ in range(num_simulations):
            resultados = self.simulate_election(variation_max)
            resultados_simulaciones.append(resultados)
        
        return resultados_simulaciones
    
    def check_second_round_needed(self, resultados: Dict[str, float], rule: str) -> bool:
        """
        Verifica si se necesita segunda vuelta
        
        Args:
            resultados: Resultados de la elección
            rule: Regla para segunda vuelta ("40% con 10% diferencia" o "50% + 1 voto")
            
        Returns:
            True si se necesita segunda vuelta, False en caso contrario
        """
        total_votos = sum(resultados.values())
        if total_votos == 0:
            return False
        
        if rule == "50% + 1 voto":
            umbral = 50.0
            return not any(voto > umbral for voto in resultados.values())
        else:  # "40% con 10% diferencia"
            partidos_ordenados = sorted(resultados.items(), key=lambda x: -x[1])
            if len(partidos_ordenados) < 2:
                return False
            
            primer_partido = partidos_ordenados[0]
            segundo_partido = partidos_ordenados[1]
            
            return (primer_partido[1] < 40.0 or 
                   (primer_partido[1] - segundo_partido[1]) < 10.0)
    
    def prepare_second_round(self, resultados: Dict[str, float]) -> Dict[str, float]:
        """
        Prepara los datos para una segunda vuelta
        
        Args:
            resultados: Resultados originales
            
        Returns:
            Resultados con solo los dos partidos más votados
        """
        partidos_ordenados = sorted(resultados.items(), key=lambda x: -x[1])
        if len(partidos_ordenados) < 2:
            return resultados
        
        primer_partido = partidos_ordenados[0]
        segundo_partido = partidos_ordenados[1]
        
        return {
            primer_partido[0]: primer_partido[1],
            segundo_partido[0]: segundo_partido[1]
        }
    
    def get_top_two_parties(self, resultados: Dict[str, float]) -> Tuple[Tuple[str, float], Tuple[str, float]]:
        """
        Obtiene los dos partidos más votados
        
        Args:
            resultados: Resultados de la elección
            
        Returns:
            Tupla con los dos partidos más votados
        """
        partidos_ordenados = sorted(resultados.items(), key=lambda x: -x[1])
        if len(partidos_ordenados) < 2:
            return partidos_ordenados[0], partidos_ordenados[0]
        
        return partidos_ordenados[0], partidos_ordenados[1] 