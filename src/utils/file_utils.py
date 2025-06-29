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


def exportar_a_excel(file_path: str, datos_completos: Dict[str, Any]) -> None:
    """
    Exporta los datos de la predicción a un archivo Excel con información detallada de escaños.
    
    Args:
        file_path: Ruta donde guardar el archivo Excel
        datos_completos: Diccionario con todos los datos de la predicción incluyendo escaños detallados
        
    Raises:
        Exception: Si hay error al exportar
    """
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            # Predicción de Votos
            prediccion_votos = datos_completos.get('prediccion_votos', {})
            if prediccion_votos:
                df_votos = pd.DataFrame(list(prediccion_votos.items()), 
                                       columns=['Partido', 'Porcentaje de Votos'])
                df_votos['Porcentaje de Votos'] = df_votos['Porcentaje de Votos'].apply(lambda x: f"{x:.2f}%")
                df_votos.to_excel(writer, sheet_name='Prediccion Votos', index=False)

            # Senadores
            senadores = datos_completos.get('senadores', {})
            if senadores:
                df_senadores = pd.DataFrame(list(senadores.items()), 
                                           columns=['Partido', 'Escaños'])
                df_senadores.to_excel(writer, sheet_name='Senadores', index=False)

            # Diputados Totales
            diputados = datos_completos.get('diputados', {})
            if diputados:
                df_diputados = pd.DataFrame(list(diputados.items()), 
                                           columns=['Partido', 'Escaños Totales'])
                df_diputados.to_excel(writer, sheet_name='Diputados Totales', index=False)

            # Diputados Plurinominales
            diputados_plurinominales = datos_completos.get('diputados_plurinominales', {})
            if diputados_plurinominales:
                df_plurinominales = pd.DataFrame(list(diputados_plurinominales.items()), 
                                                columns=['Partido', 'Escaños Plurinominales'])
                df_plurinominales.to_excel(writer, sheet_name='Diputados Plurinominales', index=False)

            # Diputados Uninominales
            diputados_uninominales = datos_completos.get('diputados_uninominales', {})
            if diputados_uninominales:
                df_uninominales = pd.DataFrame(list(diputados_uninominales.items()), 
                                              columns=['Partido', 'Escaños Uninominales'])
                df_uninominales.to_excel(writer, sheet_name='Diputados Uninominales', index=False)

            # Diputados Uninominales por Departamento
            diputados_uninominales_por_depto = datos_completos.get('diputados_uninominales_por_depto', {})
            if diputados_uninominales_por_depto:
                # Crear DataFrame para diputados uninominales por departamento
                depto_data = []
                for partido, deptos in diputados_uninominales_por_depto.items():
                    for depto, escaños in deptos.items():
                        depto_data.append([partido, depto, escaños])
                
                if depto_data:
                    df_uninominales_depto = pd.DataFrame(depto_data, 
                                                        columns=['Partido', 'Departamento', 'Escaños'])
                    df_uninominales_depto.to_excel(writer, sheet_name='Uninominales por Depto', index=False)

            # Detalle de Escaños
            detalle_escanos = datos_completos.get('detalle_escanos', {})
            if detalle_escanos:
                # Crear DataFrame para detalle de escaños
                detalle_data = []
                for partido, info in detalle_escanos.items():
                    # Filtrar solo partidos reales
                    if not isinstance(info, dict):
                        continue
                    if not (('senadores' in info) or ('diputados_plurinominales' in info) or ('diputados_uninominales' in info)):
                        continue
                    senadores = info.get('senadores', 0)
                    diputados_plurinominales = info.get('diputados_plurinominales', 0)
                    diputados_uninominales = info.get('diputados_uninominales', 0)
                    total_diputados = diputados_plurinominales + diputados_uninominales
                    total_escanos = senadores + total_diputados
                    
                    detalle_data.append([
                        partido, 
                        senadores, 
                        diputados_plurinominales, 
                        diputados_uninominales, 
                        total_diputados, 
                        total_escanos
                    ])
                if not detalle_data:
                    detalle_data.append(["No hay datos de partidos", "-", "-", "-", "-", "-"])
                detalle_columnas = [
                    'Partido',
                    'Senadores',
                    'Diputados Plurinominales',
                    'Diputados Uninominales',
                    'Total Diputados',
                    'Total Escaños'
                ]
                df_detalle = pd.DataFrame(detalle_data, columns=detalle_columnas)
                df_detalle.to_excel(writer, sheet_name='Detalle Completo Escaños', index=False)

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