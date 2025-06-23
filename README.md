# Simulador Electoral Bolivia 2025

Este es un simulador electoral que permite visualizar y analizar los resultados de las elecciones bolivianas, basándose en datos históricos de 2020 y permitiendo la simulación de nuevos escenarios.

## Características

- Visualización de resultados históricos de las elecciones 2020
- Simulación de nuevos escenarios electorales
- Cálculo automático de escaños (Senadores y Diputados) usando el método D'Hondt
- Gráficos interactivos de resultados
- Simulación de segunda vuelta cuando es necesario
- Interfaz gráfica intuitiva con Tkinter

## Requisitos

Para ejecutar este proyecto, necesitas tener instalado:

- Python 3.6 o superior
- Las siguientes bibliotecas de Python:
  - tkinter (incluido en la instalación estándar de Python)
  - matplotlib
  - pandas
  - openpyxl

## Instalación

1. Clona este repositorio o descarga los archivos del proyecto

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

#en mi caso funciona en windows con
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
python src/app.py
```
python run_app.py

## Uso

1. Al iniciar la aplicación, verás la pestaña "Resultados Históricos" que muestra los datos de las elecciones 2020
2. Puedes agregar nuevos partidos políticos usando el campo de texto y el botón "Agregar"
3. Haz clic en "Mostrar Resultados Históricos" para ver los gráficos y análisis
4. La aplicación mostrará:
   - Distribución general de votos
   - Distribución de senadores
   - Distribución de diputados
   - Resumen detallado de resultados

## Notas

- El simulador utiliza el método D'Hondt para la distribución de escaños
- Se aplica un umbral mínimo del 3% para la representación parlamentaria
- Los nuevos partidos agregados reciben un porcentaje aleatorio entre 0% y 10%
- Se simula una segunda vuelta cuando ningún partido obtiene más del 50% de los votos

## Estructura del Proyecto

```
.
├── README.md
├── requirements.txt
└── src/
    └── app.py
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.
