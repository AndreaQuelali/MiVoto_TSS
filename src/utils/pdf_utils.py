"""
Utilidades para generación de informes PDF
"""
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

from utils.chart_utils import crear_grafico_pdf


def generar_informe_pdf(file_path: str, datos_completos: Dict[str, Any]) -> None:
    """
    Genera un informe PDF con los resultados de la predicción incluyendo información detallada de escaños.
    
    Args:
        file_path: Ruta donde guardar el archivo PDF
        datos_completos: Diccionario con todos los datos de la predicción incluyendo escaños detallados
        
    Raises:
        Exception: Si hay error al generar el PDF
    """
    try:
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Extraer datos
        prediccion_votos = datos_completos.get('prediccion_votos', {})
        senadores = datos_completos.get('senadores', {})
        diputados = datos_completos.get('diputados', {})
        diputados_plurinominales = datos_completos.get('diputados_plurinominales', {})
        diputados_uninominales = datos_completos.get('diputados_uninominales', {})
        diputados_uninominales_por_depto = datos_completos.get('diputados_uninominales_por_depto', {})
        detalle_escanos = datos_completos.get('detalle_escanos', {})

        # Título
        elements.append(Paragraph("Informe de Predicción Electoral Bolivia 2025", styles['h1']))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(f"Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 0.4 * inch))

        # Verificar si hay datos para procesar
        if not prediccion_votos and not senadores and not diputados:
            elements.append(Paragraph("No hay datos de predicción disponibles para generar el informe.", styles['Normal']))
            doc.build(elements)
            return

        # Sección de Predicción de Votos
        if prediccion_votos:
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

        # Gráficos - solo crear si hay datos
        img_path_votos = None
        img_path_senadores = None
        img_path_diputados = None
        
        if prediccion_votos or senadores or diputados:
            try:
                img_path_votos, img_path_senadores, img_path_diputados = crear_grafico_pdf(
                    prediccion_votos, senadores, diputados
                )
            except Exception as e:
                # Si falla la generación de gráficos, continuar sin ellos
                print(f"Advertencia: No se pudieron generar los gráficos: {e}")
        
        if prediccion_votos and img_path_votos:
            try:
                elements.append(Image(img_path_votos, width=6 * inch, height=3 * inch))
                elements.append(Spacer(1, 0.4 * inch))
            except Exception as e:
                print(f"Advertencia: No se pudo incluir el gráfico de votos: {e}")

        # Sección de Distribución de Senadores
        if senadores:
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
            
            if img_path_senadores:
                try:
                    elements.append(Image(img_path_senadores, width=6 * inch, height=3 * inch))
                    elements.append(Spacer(1, 0.4 * inch))
                except Exception as e:
                    print(f"Advertencia: No se pudo incluir el gráfico de senadores: {e}")

        # Sección de Distribución de Diputados Totales
        if diputados:
            elements.append(Paragraph("3. Distribución de Diputados Totales", styles['h2']))
            elements.append(Spacer(1, 0.1 * inch))
            data_diputados = [['Partido', 'Escaños Totales']]
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
            
            if img_path_diputados:
                try:
                    elements.append(Image(img_path_diputados, width=6 * inch, height=3 * inch))
                    elements.append(Spacer(1, 0.4 * inch))
                except Exception as e:
                    print(f"Advertencia: No se pudo incluir el gráfico de diputados: {e}")

        # Nueva página para detalles de escaños
        if diputados_plurinominales or diputados_uninominales or diputados_uninominales_por_depto or detalle_escanos:
            elements.append(PageBreak())
            elements.append(Paragraph("4. Detalle de Escaños por Tipo", styles['h2']))
            elements.append(Spacer(1, 0.2 * inch))

            # Diputados Plurinominales
            if diputados_plurinominales:
                elements.append(Paragraph("4.1. Diputados Plurinominales", styles['h3']))
                elements.append(Spacer(1, 0.1 * inch))
                data_plurinominales = [['Partido', 'Escaños Plurinominales']]
                sorted_plurinominales = sorted(diputados_plurinominales.items(), key=lambda item: item[1], reverse=True)
                for party, seats in sorted_plurinominales:
                    data_plurinominales.append([party, str(seats)])
                table_plurinominales = Table(data_plurinominales)
                table_plurinominales.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table_plurinominales)
                elements.append(Spacer(1, 0.2 * inch))

            # Diputados Uninominales
            if diputados_uninominales:
                elements.append(Paragraph("4.2. Diputados Uninominales", styles['h3']))
                elements.append(Spacer(1, 0.1 * inch))
                data_uninominales = [['Partido', 'Escaños Uninominales']]
                sorted_uninominales = sorted(diputados_uninominales.items(), key=lambda item: item[1], reverse=True)
                for party, seats in sorted_uninominales:
                    data_uninominales.append([party, str(seats)])
                table_uninominales = Table(data_uninominales)
                table_uninominales.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table_uninominales)
                elements.append(Spacer(1, 0.2 * inch))

            # Diputados Uninominales por Departamento
            if diputados_uninominales_por_depto:
                elements.append(Paragraph("4.3. Diputados Uninominales por Departamento", styles['h3']))
                elements.append(Spacer(1, 0.1 * inch))
                
                # Crear tabla para diputados uninominales por departamento
                depto_data = [['Partido', 'Departamento', 'Escaños']]
                for partido, deptos in diputados_uninominales_por_depto.items():
                    for depto, escaños in deptos.items():
                        if escaños > 0:  # Solo mostrar departamentos con escaños
                            depto_data.append([partido, depto, str(escaños)])
                
                if len(depto_data) > 1:  # Si hay datos además del encabezado
                    table_uninominales_depto = Table(depto_data)
                    table_uninominales_depto.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    elements.append(table_uninominales_depto)
                    elements.append(Spacer(1, 0.2 * inch))

            # Resumen Completo de Escaños
            if detalle_escanos:
                elements.append(Paragraph("5. Resumen Completo de Escaños por Partido", styles['h2']))
                elements.append(Spacer(1, 0.1 * inch))
                
                detalle_data = [['Partido', 'Senadores', 'Diputados Plurinominales', 'Diputados Uninominales', 'Total Diputados', 'Total Escaños']]
                for partido, info in detalle_escanos.items():
                    # Filtrar solo partidos reales
                    if not isinstance(info, dict):
                        continue
                    if not (('senadores' in info) or ('diputados_plurinominales' in info) or ('diputados_uninominales' in info)):
                        continue
                    senadores_count = info.get('senadores', 0)
                    diputados_plurinominales_count = info.get('diputados_plurinominales', 0)
                    diputados_uninominales_count = info.get('diputados_uninominales', 0)
                    total_diputados = diputados_plurinominales_count + diputados_uninominales_count
                    total_escanos = senadores_count + total_diputados
                    
                    detalle_data.append([
                        partido,
                        str(senadores_count),
                        str(diputados_plurinominales_count),
                        str(diputados_uninominales_count),
                        str(total_diputados),
                        str(total_escanos)
                    ])
                if len(detalle_data) == 1:
                    detalle_data.append(["No hay datos de partidos", "-", "-", "-", "-", "-"])
                table_detalle = Table(detalle_data)
                table_detalle.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table_detalle)
                elements.append(Spacer(1, 0.2 * inch))

        doc.build(elements)

    except Exception as e:
        raise Exception(f"No se pudo generar el informe PDF: {e}")
    finally:
        # Clean up temporary image files
        from utils.file_utils import limpiar_archivos_temporales
        temp_files = []
        if 'img_path_votos' in locals() and img_path_votos:
            temp_files.append(img_path_votos)
        if 'img_path_senadores' in locals() and img_path_senadores:
            temp_files.append(img_path_senadores)
        if 'img_path_diputados' in locals() and img_path_diputados:
            temp_files.append(img_path_diputados)
        if temp_files:
            limpiar_archivos_temporales(temp_files) 