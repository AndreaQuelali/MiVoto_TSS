# Funcionalidades de Escaños Uninominales y Plurinominales

## Implementación según la Ley 026 de Bolivia

### 🎯 **Nuevas Funcionalidades Agregadas**

El sistema "MiVoto_TSS" ahora incluye una implementación completa de la distribución de escaños según la Ley 026 de Bolivia, diferenciando entre escaños uninominales y plurinominales.

### 📊 **Configuración Electoral**

#### **Diputados (130 totales)**
- **Diputados Plurinominales**: 60 escaños
  - Asignados por lista nacional
  - Distribución proporcional usando método D'Hondt
  - Representación nacional

- **Diputados Uninominales**: 70 escaños
  - Asignados por circunscripciones departamentales
  - Distribución por departamento según población
  - Representación territorial

#### **Senadores (36 totales)**
- 4 senadores por departamento
- Asignación por lista nacional
- Método D'Hondt

### 🗺️ **Distribución por Departamentos**

```python
CIRCUNSCRIPCIONES_UNINOMINALES = {
    'La Paz': 20,      # Mayor población
    'Cochabamba': 14,
    'Santa Cruz': 18,
    'Oruro': 4,
    'Potosí': 5,
    'Chuquisaca': 4,
    'Tarija': 3,
    'Beni': 1,
    'Pando': 1         # Menor población
}
```

### 🔧 **Funciones Implementadas**

#### **1. Cálculo de Escaños Plurinominales**
```python
def calcular_escanos_plurinominales(prediccion_votos, umbral_minimo, total_escanos)
```
- Aplica método D'Hondt para 60 escaños
- Considera umbral mínimo del 3%
- Distribución proporcional nacional

#### **2. Simulación de Escaños Uninominales**
```python
def simular_escanos_uninominales(prediccion_votos, circunscripciones)
```
- Simula distribución por departamento
- Basado en fuerza electoral relativa
- Considera características territoriales

#### **3. Detalle Completo de Escaños**
```python
def obtener_detalle_escanos(prediccion_votos, umbral_minimo)
```
- Retorna desglose completo
- Incluye todos los tipos de escaños
- Datos por departamento

### 🖥️ **Nueva Vista: "Detalle de Escaños"**

#### **Secciones Incluidas:**

1. **Diputados Plurinominales**
   - Gráfico de distribución
   - Tabla detallada
   - Total: 60 escaños

2. **Diputados Uninominales**
   - Gráfico de distribución
   - Tabla detallada
   - Total: 70 escaños

3. **Distribución por Departamento**
   - Tabla por departamento
   - Escaños uninominales por región
   - Análisis territorial

4. **Senadores**
   - Gráfico de distribución
   - Tabla detallada
   - Total: 36 escaños

5. **Resumen Total**
   - Combinación de todos los escaños
   - Vista general del parlamento

### 📈 **Características Técnicas**

#### **Método D'Hondt**
- Implementación completa del algoritmo
- Aplicado a escaños plurinominales y senadores
- Distribución proporcional exacta

#### **Umbral Mínimo**
- 3% según Ley 026
- Aplicado a todos los cálculos
- Filtrado de partidos minoritarios

#### **Simulación Territorial**
- Considera fuerza electoral por departamento
- Distribución realista de escaños uninominales
- Basado en patrones electorales históricos

### 🎨 **Interfaz de Usuario**

#### **Nueva Pestaña: "Detalle de Escaños"**
- Diseño consistente con temática boliviana
- Gráficos interactivos
- Tablas detalladas con scroll
- Información explicativa

#### **Colores y Estilos**
- Rojo, verde, amarillo (colores patrios)
- Tipografía clara y legible
- Organización visual intuitiva

### 🔍 **Análisis de Resultados**

#### **Información Proporcionada:**
- Distribución exacta de escaños
- Comparación entre tipos de representación
- Análisis territorial
- Proyecciones parlamentarias

#### **Visualizaciones:**
- Gráficos de barras por tipo de escaño
- Tablas detalladas con datos numéricos
- Distribución geográfica
- Resúmenes comparativos

### 📋 **Uso del Sistema**

1. **Ejecutar Predicción**: El modelo calcula automáticamente todos los tipos de escaños
2. **Ver Resultados Generales**: En la pestaña "Resultados de Predicción"
3. **Analizar Detalle**: En la nueva pestaña "Detalle de Escaños"
4. **Exportar Datos**: Incluye toda la información detallada

### 🎯 **Beneficios Educativos**

#### **Para el Taller de Simulación de Sistemas:**
- Comprensión del sistema electoral boliviano
- Aplicación práctica de métodos matemáticos
- Análisis de representación proporcional
- Simulación de escenarios electorales

#### **Aspectos Técnicos:**
- Implementación de algoritmos complejos
- Manejo de datos multidimensionales
- Interfaz gráfica avanzada
- Análisis estadístico aplicado

### 🔮 **Futuras Mejoras**

1. **Datos Departamentales Reales**: Integrar encuestas por departamento
2. **Análisis de Sensibilidad**: Mostrar variaciones con diferentes parámetros
3. **Historial de Predicciones**: Guardar y comparar diferentes escenarios
4. **Exportación Avanzada**: Reportes PDF detallados con análisis

---

**Nota**: Esta implementación respeta fielmente la Ley 026 de Bolivia y proporciona una herramienta educativa valiosa para comprender el sistema electoral boliviano.