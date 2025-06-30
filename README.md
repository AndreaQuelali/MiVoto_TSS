# Simulador Electoral Bolivia 2025

Este es un simulador electoral que permite visualizar y analizar los resultados de las elecciones bolivianas, basándose en datos históricos de 2020 y permitiendo la simulación de nuevos escenarios.

## Características

- Visualización de resultados históricos de las elecciones 2020
- Simulación de nuevos escenarios electorales
- Cálculo automático de escaños (Senadores y Diputados) usando el método D'Hondt
- **NUEVO**: Especificación de escaños uninominales y plurinominales según la Ley 026
- **NUEVO**: Distribución territorial de escaños por departamento
- **NUEVO**: Vista detallada de distribución de escaños
- Gráficos interactivos de resultados
- Simulación de segunda vuelta cuando es necesario
- Interfaz gráfica intuitiva con CustomTkinter
- Temática boliviana con colores patrios

## 🆕 **Nuevas Funcionalidades - Escaños Uninominales y Plurinominales**

### Implementación según la Ley 026 de Bolivia

El sistema ahora incluye una implementación completa que diferencia entre:

#### **Diputados (130 totales)**
- **60 Diputados Plurinominales**: Lista nacional, método D'Hondt
- **70 Diputados Uninominales**: Circunscripciones departamentales

#### **Senadores (36 totales)**
- 4 senadores por departamento
- Asignación por lista nacional

#### **Nueva Vista: "Detalle de Escaños"**
- Distribución detallada por tipo de escaño
- Análisis territorial por departamento
- Gráficos y tablas comparativas
- Resumen parlamentario completo

## Requisitos

Para ejecutar este proyecto, necesitas tener instalado:

- Python 3.6 o superior
- Las siguientes bibliotecas principales de Python (todas las dependencias, incluidas las indirectas, están en el archivo requirements.txt):
  - customtkinter
  - matplotlib
  - pandas
  - openpyxl
  - numpy
  - pillow

> **Nota:** El archivo `requirements.txt` incluye todas las dependencias necesarias para el correcto funcionamiento del sistema, incluidas las requeridas por las librerías principales (por ejemplo: fonttools, kiwisolver, cycler, contourpy, pyparsing, python-dateutil, packaging, six, tzdata, et_xmlfile, entre otras). **Se recomienda instalar siempre usando:**
>
> ```bash
> pip install -r requirements.txt
> ```

## Instalación

1. Clona este repositorio o descarga los archivos del proyecto:

  https://github.com/AndreaQuelali/MiVoto_TSS.git

2. Crea un entorno virtual (recomendado):

```bash
# En Windows
python -m venv venv

# En Linux/Mac
python3 -m venv venv
```

3. Activa el entorno virtual:

```bash
# En Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# En Windows (Command Prompt)
.\venv\Scripts\activate.bat

# En algunos casos funciona en windows con
env\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

4. Instala las dependencias necesarias usando pip y el archivo requirements.txt:

```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar el simulador, simplemente ejecuta el archivo principal:

```bash
python src/main.py
```

## Uso

1. **Introducción**: Información general sobre las elecciones 2025
2. **Datos Históricos y Encuestas**: Cargar y visualizar datos electorales
3. **Configuración del Modelo**: Ajustar parámetros de predicción
4. **Resultados de Predicción**: Ver resultados generales
5. **🆕 Detalle de Escaños**: Análisis detallado de distribución de escaños
6. **Exportar Resultados**: Generar reportes y gráficos

### Nuevas Funcionalidades de Escaños

- **Vista Detallada**: Nueva pestaña "Detalle de Escaños" con análisis completo
- **Distribución Territorial**: Escaños uninominales por departamento
- **Análisis Comparativo**: Comparación entre tipos de representación
- **Visualizaciones Avanzadas**: Gráficos específicos por tipo de escaño

## Notas

- El simulador utiliza el método D'Hondt para la distribución de escaños
- Se aplica un umbral mínimo del 3% para la representación parlamentaria
- Los nuevos partidos agregados reciben un porcentaje aleatorio entre 0% y 10%
- Se simula una segunda vuelta cuando ningún partido obtiene más del 50% de los votos
- **NUEVO**: Implementación completa de la Ley 026 de Bolivia
- **NUEVO**: Distribución realista de escaños uninominales por departamento

## Estructura del Proyecto

```
.
├── README.md
├── requirements.txt
├── FUNCIONALIDADES_ESCANOS.md
└── src/
    ├── main.py
    ├── controllers/
    │   └── main_controller.py
    ├── models/
    │   └── electoral_model.py
    ├── views/
    │   ├── introduccion_view.py
    │   ├── datos_view.py
    │   ├── modelo_view.py
    │   ├── resultados_view.py
    │   ├── exportacion_view.py
    │   └── detalle_escanos_view.py
    ├── utils/
    │   ├── electoral_utils.py
    │   ├── chart_utils.py
    │   └── style_utils.py
    └── config/
        ├── settings.py
        └── bolivian_theme.py
```

## Documentación Adicional

Para más detalles sobre las nuevas funcionalidades de escaños, consulta:
- [FUNCIONALIDADES_ESCANOS.md](FUNCIONALIDADES_ESCANOS.md)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.

## Créditos

Desarrollado para el Taller de Simulación de Sistemas de la Universidad Mayor de San Simón, Bolivia.