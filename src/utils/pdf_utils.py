"""
Utilidades para generación de informes PDF
"""
from datetime import datetime
from typing import Dict, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

from utils.chart_utils import crear_grafico_pdf


def generar_informe_pdf(file_path: str, prediccion_votos: Dict[str, float], 
                       senadores: Dict[str, int], diputados: Dict[str, int]) -> None:
    """
    Genera un informe PDF con los resultados de la predicción.
    
    Args:
        file_path: Ruta donde guardar el archivo PDF
        prediccion_votos: Diccionario con la predicción de votos
        senadores: Diccionario con la distribución de senadores
        diputados: Diccionario con la distribución de diputados
        
    Raises:
        Exception: Si hay error al generar el PDF
    """
    try:
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Título
        elements.append(Paragraph("Informe de Predicción Electoral Bolivia 2025", styles['h1']))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(f"Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 0.4 * inch))

        # Sección de Predicción de Votos
        elements.append(Paragraph("1. Predicción de Votos por Partido", styles['h2']))
        elements.append(Spacer(1, 0.1 * inch))
        data_votos = [['Partido', 'Porcentaje de Votos (%)']]
        sorted_votos = sorted(prediccion_votos.items(), key=lambda item: item[1], reverse=True)
        for party, percentage in sorted_votos:
            data_votos.append([party, f"{percentage:.2f}%"])
        table_votos = Table(data_votos)
        table_votos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table_votos)
        elements.append(Spacer(1, 0.2 * inch))

        # Gráfico de Votos
        img_path_votos, img_path_senadores, img_path_diputados = crear_grafico_pdf(
            prediccion_votos, senadores, diputados
        )
        
        elements.append(Image(img_path_votos, width=6 * inch, height=3 * inch))
        elements.append(Spacer(1, 0.4 * inch))

        # Sección de Distribución de Senadores
        elements.append(Paragraph("2. Distribución de Senadores", styles['h2']))
        elements.append(Spacer(1, 0.1 * inch))
        data_senadores = [['Partido', 'Escaños']]
        sorted_senadores = sorted(senadores.items(), key=lambda item: item[1], reverse=True)
        for party, seats in sorted_senadores:
            data_senadores.append([party, str(seats)])
        table_senadores = Table(data_senadores)
        table_senadores.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table_senadores)
        elements.append(Spacer(1, 0.2 * inch))

        # Gráfico de Senadores
        elements.append(Image(img_path_senadores, width=6 * inch, height=3 * inch))
        elements.append(Spacer(1, 0.4 * inch))

        # Sección de Distribución de Diputados
        elements.append(Paragraph("3. Distribución de Diputados", styles['h2']))
        elements.append(Spacer(1, 0.1 * inch))
        data_diputados = [['Partido', 'Escaños']]
        sorted_diputados = sorted(diputados.items(), key=lambda item: item[1], reverse=True)
        for party, seats in sorted_diputados:
            data_diputados.append([party, str(seats)])
        table_diputados = Table(data_diputados)
        table_diputados.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table_diputados)
        elements.append(Spacer(1, 0.2 * inch))

        # Gráfico de Diputados
        elements.append(Image(img_path_diputados, width=6 * inch, height=3 * inch))
        elements.append(Spacer(1, 0.4 * inch))

        doc.build(elements)

    except Exception as e:
        raise Exception(f"No se pudo generar el informe PDF: {e}")
    finally:
        # Clean up temporary image files
        from utils.file_utils import limpiar_archivos_temporales
        limpiar_archivos_temporales([img_path_votos, img_path_senadores, img_path_diputados]) 