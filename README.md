# 🌍 El Pulso de la Tierra - Data Storytelling

## Narrativa con Datos sobre Actividad Sísmica Global (1965-2016)

### 📋 Descripción del Proyecto

Este proyecto es un **trabajo de storytelling con datos** que analiza 50 años de actividad sísmica global utilizando visualizaciones interactivas avanzadas. La narrativa guía al lector a través de un viaje visual por los patrones, tendencias y eventos significativos registrados en el dataset de terremotos del National Earthquake Information Center (NEIC).

---

## 🎯 Objetivos

- Desarrollar una narrativa clara basada en datos sísmicos
- Crear visualizaciones interactivas avanzadas (no convencionales)
- Identificar patrones geográficos, temporales y de magnitud
- Comunicar hallazgos de forma visual y persuasiva

---

## 📊 Dataset

### Información General
- **Fuente:** National Earthquake Information Center (NEIC)
- **Enlace:** Kaggle - Significant Earthquakes Database
- **Registros:** 23,412 eventos sísmicos
- **Período:** 1965 - 2016 (51 años)
- **Archivo:** `database.csv`

### Variables Principales

| Variable | Tipo | Descripción |
|----------|------|-------------|
| Date | Temporal | Fecha del evento |
| Time | Temporal | Hora del evento |
| Latitude | Numérica | Latitud geográfica |
| Longitude | Numérica | Longitud geográfica |
| Type | Categórica | Tipo de evento sísmico |
| Depth | Numérica | Profundidad en km |
| Magnitude | Numérica | Magnitud del terremoto |
| Magnitude Type | Categórica | Escala de medición (MW, ML, etc.) |

### Justificación del Dataset

Este dataset fue seleccionado porque:
1. **Relevancia global:** Los terremotos afectan a millones de personas
2. **Completitud:** Contiene variables cuantitativas y cualitativas
3. **Extensión temporal:** 51 años permiten análisis de tendencias
4. **Riqueza geográfica:** Cobertura mundial para análisis espacial
5. **Impacto social:** Información vital para prevención y preparación

---

## 🛠️ Herramientas y Tecnologías

### Lenguajes
- **Python 3.x** - Análisis y generación de visualizaciones
- **HTML5** - Estructura de la página web
- **CSS3** - Diseño y estilos responsivos
- **JavaScript** - Interactividad web

### Librerías de Visualización
- **Plotly** - Gráficos interactivos principales
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Operaciones numéricas

### Entorno de Desarrollo
- **VS Code** - Editor de código
- **Python Virtual Environment** - Gestión de dependencias
- **Browser** - Visualización de resultados

---

## 📈 Visualizaciones Incluidas

### 1. 🗺️ Mapa Geoespacial Interactivo 3D
- **Tipo:** Scatter Geo con proyección ortográfica
- **Características:** 
  - Animación por décadas
  - Filtros interactivos
  - Tooltips informativos
  - Rotación 3D del globo
- **Propósito:** Mostrar distribución global y concentración en zonas tectónicas

### 2. 🌊 Diagrama Sankey
- **Tipo:** Flujo Sankey
- **Características:**
  - Nodos de magnitud y profundidad
  - Enlaces proporcionales
  - Colores diferenciados
- **Propósito:** Revelar relación entre magnitud y profundidad

### 3. 📦 Gráfico 3D de Dispersión
- **Tipo:** Scatter 3D
- **Características:**
  - Ejes: Longitud, Latitud, Profundidad
  - Color por magnitud
  - Rotación interactiva
- **Propósito:** Visualizar ubicación tridimensional de eventos

### 4. 🌳 Treemap
- **Tipo:** Mapa de árbol jerárquico
- **Características:**
  - Jerarquía: Tipo → Categoría de Magnitud
  - Tamaño proporcional a frecuencia
  - Navegación por niveles
- **Propósito:** Mostrar distribución jerárquica de tipos de eventos

### 5. 🎯 Gráfico de Radar
- **Tipo:** Polar/Radar Chart
- **Características:**
  - 12 ejes (meses del año)
  - Múltiples series (categorías de magnitud)
  - Forma circular
- **Propósito:** Identificar patrones estacionales

### 6. 💧 Gráfico de Cascada (Waterfall)
- **Tipo:** Waterfall Chart
- **Características:**
  - Barras incrementales/decrementales
  - Total acumulado
  - Código de colores
