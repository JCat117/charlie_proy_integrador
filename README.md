# charlie_proy_integrador
SB - Proyecto Integrador
# 📊 Análisis de Desplazamiento y Precipitación

Una aplicación web desarrollada en **Streamlit** para el análisis avanzado de datos de desplazamiento geotécnico y precipitación. Esta herramienta permite visualizar, analizar y extraer insights de datos de monitoreo de movimientos de tierra en relación con eventos pluviométricos.

## 🎯 Características Principales

### 📈 Visualización Avanzada
- **Gráficas duales**: Desplazamiento de puntos vs precipitación mensual
- **Gráficas de velocidad**: Análisis de tasas de desplazamiento temporal
- **Interfaz interactiva**: Selección dinámica de puntos de análisis
- **Exportación**: Descarga de gráficas en alta resolución (PNG)

### 🔍 Análisis Estadístico
- **Estadísticas descriptivas**: Media, máximo, mínimo, desviación estándar
- **Análisis de velocidad**: Cálculo de velocidades medias, máximas y mínimas de desplazamiento
- **Correlaciones**: Análisis de correlación entre desplazamiento y precipitación
- **Eventos críticos**: Identificación automática de eventos de alta precipitación y desplazamiento máximo

### 📊 Métricas Avanzadas
- Desplazamiento total por punto
- Velocidades de desplazamiento (mm/día)
- Fechas con mayor tasa de desplazamiento
- Análisis de percentiles de precipitación
- Detección de eventos críticos

## 🚀 Instalación

### Requisitos del Sistema
- Python 3.7+
- pip (gestor de paquetes de Python)

### Dependencias
```bash
pip install streamlit pandas matplotlib numpy openpyxl
```

### Instalación Rápida
```bash
git clone <repositorio>
cd <directorio-proyecto>
pip install -r requirements.txt
streamlit run Trabajo_Integrador.py
```

## 📋 Uso

### 1. Iniciar la Aplicación
```bash
streamlit run Trabajo_Integrador.py
```

### 2. Cargar Datos
- Utiliza el botón "Cargar archivo Excel" en la interfaz
- Selecciona un archivo `.xlsx` o `.xls` con el formato requerido

### 3. Configurar Análisis
- **Seleccionar puntos**: Elige los puntos de desplazamiento a analizar
- **Configurar precipitación**: Selecciona la columna de datos pluviométricos
- **Visualizar resultados**: Las gráficas se generan automáticamente

## 📊 Formato de Datos

### Estructura del Archivo Excel

| Columna | Descripción | Formato | Ejemplo |
|---------|-------------|---------|---------|
| `FECHA` | Fecha de medición | DD/MM/YYYY | 28/4/2015 |
| `53763`, `53834`, etc. | Puntos de desplazamiento | Numérico (mm) | 0.0395 |
| `rainfall (mm)` | Precipitación mensual | Numérico (mm) | 18.73 |

### Ejemplo de Datos
```csv
FECHA,53763,53834,53948,rainfall (mm)
28/4/2015,0.0,0.0,0.0,0.0
30/11/2015,0.0395,0.2015,-0.0033,18.73
24/12/2015,-0.0882,0.0558,-0.3386,28.95
```

## 🔧 Funcionalidades Detalladas

### Análisis de Desplazamiento
- **Cálculo automático de velocidades**: Diferencias temporales en mm/día
- **Estadísticas por punto**: Total, máximo, mínimo, media
- **Identificación de tendencias**: Análisis de patrones temporales

### Análisis de Precipitación
- **Eventos de alta precipitación**: Identificación automática (>90% percentil)
- **Correlación con desplazamiento**: Coeficientes de correlación de Pearson
- **Visualización integrada**: Gráficas de barras superpuestas

### Eventos Críticos
- **Desplazamientos máximos**: Identificación de valores extremos
- **Fechas críticas**: Registro de eventos significativos
- **Análisis de patrones**: Correlación entre lluvia y movimiento

## 📈 Interpretación de Resultados

### Correlación
- **Fuerte**: |r| > 0.7 - Relación significativa
- **Moderada**: 0.3 < |r| ≤ 0.7 - Relación moderada
- **Débil**: |r| ≤ 0.3 - Relación débil o inexistente

### Velocidades
- **Velocidades positivas**: Desplazamiento en dirección positiva
- **Velocidades negativas**: Desplazamiento en dirección negativa
- **Velocidades altas**: Posibles eventos de inestabilidad

## 🛠️ Estructura del Código

### Funciones Principales

#### `process_excel_data(df)`
- Limpia y procesa datos del archivo Excel
- Convierte fechas y valores numéricos
- Maneja errores de formato automáticamente

#### `calculate_displacement_statistics(df, selected_points)`
- Calcula estadísticas avanzadas de desplazamiento
- Computa velocidades y métricas temporales
- Identifica eventos extremos

