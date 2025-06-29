"""
Modelo principal para la predicción electoral
"""
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict

from utils.electoral_utils import (
    verificar_segunda_vuelta, calcular_escanos, simular_segunda_vuelta,
    obtener_detalle_escanos
)


class ModeloPredictivoElectoral:
    """
    Modelo predictivo para las elecciones en Bolivia 2025.
    """
    
    def __init__(self):
        self.datos_historicos = {}
        self.encuestas_2025 = {}
        self.prediccion_2025 = {}
        self.senadores_2025 = {}
        self.diputados_2025 = {}
        self.prediccion_segunda_vuelta = {}
        
        # Nuevas variables para escaños detallados
        self.diputados_plurinominales_2025 = {}
        self.diputados_uninominales_2025 = {}
        self.diputados_uninominales_por_depto_2025 = {}
        self.detalle_escanos_2025 = {}
        
        # Variables del modelo
        self.peso_historico = 0.4
        self.peso_encuestas = 0.6
        self.margen_error_prediccion = 0.03
        self.tendencia_ajuste = "Conservar"
        self.umbral_minimo = 0.03
        
        # Variables para segunda vuelta
        self.segunda_vuelta = False
        self.candidatos_segunda_vuelta = []
        
        # Configuración electoral
        self.total_senadores = 36
        self.total_diputados = 130
        
        self.prediccion_ejecutada = False
    
    def cargar_datos_historicos(self, datos: Dict[str, Dict[str, float]]) -> None:
        """Carga los datos históricos de elecciones."""
        self.datos_historicos = datos
    
    def cargar_encuestas(self, encuestas: Dict[str, Dict[str, float]]) -> None:
        """Carga los datos de encuestas 2025."""
        self.encuestas_2025 = encuestas
    
    def configurar_parametros(self, peso_historico: float, peso_encuestas: float,
                            margen_error: float, tendencia: str, umbral: float) -> None:
        """Configura los parámetros del modelo predictivo."""
        self.peso_historico = peso_historico
        self.peso_encuestas = peso_encuestas
        self.margen_error_prediccion = margen_error
        self.tendencia_ajuste = tendencia
        self.umbral_minimo = umbral
    
    def ejecutar_prediccion(self) -> None:
        """
        Ejecuta el modelo predictivo completo.
        """
        if not self.datos_historicos or not self.encuestas_2025:
            raise ValueError("Se requieren tanto datos históricos como encuestas para ejecutar la predicción.")
        
        # Obtener datos históricos más recientes
        ultimos_años_historicos_keys = sorted([int(float(y)) for y in self.datos_historicos.keys()], reverse=True)
        if not ultimos_años_historicos_keys:
            raise ValueError("No hay datos históricos disponibles.")
            
        datos_historicos_recientes = self.datos_historicos[str(ultimos_años_historicos_keys[0])]
        
        # Obtener todos los partidos únicos
        all_parties = set(datos_historicos_recientes.keys()).union(*[e.keys() for e in self.encuestas_2025.values()])
        
        # Calcular promedios de encuestas
        promedios_encuestas_2025 = {}
        for p in all_parties:
            valores = [e.get(p, 0) for e in self.encuestas_2025.values()]
            promedios_encuestas_2025[p] = np.mean(valores) if valores else 0
        
        # Ejecutar predicción
        self.prediccion_2025 = {}
        for p in all_parties:
            hist_val = datos_historicos_recientes.get(p, 0)
            enc_val = promedios_encuestas_2025.get(p, 0)
            
            prediccion_base = (hist_val * self.peso_historico) + (enc_val * self.peso_encuestas)
            
            # Aplicar ajuste de tendencia
            if self.tendencia_ajuste == "Acentuar":
                if enc_val > hist_val:
                    prediccion_base *= 1.05
                elif enc_val < hist_val:
                    prediccion_base *= 0.95
            elif self.tendencia_ajuste == "Suavizar":
                prediccion_base = (hist_val + enc_val) / 2
            
            # Aplicar margen de error
            variacion = np.random.uniform(-self.margen_error_prediccion, self.margen_error_prediccion)
            prediccion = max(0, prediccion_base * (1 + variacion))
            self.prediccion_2025[p] = prediccion
        
        # Normalizar predicción
        total_prediccion = sum(self.prediccion_2025.values())
        if total_prediccion > 0:
            self.prediccion_2025 = {p: (v / total_prediccion) * 100 for p, v in self.prediccion_2025.items()}
        else:
            raise ValueError("La predicción de votos resultó en 0 para todos los partidos.")
        
        # Verificar segunda vuelta
        self.segunda_vuelta, self.candidatos_segunda_vuelta = verificar_segunda_vuelta(self.prediccion_2025)
        
        # Calcular escaños con detalle
        self.detalle_escanos_2025 = obtener_detalle_escanos(self.prediccion_2025, self.umbral_minimo)
        
        # Extraer resultados específicos
        self.senadores_2025 = self.detalle_escanos_2025['senadores']
        self.diputados_plurinominales_2025 = self.detalle_escanos_2025['diputados_plurinominales']
        self.diputados_uninominales_2025 = self.detalle_escanos_2025['diputados_uninominales']
        self.diputados_uninominales_por_depto_2025 = self.detalle_escanos_2025['diputados_uninominales_por_depto']
        self.diputados_2025 = self.detalle_escanos_2025['total_diputados']
        
        self.prediccion_ejecutada = True
    
    def simular_segunda_vuelta(self) -> Dict[str, float]:
        """
        Simula los resultados de la segunda vuelta electoral.
        
        Returns:
            Dict[str, float]: Predicción de votos para la segunda vuelta
        """
        if not self.segunda_vuelta or len(self.candidatos_segunda_vuelta) < 2:
            return {}
        
        self.prediccion_segunda_vuelta = simular_segunda_vuelta(
            self.prediccion_2025, 
            self.candidatos_segunda_vuelta
        )
        
        return self.prediccion_segunda_vuelta
    
    def obtener_resultados(self) -> Dict[str, any]:
        """
        Obtiene todos los resultados de la predicción.
        
        Returns:
            Dict con todos los resultados
        """
        return {
            'prediccion_votos': self.prediccion_2025,
            'senadores': self.senadores_2025,
            'diputados': self.diputados_2025,
            'diputados_plurinominales': self.diputados_plurinominales_2025,
            'diputados_uninominales': self.diputados_uninominales_2025,
            'diputados_uninominales_por_depto': self.diputados_uninominales_por_depto_2025,
            'detalle_escanos': self.detalle_escanos_2025,
            'segunda_vuelta': self.segunda_vuelta,
            'candidatos_segunda_vuelta': self.candidatos_segunda_vuelta,
            'prediccion_segunda_vuelta': self.prediccion_segunda_vuelta,
            'prediccion_ejecutada': self.prediccion_ejecutada
        }
    
    def obtener_detalle_escanos(self) -> Dict[str, any]:
        """
        Obtiene el detalle completo de la distribución de escaños.
        
        Returns:
            Dict con el detalle completo de escaños
        """
        return self.detalle_escanos_2025
    
    def obtener_escanos_por_departamento(self) -> Dict[str, Dict[str, int]]:
        """
        Obtiene la distribución de escaños uninominales por departamento.
        
        Returns:
            Dict con escaños por departamento y partido
        """
        return self.diputados_uninominales_por_depto_2025
    
    def obtener_estado_segunda_vuelta(self) -> Tuple[bool, List[str]]:
        """
        Obtiene el estado de la segunda vuelta.
        
        Returns:
            Tuple[bool, List[str]]: (requiere_segunda_vuelta, candidatos)
        """
        return self.segunda_vuelta, self.candidatos_segunda_vuelta 