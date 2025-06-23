"""
Módulo para calcular la distribución de escaños usando el método D'Hondt.
"""

from typing import Dict, Union, List
from dataclasses import dataclass


@dataclass
class SeatAllocation:
    """Estructura para almacenar la asignación de escaños"""
    total: int
    mujeres: int = 0
    hombres: int = 0


class DHondtCalculator:
    """Clase para calcular la distribución de escaños usando el método D'Hondt"""
    
    @staticmethod
    def apply_dhondt(votos: Dict[str, float], total_seats: int, threshold: float = 0.0) -> Dict[str, Union[int, SeatAllocation]]:
        """
        Aplica el método D'Hondt para asignar escaños
        
        Args:
            votos: Diccionario con partidos y sus votos
            total_seats: Total de escaños a asignar
            threshold: Umbral mínimo para representación (0.0 a 1.0)
            
        Returns:
            Diccionario con partidos y sus escaños asignados
        """
        if not votos:
            return {}
        
        total_votos = sum(votos.values())
        if total_votos == 0:
            return {}
        
        # Filtrar partidos que superan el umbral
        partidos_validos = {p: v for p, v in votos.items() 
                          if (v / total_votos) >= threshold}
        
        if not partidos_validos:
            return {}
        
        asignaciones = {p: 0 for p in partidos_validos}
        cocientes = {p: v for p, v in partidos_validos.items()}  # Cocientes iniciales (V/1)
        
        for _ in range(total_seats):
            # Encontrar partido con mayor cociente
            partido_ganador = max(cocientes.items(), key=lambda x: x[1])[0]
            
            # Asignar escaño
            asignaciones[partido_ganador] += 1
            
            # Actualizar cociente para el próximo escaño
            cocientes[partido_ganador] = partidos_validos[partido_ganador] / (asignaciones[partido_ganador] + 1)
        
        return asignaciones
    
    @staticmethod
    def apply_gender_parity(seats: Dict[str, Union[int, SeatAllocation]]) -> Dict[str, SeatAllocation]:
        """
        Aplica paridad de género a la asignación de escaños
        
        Args:
            seats: Diccionario con partidos y sus escaños
            
        Returns:
            Diccionario con partidos y sus escaños con paridad de género
        """
        seats_with_parity = {}
        
        for partido, escanos in seats.items():
            if isinstance(escanos, int):
                total = escanos
            else:
                total = escanos.total
            
            if total > 0:
                mujeres = total // 2
                hombres = total - mujeres
                seats_with_parity[partido] = SeatAllocation(
                    total=total,
                    mujeres=mujeres,
                    hombres=hombres
                )
            else:
                seats_with_parity[partido] = SeatAllocation(total=0)
        
        return seats_with_parity
    
    @staticmethod
    def calculate_seats_for_chambers(votos: Dict[str, float], 
                                   total_senadores: int, 
                                   total_diputados: int, 
                                   threshold: float = 0.0,
                                   apply_parity: bool = False) -> Dict[str, Dict[str, Union[int, SeatAllocation]]]:
        """
        Calcula escaños para ambas cámaras
        
        Args:
            votos: Diccionario con partidos y sus votos
            total_senadores: Total de senadores
            total_diputados: Total de diputados
            threshold: Umbral mínimo para representación
            apply_parity: Si aplicar paridad de género
            
        Returns:
            Diccionario con escaños para senadores y diputados
        """
        # Calcular escaños básicos
        senadores = DHondtCalculator.apply_dhondt(votos, total_senadores, threshold)
        diputados = DHondtCalculator.apply_dhondt(votos, total_diputados, threshold)
        
        # Aplicar paridad si está activado
        if apply_parity:
            senadores = DHondtCalculator.apply_gender_parity(senadores)
            diputados = DHondtCalculator.apply_gender_parity(diputados)
        
        return {
            'senadores': senadores,
            'diputados': diputados
        }
    
    @staticmethod
    def get_majority_party(seats: Dict[str, Union[int, SeatAllocation]]) -> str:
        """
        Obtiene el partido con mayoría de escaños
        
        Args:
            seats: Diccionario con partidos y sus escaños
            
        Returns:
            Nombre del partido con mayoría
        """
        if not seats:
            return ""
        
        def get_total_seats(seat_data):
            if isinstance(seat_data, int):
                return seat_data
            return seat_data.total
        
        return max(seats.items(), key=lambda x: get_total_seats(x[1]))[0] 