- **Propósito:** Mostrar evolución temporal por décadas

### 7. 🔥 Heatmap Temporal
- **Tipo:** Mapa de calor interactivo
- **Características:**
  - Matriz año-mes
  - Escala de colores
  - Tooltips con valores
- **Propósito:** Identificar períodos de alta actividad

---

## 🚀 Instalación y Uso

### Prerrequisitos
```bash
Python 3.8 o superior
pip (gestor de paquetes de Python)
Navegador web moderno (Chrome, Firefox, Edge)
```

### Paso 1: Instalar Dependencias
```bash
pip install pandas plotly numpy
```

### Paso 2: Generar Visualizaciones
```bash
python analisis_terremotos.py
```

Este script:
- Carga y limpia el dataset
- Genera 7 archivos HTML con visualizaciones interactivas
- Muestra estadísticas del análisis en consola

### Paso 3: Abrir la Página Web
Abre el archivo `index.html` en tu navegador web.

---

## 📁 Estructura del Proyecto

```
Trabajo_Autonomo_2p/
│
├── database.csv                          # Dataset original
├── analisis_terremotos.py                # Script de análisis
├── index.html                            # Página web principal
├── README.md                             # Este archivo
│
├── mapa_terremotos_3d.html              # Visualización 1
├── sankey_magnitud_profundidad.html     # Visualización 2
├── terremotos_3d_scatter.html           # Visualización 3
├── treemap_tipos_magnitud.html          # Visualización 4
├── radar_distribucion_mensual.html      # Visualización 5
├── waterfall_evolucion_decadas.html     # Visualización 6
└── heatmap_temporal.html                # Visualización 7
```

---

## 🔍 Hallazgos Principales

### 1. **Concentración Geográfica**
El 90% de terremotos significativos ocurren en el Cinturón de Fuego del Pacífico.

### 2. **Distribución de Magnitudes**
- 85% tienen magnitudes entre 5.5 y 6.5
- Menos del 0.5% son magnitud 8.0+
- Siguen la Ley de Gutenberg-Richter

### 3. **Profundidad vs Impacto**
Los terremotos superficiales (<70 km) son más destructivos en superficie.

### 4. **Sin Estacionalidad Clara**
No existe evidencia de patrones estacionales significativos.

### 5. **Variación Decadal**
La actividad fluctúa sin tendencia clara de aumento o disminución.

---

## 💡 Conclusiones e Implicaciones

### Para la Ciencia
- Confirma teorías de tectónica de placas
- Valida modelos estadísticos de frecuencia sísmica
- Identifica zonas de alto riesgo con precisión

### Para la Sociedad
- **Planificación urbana:** Evitar construcción en zonas de alto riesgo
- **Códigos de construcción:** Edificios sismorresistentes en áreas críticas
- **Sistemas de alerta:** Implementación en regiones vulnerables
- **Educación pública:** Preparación ante desastres naturales

### Posibles Decisiones Basadas en Datos
1. Inversión en infraestructura sismorresistente en zonas críticas
2. Desarrollo de sistemas de monitoreo en tiempo real
3. Políticas de ordenamiento territorial basadas en riesgo sísmico
4. Programas de educación y simulacros en comunidades vulnerables
5. Investigación científica enfocada en predicción de réplicas

---

## 👥 Autoría

**Trabajo Autónomo - Visualización de Datos**
- Universidad Laica Eloy Alfaro de Manabí (ULEAM)
- 5to Semestre - 2do Parcial
- Año: 2026

---

## 📚 Referencias

1. National Earthquake Information Center (NEIC) - USGS
2. Gutenberg, B. & Richter, C.F. (1944). "Frequency of earthquakes in California"
3. Plotly Documentation - https://plotly.com/python/
4. Pandas Documentation - https://pandas.pydata.org/

---

## 📝 Licencia

Este proyecto es de carácter académico para la asignatura de Visualización de Datos.

---

## 🌟 Características Destacadas

✅ **7 visualizaciones interactivas diferentes**
✅ **Gráficos avanzados no convencionales**
✅ **Filtros, tooltips y zoom interactivo**
✅ **Diseño web responsive y moderno**
✅ **Narrativa guiada paso a paso**
✅ **Análisis de 23,412 eventos sísmicos**
✅ **51 años de datos históricos**

---

**🌍 "El pulso de la Tierra continúa latiendo. Nuestra responsabilidad es escucharlo y comprenderlo."**
