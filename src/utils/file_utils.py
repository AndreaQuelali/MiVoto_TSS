"""
Utilidades para manejo de archivos
"""
import pandas as pd
import os
from typing import Dict, Any
from tkinter import messagebox


def cargar_encuestas_desde_archivo(file_path: str) -> Dict[str, Dict[str, float]]:
    """
    Carga datos de encuestas desde un archivo CSV o Excel.
    
    Args:
        file_path: Ruta del archivo a cargar
        
    Returns:
        Dict[str, Dict[str, float]]: Diccionario con los datos de encuestas
        
    Raises:
        ValueError: Si el formato del archivo es incorrecto
        Exception: Si hay error al cargar el archivo
    """
    try:
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        if 'Encuesta' not in df.columns:
            raise ValueError("El archivo debe contener una columna llamada 'Encuesta' para identificar las encuestas.")

        encuestas_cargadas = {}
        for idx, row in df.iterrows():
            encuesta_nombre = str(row['Encuesta'])
            partido_data = {}
            
            for col in df.columns:
                if col != 'Encuesta':
                    value = row[col]
                    if pd.notna(value):
                        partido_data[col] = float(value)
                    else:
                        partido_data[col] = 0.0
            
            if not partido_data:
                raise ValueError(f"La encuesta '{encuesta_nombre}' no contiene datos de partidos.")

            current_sum = sum(partido_data.values())
            if abs(current_sum - 100) > 0.1:
                messagebox.showwarning("Advertencia de Formato", 
                                     f"Los porcentajes de la encuesta '{encuesta_nombre}' no suman exactamente 100%. "
                                     f"Suma actual: {current_sum:.1f}%. Se utilizarán los valores tal cual.")
            
            encuestas_cargadas[encuesta_nombre] = partido_data

        return encuestas_cargadas
        
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise Exception(f"No se pudo cargar el archivo: {e}")


def cargar_historicos_desde_archivo(file_path: str) -> Dict[str, Dict[str, float]]:
    """
    Carga datos históricos desde un archivo CSV o Excel.
    
    Args:
        file_path: Ruta del archivo a cargar
        
    Returns:
        Dict[str, Dict[str, float]]: Diccionario con los datos históricos
        
    Raises:
        ValueError: Si el formato del archivo es incorrecto
        Exception: Si hay error al cargar el archivo
    """
    try:
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        if 'Año' not in df.columns:
            raise ValueError("El archivo debe contener una columna llamada 'Año' para identificar el año de la elección.")

        historicos_cargados = {}
        for idx, row in df.iterrows():
            año = str(int(float(row['Año'])))
            partido_data = {}
            
            for col in df.columns:
                if col != 'Año':
                    value = row[col]
                    if pd.notna(value):
                        partido_data[col] = float(value)
                    else:
                        partido_data[col] = 0.0
                        
            if not partido_data:
                raise ValueError(f"Los datos históricos del año '{año}' no contienen datos de partidos.")
                
            current_sum = sum(partido_data.values())
            if abs(current_sum - 100) > 0.1:
                messagebox.showwarning("Advertencia de Formato", 
                                     f"Los porcentajes del año '{año}' no suman exactamente 100%. "
                                     f"Suma actual: {current_sum:.1f}%. Se utilizarán los valores tal cual.")
                                     
            historicos_cargados[año] = partido_data

        return historicos_cargados
        
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise Exception(f"No se pudo cargar el archivo: {e}")


def exportar_a_excel(file_path: str, prediccion_votos: Dict[str, float], 
                    senadores: Dict[str, int], diputados: Dict[str, int]) -> None:
    """
    Exporta los datos de la predicción a un archivo Excel.
    
    Args:
        file_path: Ruta donde guardar el archivo Excel
        prediccion_votos: Diccionario con la predicción de votos
        senadores: Diccionario con la distribución de senadores
        diputados: Diccionario con la distribución de diputados
        
    Raises:
        Exception: Si hay error al exportar
    """
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            # Predicción de Votos
            df_votos = pd.DataFrame(list(prediccion_votos.items()), 
                                   columns=['Partido', 'Porcentaje de Votos'])
            df_votos['Porcentaje de Votos'] = df_votos['Porcentaje de Votos'].apply(lambda x: f"{x:.2f}%")
            df_votos.to_excel(writer, sheet_name='Prediccion Votos', index=False)

            # Senadores
            df_senadores = pd.DataFrame(list(senadores.items()), 
                                       columns=['Partido', 'Escaños'])
            df_senadores.to_excel(writer, sheet_name='Senadores', index=False)

            # Diputados
            df_diputados = pd.DataFrame(list(diputados.items()), 
                                       columns=['Partido', 'Escaños'])
            df_diputados.to_excel(writer, sheet_name='Diputados', index=False)

    except Exception as e:
        raise Exception(f"No se pudo exportar a Excel: {e}")


def limpiar_archivos_temporales(archivos: list) -> None:
    """
    Elimina archivos temporales del sistema.
    
    Args:
        archivos: Lista de rutas de archivos temporales a eliminar
    """
    for archivo in archivos:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
            except Exception:
                pass  # Ignorar errores al eliminar archivos temporales 