"""
Módulo para manejar datos electorales históricos y configuración del sistema electoral.
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class ElectoralConfig:
    """Configuración del sistema electoral"""
    total_senadores: int = 36
    total_diputados: int = 130
    umbral_minimo: float = 0.03  # 3% mínimo para representación
    umbral_segunda_vuelta: float = 0.40  # 40% con 10% de diferencia
    variacion_maxima: float = 5.0  # Variación máxima para simulaciones


class ElectoralData:
    """Clase para manejar datos electorales históricos"""
    
    def __init__(self):
        self.datos_historicos = {
            '2014': {'MAS': 61.36, 'UD': 24.23, 'PDC': 9.04, 'Otros': 5.37},
            '2019': {'MAS': 47.08, 'CC': 36.51, 'FPV': 8.86, 'Otros': 7.55},
            '2020': {'MAS': 54.10, 'CC': 28.83, 'Creemos': 14.00, 'FPV': 1.55, 'PAN-BOL': 0.52}
        }
        self.config = ElectoralConfig()
        self.partidos_hist = {}
    
    def get_available_years(self) -> List[str]:
        """Obtiene los años disponibles en los datos históricos"""
        return list(self.datos_historicos.keys())
    
    def get_parties_by_year(self, year: str) -> Dict[str, float]:
        """Obtiene los partidos y sus porcentajes para un año específico"""
        return self.datos_historicos.get(year, {})
    
    def load_historical_data(self, year: str) -> Dict[str, float]:
        """Carga los datos históricos de un año específico"""
        self.partidos_hist = self.datos_historicos.get(year, {})
        return self.partidos_hist
    
    def get_all_parties(self) -> List[str]:
        """Obtiene todos los partidos únicos a través de todos los años"""
        parties = set()
        for year_data in self.datos_historicos.values():
            parties.update(year_data.keys())
        return list(parties)
    
    def get_historical_trends(self) -> Dict[str, List[Tuple[str, float]]]:
        """Obtiene las tendencias históricas por partido"""
        trends = {}
        all_parties = self.get_all_parties()
        
        for party in all_parties:
            trends[party] = []
            for year in sorted(self.datos_historicos.keys()):
                if party in self.datos_historicos[year]:
                    trends[party].append((year, self.datos_historicos[year][party]))
        
        return trends 