#### `create_displacement_chart(df, selected_points, rainfall_col)`
- Genera gráficas duales de desplazamiento vs precipitación
- Implementa ejes Y duales para diferentes escalas
- Incluye etiquetas automáticas para eventos importantes

#### `find_critical_events(df, selected_points, rainfall_col)`
- Identifica automáticamente eventos críticos
- Analiza patrones de precipitación extrema
- Correlaciona eventos de desplazamiento y lluvia

## 🎨 Personalización

### Colores y Estilos
- Paleta de colores predefinida para hasta 8 puntos
- Configuración de transparencia y tamaños de marcadores
- Estilos de gráficas personalizables

### Parámetros Ajustables
```python
# Colores para puntos
colors = ['#2E8B57', '#FF6347', '#4682B4', '#9ACD32', '#FF1493', '#FFD700', '#8A2BE2', '#FF4500']

# Umbral para eventos de alta precipitación
high_rainfall_threshold = df[rainfall_col].quantile(0.9)

# Configuración de figura
fig, ax = plt.subplots(figsize=(15, 8))
```

## 📱 Interfaz de Usuario

### Sidebar
- **Configuración**: Selección de puntos y columnas
- **Información**: Estadísticas básicas del dataset
- **Parámetros**: Opciones de visualización

### Panel Principal
- **Vista previa**: Tabla con primeras 10 filas
- **Gráficas**: Visualizaciones interactivas
- **Análisis**: Tablas de estadísticas y eventos
- **Exportación**: Botones de descarga

## 🔍 Casos de Uso

### Monitoreo Geotécnico
- Análisis de estabilidad de taludes
- Monitoreo de deslizamientos
- Evaluación de riesgos geológicos

### Investigación Académica
- Estudios de correlación lluvia-movimiento
- Análisis de series temporales geotécnicas
- Modelado predictivo de movimientos

### Ingeniería Civil
- Monitoreo de obras de infraestructura
- Evaluación de cimentaciones
- Control de calidad en construcción

## 📊 Salidas y Reportes

### Gráficas Generadas
1. **Desplazamiento vs Precipitación**: Gráfica dual con ejes Y independientes
2. **Velocidad de Desplazamiento**: Evolución temporal de velocidades
3. **Análisis de Correlación**: Matrices de correlación visual

### Tablas de Datos
1. **Estadísticas de Velocidad**: Métricas por punto de medición
2. **Eventos Críticos**: Fechas y valores extremos
3. **Análisis de Correlación**: Coeficientes e interpretaciones

### Archivos de Exportación
- **PNG**: Gráficas en alta resolución (300 DPI)
- **Datos procesados**: Disponibles para análisis adicional

## 🐛 Solución de Problemas

### Errores Comunes

#### Error de Formato de Fecha
```
Error: time data '28/4/2015' does not match format
```
**Solución**: Verificar formato DD/MM/YYYY en columna FECHA

#### Error de Columnas Numéricas
```
Error: could not convert string to float
```
**Solución**: Reemplazar comas por puntos en valores decimales

#### Error de Archivo
```
Error: No such file or directory
```
**Solución**: Verificar que el archivo Excel esté en formato correcto

### Optimización
- **Datasets grandes**: Considerar muestreo de datos
- **Memoria**: Cerrar figuras después de mostrar
- **Rendimiento**: Filtrar datos antes de procesar

## 📋 Limitaciones

### Técnicas
- Máximo 8 puntos de desplazamiento simultáneos
- Formatos de fecha limitados a DD/MM/YYYY
- Requiere columnas específicas nombradas

### Funcionales
- No incluye análisis predictivo
- Correlaciones limitadas a Pearson
- Sin análisis espectral o frecuencial

## 🚀 Futuras Mejoras

### Funcionalidades Planificadas
- [ ] Análisis predictivo con Machine Learning
- [ ] Exportación a múltiples formatos (PDF, SVG)
- [ ] Análisis espectral de series temporales
- [ ] Integración con bases de datos
- [ ] API REST para análisis automatizado

### Mejoras de Interfaz
- [ ] Tema oscuro/claro
- [ ] Personalización de colores
- [ ] Zoom interactivo en gráficas
- [ ] Filtros temporales avanzados

## 🤝 Contribución

### Cómo Contribuir
1. Fork del repositorio
2. Crear branch para nueva funcionalidad
3. Implementar cambios con tests
4. Crear pull request con descripción detallada

### Estándares de Código
- PEP 8 para Python
- Docstrings en todas las funciones
- Comentarios explicativos
- Tests unitarios cuando aplique

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Créditos

Desarrollado para análisis geotécnico y monitoreo de movimientos de tierra en relación con eventos pluviométricos.

---

**Versión**: 1.0.0  
**Autor**: [Equipo Charlie]  
**Fecha**: Julio 2025  
**Contacto**: [jvcalderon7@utpl.edu.ec]
