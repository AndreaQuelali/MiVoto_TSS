# Distribución Departamental de Escaños

## Implementación según la Ley 026 de Bolivia

### 🗺️ **Distribución Territorial Completa**

El sistema "MiVoto_TSS" ahora incluye una implementación completa de la distribución de escaños por departamento, respetando tanto la representación territorial como la proporcionalidad nacional.

### 📊 **Configuración por Departamento**

#### **Diputados Uninominales (70 escaños)**

```python
CIRCUNSCRIPCIONES_UNINOMINALES = {
    'La Paz': 20,      # Mayor población - Occidente
    'Cochabamba': 14,  # Centro del país
    'Santa Cruz': 18,  # Mayor población - Oriente
    'Oruro': 4,        # Altiplano
    'Potosí': 5,       # Altiplano
    'Chuquisaca': 4,   # Valles
    'Tarija': 3,       # Valles
    'Beni': 1,         # Llanos
    'Pando': 1         # Llanos
}
```

#### **Senadores (36 escaños)**
- **4 senadores por departamento** (representación igualitaria)
- Distribución por partido según fuerza electoral nacional
- Garantiza representación territorial equilibrada

### 🎯 **Características de la Distribución**

#### **1. Diputados Uninominales**
- **Representación Territorial**: Cada departamento tiene un número específico de escaños
- **Distribución Proporcional**: Los escaños se distribuyen entre partidos según su fuerza electoral
- **Variaciones Regionales**: Considera patrones electorales históricos por región

#### **2. Senadores**
- **Representación Igualitaria**: Todos los departamentos tienen 4 senadores
- **Distribución Nacional**: Los senadores se asignan por lista nacional
- **Equilibrio Territorial**: Garantiza voz igual para todos los departamentos

#### **3. Diputados Plurinominales**
- **Lista Nacional**: 60 escaños asignados proporcionalmente
- **Representación Proporcional**: Método D'Hondt aplicado a nivel nacional
- **Sin Distribución Territorial**: No se asignan por departamento

### 🔧 **Algoritmos Implementados**

#### **Simulación de Escaños Uninominales por Departamento**

```python
def simular_escanos_uninominales(prediccion_votos, circunscripciones):
    """
    Simula la distribución de escaños uninominales por departamento.
    Considera:
    - Fuerza electoral nacional de cada partido
    - Variaciones regionales (patrones históricos)
    - Número de escaños disponibles por departamento
    """
```

**Características del algoritmo:**
- **Variaciones Regionales**: Simula patrones electorales conocidos
- **Distribución Proporcional**: Basada en fuerza electoral nacional
- **Límites por Departamento**: Respeta el número de escaños asignados

#### **Patrones Regionales Simulados**

```python
# Patrones regionales para escaños uninominales
if departamento in ['La Paz', 'Cochabamba'] and partido in ['MAS', 'ALIANZA UNIDAD']:
    variacion_regional = 1.2  # Más fuertes en el occidente
elif departamento in ['Santa Cruz', 'Tarija'] and partido in ['LIBRE', 'APB-SÚMATE']:
    variacion_regional = 1.3  # Más fuertes en el oriente
elif departamento in ['Oruro', 'Potosí'] and partido in ['MAS', 'ALIANZA POPULAR']:
    variacion_regional = 1.1  # Más fuertes en el altiplano
```

#### **Simulación de Senadores por Departamento**

```python
def simular_senadores_por_departamento(prediccion_votos):
    """
    Simula la distribución de senadores por departamento.
    Cada departamento tiene 4 senadores que pueden ser de diferentes partidos.
    """
```

### 📈 **Visualizaciones Implementadas**

#### **1. Vista "Detalle de Escaños"**

**Secciones incluidas:**
- **Diputados Plurinominales**: Distribución nacional (60 escaños)
- **Diputados Uninominales**: Distribución nacional total (70 escaños)
- **Diputados por Departamento**: Desglose territorial detallado
- **Senadores**: Distribución nacional (36 escaños)
- **Senadores por Departamento**: Desglose territorial
- **Mapa Territorial**: Resumen completo por departamento

#### **2. Tablas Detalladas**

**Diputados por Departamento:**
- Departamento
- Partido Político
- Número de Escaños

**Senadores por Departamento:**
- Departamento
- Partido Político
- Número de Senadores

**Resumen Territorial:**
- Departamento
- Diputados Uninominales
- Senadores
- Total Territorial

### 🎨 **Interfaz de Usuario**

#### **Nueva Pestaña: "Detalle de Escaños"**

**Características:**
- **Diseño Responsivo**: Adaptable a diferentes tamaños de pantalla
- **Navegación Intuitiva**: Secciones claramente diferenciadas
- **Información Explicativa**: Contexto sobre cada tipo de distribución
- **Tablas Interactivas**: Con scroll y ordenamiento

#### **Colores y Estilos**
- **Temática Boliviana**: Rojo, verde, amarillo
- **Diferenciación Visual**: Cada tipo de escaño tiene su color distintivo
- **Tipografía Clara**: Fácil lectura de datos

### 📋 **Información Mostrada por Departamento**

#### **Para Cada Departamento se Muestra:**

1. **Diputados Uninominales Asignados**
   - Número total de escaños del departamento
   - Distribución por partido político
   - Porcentaje de representación territorial

2. **Senadores Asignados**
   - 4 senadores por departamento
   - Distribución por partido político
   - Representación igualitaria

3. **Total de Representación Territorial**
   - Suma de diputados uninominales + senadores
   - Peso político del departamento
   - Comparación con otros departamentos

### 🔍 **Análisis Territorial**

#### **Departamentos con Mayor Representación:**
1. **La Paz**: 24 escaños (20 diputados + 4 senadores)
2. **Santa Cruz**: 22 escaños (18 diputados + 4 senadores)
3. **Cochabamba**: 18 escaños (14 diputados + 4 senadores)

#### **Departamentos con Menor Representación:**
1. **Beni**: 5 escaños (1 diputado + 4 senadores)
2. **Pando**: 5 escaños (1 diputado + 4 senadores)

### 🎓 **Valor Educativo**

#### **Para el Taller de Simulación de Sistemas:**

1. **Comprensión del Federalismo**: Representación territorial vs. proporcional
2. **Análisis de Datos**: Distribución geográfica de poder político
3. **Simulación Matemática**: Algoritmos de distribución electoral
4. **Análisis Político**: Patrones electorales regionales

#### **Aspectos Técnicos:**
- **Algoritmos de Distribución**: Métodos proporcionales y territoriales
- **Análisis Geográfico**: Distribución espacial de representación
- **Visualización de Datos**: Gráficos y tablas comparativas
- **Interfaz de Usuario**: Diseño de sistemas de información

### 🔮 **Futuras Mejoras**

1. **Datos Departamentales Reales**: Integrar encuestas específicas por departamento
2. **Mapas Interactivos**: Visualización geográfica de la distribución
3. **Análisis de Sensibilidad**: Mostrar variaciones con diferentes parámetros
4. **Historial Territorial**: Comparar distribuciones entre diferentes elecciones

### 📊 **Ejemplo de Resultados**

#### **Distribución Típica por Departamento:**

```
La Paz:
- Diputados Uninominales: 20
- Senadores: 4
- Total: 24 escaños

Santa Cruz:
- Diputados Uninominales: 18
- Senadores: 4
- Total: 22 escaños

Cochabamba:
- Diputados Uninominales: 14
- Senadores: 4
- Total: 18 escaños
```

---

**Nota**: Esta implementación proporciona una herramienta educativa valiosa para comprender la complejidad del sistema electoral boliviano y la importancia de la representación territorial en un país federal.