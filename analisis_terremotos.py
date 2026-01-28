import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Cargar el dataset
df = pd.read_csv('database.csv')

# Limpieza de datos - manejo flexible de fechas
df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)
df = df.dropna(subset=['Date'])  # Eliminar filas con fechas inválidas

df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Decade'] = (df['Year'] // 10) * 10

# Filtrar datos con magnitud válida
df = df.dropna(subset=['Magnitude', 'Latitude', 'Longitude'])
df = df[df['Year'] >= 1965]  # Filtrar años válidos

print("Dataset cargado correctamente")
print(f"Total de registros: {len(df)}")
print(f"Rango de años: {df['Year'].min()} - {df['Year'].max()}")
print(f"Magnitud promedio: {df['Magnitude'].mean():.2f}")
print(f"Magnitud máxima: {df['Magnitude'].max():.2f}")

# ============================================
# GRÁFICO 1: MAPA INTERACTIVO CON LEAFLET (SIN API KEY)
# ============================================
print("\nGenerando mapa interactivo con Leaflet.js...")

# Filtrar terremotos significativos (magnitud > 5.5)
df_map = df[df['Magnitude'] > 5.5].copy()

# Preparar datos para el mapa
# Limitar a 5000 puntos para mejor rendimiento
df_map_sample = df_map.sample(min(5000, len(df_map)), random_state=42)

# Crear HTML con Leaflet
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa Global de Terremotos - Interactivo</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
    <style>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: #1a1a2e;
            overflow: hidden;
        }
        
        #map {
            height: 100vh;
            width: 100%;
        }
        
        .info-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            max-width: 350px;
            z-index: 1000;
        }
        
        .info-panel h2 {
            color: #c92a2a;
            margin-bottom: 10px;
            font-size: 1.3rem;
        }
        
        .info-panel p {
            color: #333;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }
        
        .legend {
            position: absolute;
            bottom: 30px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            z-index: 1000;
        }
        
        .legend h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
            border: 2px solid white;
        }
        
        .controls {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            z-index: 1000;
            min-width: 220px;
        }
        
        .controls h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        
        .control-group {
            margin-bottom: 10px;
        }
        
        .control-group label {
            display: block;
            color: #555;
            margin-bottom: 5px;
            font-size: 0.85rem;
        }
        
        .control-group input[type="range"] {
            width: 100%;
        }
        
        .control-group input[type="checkbox"] {
            margin-right: 5px;
        }
        
        button {
            background: #c92a2a;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
            margin-top: 5px;
            width: 100%;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #a51f1f;
        }
        
        .leaflet-popup-content-wrapper {
            border-radius: 8px;
            box-shadow: 0 3px 14px rgba(0,0,0,0.4);
        }
        
        .leaflet-popup-content {
            margin: 15px;
            font-family: Arial;
        }
        
        .popup-title {
            color: #c92a2a;
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .popup-info {
            margin: 5px 0;
            font-size: 0.9rem;
        }
        
        .marker-cluster-small {
            background-color: rgba(181, 226, 140, 0.6);
        }
        
        .marker-cluster-small div {
            background-color: rgba(110, 204, 57, 0.6);
        }
        
        .marker-cluster-medium {
            background-color: rgba(241, 211, 87, 0.6);
        }
        
        .marker-cluster-medium div {
            background-color: rgba(240, 194, 12, 0.6);
        }
        
        .marker-cluster-large {
            background-color: rgba(253, 156, 115, 0.6);
        }
        
        .marker-cluster-large div {
            background-color: rgba(241, 128, 23, 0.6);
        }
        
        @media (max-width: 768px) {
            .info-panel, .controls, .legend {
                position: relative;
                top: 0;
                left: 0;
                right: 0;
                margin: 10px;
                max-width: 100%;
            }
            
            #map {
                height: 70vh;
            }
        }
    </style>
</head>
<body>
    <div class="info-panel">
        <h2>🌍 Terremotos Globales</h2>
        <p><strong>Período:</strong> 1965 - 2016</p>
        <p><strong>Total de eventos:</strong> TOTAL_EVENTS</p>
        <p><strong>Magnitud promedio:</strong> AVG_MAG</p>
        <p><strong>Magnitud máxima:</strong> MAX_MAG</p>
        <p style="margin-top: 10px; font-size: 0.8rem; color: #666;">
            💡 Haz clic en los marcadores para ver detalles. 
            Usa zoom y arrastre para explorar.
        </p>
    </div>
    
    <div class="controls">
        <h3>🎛️ Controles</h3>
        <div class="control-group">
            <label>
                <input type="checkbox" id="toggleHeatmap" checked>
                Mostrar Mapa de Calor
            </label>
        </div>
        <div class="control-group">
            <label>
                <input type="checkbox" id="toggleMarkers" checked>
                Mostrar Marcadores
            </label>
        </div>
        <div class="control-group">
            <label>Magnitud Mínima: <span id="magValue">6.0</span></label>
            <input type="range" id="magSlider" min="5.5" max="9.0" step="0.1" value="6.0">
        </div>
        <button onclick="resetView()">🔄 Resetear Vista</button>
        <button onclick="toggleLayer()" style="margin-top: 5px;">🗺️ Cambiar Estilo</button>
    </div>
    
    <div class="legend">
        <h3>📊 Magnitud</h3>
        <div class="legend-item">
            <div class="legend-color" style="background: #fee5d9;"></div>
            <span style="font-size: 0.85rem;">5.5 - 6.0</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #fcae91;"></div>
            <span style="font-size: 0.85rem;">6.0 - 6.5</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #fb6a4a;"></div>
            <span style="font-size: 0.85rem;">6.5 - 7.0</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #de2d26;"></div>
            <span style="font-size: 0.85rem;">7.0 - 8.0</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #a50f15;"></div>
            <span style="font-size: 0.85rem;">≥ 8.0</span>
        </div>
    </div>
    
    <div id="map"></div>
    
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
    <script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
    
    <script>
        const earthquakeData = EARTHQUAKE_DATA;
        
        // Inicializar mapa
        const map = L.map('map', {
            center: [20, 0],
            zoom: 2,
            minZoom: 2,
            maxZoom: 18,
            worldCopyJump: true
        });
        
        // Capa base - OpenStreetMap
        const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        
        // Capa alternativa - Dark mode
        const darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '© OpenStreetMap contributors © CARTO',
            maxZoom: 19
        });
        
        let currentLayer = 'street';
        
        function toggleLayer() {
            if (currentLayer === 'street') {
                map.removeLayer(streetLayer);
                map.addLayer(darkLayer);
                currentLayer = 'dark';
            } else {
                map.removeLayer(darkLayer);
                map.addLayer(streetLayer);
                currentLayer = 'street';
            }
        }
        
        // Crear mapa de calor
        const heatData = earthquakeData.map(eq => [eq.lat, eq.lng, eq.mag * 0.5]);
        const heatLayer = L.heatLayer(heatData, {
            radius: 15,
            blur: 20,
            maxZoom: 10,
            max: 5.0,
            gradient: {
                0.0: 'blue',
                0.2: 'cyan',
                0.4: 'lime',
                0.6: 'yellow',
                0.8: 'orange',
                1.0: 'red'
            }
        }).addTo(map);
        
        // Función para obtener color por magnitud
        function getColorByMagnitude(mag) {
            if (mag < 6.0) return '#fee5d9';
            if (mag < 6.5) return '#fcae91';
            if (mag < 7.0) return '#fb6a4a';
            if (mag < 8.0) return '#de2d26';
            return '#a50f15';
        }
        
        // Función para obtener radio por magnitud
        function getRadiusByMagnitude(mag) {
            return Math.max(3, Math.min(15, mag * 1.5));
        }
        
        // Crear grupo de clusters para marcadores
        const markers = L.markerClusterGroup({
            maxClusterRadius: 50,
            spiderfyOnMaxZoom: true,
            showCoverageOnHover: false,
            zoomToBoundsOnClick: true
        });
        
        // Agregar marcadores
        earthquakeData.forEach(eq => {
            if (eq.mag >= 6.0) {  // Solo mostrar terremotos significativos
                const circle = L.circleMarker([eq.lat, eq.lng], {
                    radius: getRadiusByMagnitude(eq.mag),
                    fillColor: getColorByMagnitude(eq.mag),
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                });
                
                const popupContent = `
                    <div class="popup-title">Terremoto - Magnitud ${eq.mag}</div>
                    <div class="popup-info"><strong>📅 Fecha:</strong> ${eq.date}</div>
                    <div class="popup-info"><strong>⬇️ Profundidad:</strong> ${eq.depth} km</div>
                    <div class="popup-info"><strong>📍 Lat/Lng:</strong> ${eq.lat.toFixed(2)}°, ${eq.lng.toFixed(2)}°</div>
                    <div class="popup-info"><strong>🔍 Tipo:</strong> ${eq.type}</div>
                `;
                
                circle.bindPopup(popupContent);
                circle.magnitude = eq.mag;
                markers.addLayer(circle);
            }
        });
        
        map.addLayer(markers);
        
        // Controles
        document.getElementById('toggleHeatmap').addEventListener('change', function() {
            if (this.checked) {
                map.addLayer(heatLayer);
            } else {
                map.removeLayer(heatLayer);
            }
        });
        
        document.getElementById('toggleMarkers').addEventListener('change', function() {
            if (this.checked) {
                map.addLayer(markers);
            } else {
                map.removeLayer(markers);
            }
        });
        
        document.getElementById('magSlider').addEventListener('input', function() {
            const minMag = parseFloat(this.value);
            document.getElementById('magValue').textContent = minMag.toFixed(1);
            
            markers.clearLayers();
            earthquakeData.forEach(eq => {
                if (eq.mag >= minMag) {
                    const circle = L.circleMarker([eq.lat, eq.lng], {
                        radius: getRadiusByMagnitude(eq.mag),
                        fillColor: getColorByMagnitude(eq.mag),
                        color: '#fff',
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.8
                    });
                    
                    const popupContent = `
                        <div class="popup-title">Terremoto - Magnitud ${eq.mag}</div>
                        <div class="popup-info"><strong>📅 Fecha:</strong> ${eq.date}</div>
                        <div class="popup-info"><strong>⬇️ Profundidad:</strong> ${eq.depth} km</div>
                        <div class="popup-info"><strong>📍 Lat/Lng:</strong> ${eq.lat.toFixed(2)}°, ${eq.lng.toFixed(2)}°</div>
                        <div class="popup-info"><strong>🔍 Tipo:</strong> ${eq.type}</div>
                    `;
                    
                    circle.bindPopup(popupContent);
                    markers.addLayer(circle);
                }
            });
        });
        
        function resetView() {
            map.setView([20, 0], 2);
            document.getElementById('magSlider').value = 6.0;
            document.getElementById('magValue').textContent = '6.0';
            
            // Resetear marcadores
            markers.clearLayers();
            earthquakeData.forEach(eq => {
                if (eq.mag >= 6.0) {
                    const circle = L.circleMarker([eq.lat, eq.lng], {
                        radius: getRadiusByMagnitude(eq.mag),
                        fillColor: getColorByMagnitude(eq.mag),
                        color: '#fff',
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.8
                    });
                    
                    const popupContent = `
                        <div class="popup-title">Terremoto - Magnitud ${eq.mag}</div>
                        <div class="popup-info"><strong>📅 Fecha:</strong> ${eq.date}</div>
                        <div class="popup-info"><strong>⬇️ Profundidad:</strong> ${eq.depth} km</div>
                        <div class="popup-info"><strong>📍 Lat/Lng:</strong> ${eq.lat.toFixed(2)}°, ${eq.lng.toFixed(2)}°</div>
                        <div class="popup-info"><strong>🔍 Tipo:</strong> ${eq.type}</div>
                    `;
                    
                    circle.bindPopup(popupContent);
                    markers.addLayer(circle);
                }
            });
        }
    </script>
</body>
</html>
"""

# Preparar datos en formato JSON
earthquake_data = []
for _, row in df_map_sample.iterrows():
    earthquake_data.append({
        'lat': float(row['Latitude']),
        'lng': float(row['Longitude']),
        'mag': float(row['Magnitude']),
        'depth': float(row['Depth']) if not pd.isna(row['Depth']) else 0,
        'date': row['Date'].strftime('%Y-%m-%d'),
        'type': str(row['Type'])
    })

import json
earthquake_json = json.dumps(earthquake_data)

# Reemplazar placeholders
html_final = html_template.replace('EARTHQUAKE_DATA', earthquake_json)
html_final = html_final.replace('TOTAL_EVENTS', f"{len(df_map):,}")
html_final = html_final.replace('AVG_MAG', f"{df_map['Magnitude'].mean():.2f}")
html_final = html_final.replace('MAX_MAG', f"{df_map['Magnitude'].max():.1f}")

# Guardar archivo
with open('mapa_terremotos_3d.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("✓ Mapa interactivo con Leaflet.js guardado: mapa_terremotos_3d.html")

# ============================================
# GRÁFICO 2: GRÁFICO SANKEY - FLUJO DE MAGNITUDES
# ============================================
print("\nGenerando diagrama Sankey...")

# Crear categorías de magnitud
def categorizar_magnitud(mag):
    if mag < 5.0:
        return 'Leve (<5.0)'
    elif mag < 6.0:
        return 'Moderado (5.0-5.9)'
    elif mag < 7.0:
        return 'Fuerte (6.0-6.9)'
    elif mag < 8.0:
        return 'Mayor (7.0-7.9)'
    else:
        return 'Gran Terremoto (≥8.0)'

def categorizar_profundidad(depth):
    if pd.isna(depth):
        return 'Desconocida'
    elif depth < 70:
        return 'Superficial (<70km)'
    elif depth < 300:
        return 'Intermedio (70-300km)'
    else:
        return 'Profundo (>300km)'

df['Categoria_Magnitud'] = df['Magnitude'].apply(categorizar_magnitud)
df['Categoria_Profundidad'] = df['Depth'].apply(categorizar_profundidad)

# Preparar datos para Sankey
sankey_data = df.groupby(['Categoria_Magnitud', 'Categoria_Profundidad']).size().reset_index(name='count')

# Crear nodos
mag_categories = ['Leve (<5.0)', 'Moderado (5.0-5.9)', 'Fuerte (6.0-6.9)', 'Mayor (7.0-7.9)', 'Gran Terremoto (≥8.0)']
depth_categories = ['Superficial (<70km)', 'Intermedio (70-300km)', 'Profundo (>300km)', 'Desconocida']

all_nodes = mag_categories + depth_categories
node_dict = {node: idx for idx, node in enumerate(all_nodes)}

# Crear enlaces
source = []
target = []
value = []

for _, row in sankey_data.iterrows():
    if row['count'] > 10:  # Filtrar flujos muy pequeños
        source.append(node_dict[row['Categoria_Magnitud']])
        target.append(node_dict[row['Categoria_Profundidad']])
        value.append(row['count'])

# Colores para los nodos
node_colors = ['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15',  # Magnitudes
               '#08519c', '#3182bd', '#6baed6', '#bdd7e7']  # Profundidades

fig_sankey = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=all_nodes,
        color=node_colors
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color='rgba(255, 165, 0, 0.3)'
    )
)])

fig_sankey.update_layout(
    title_text='Relación entre Magnitud y Profundidad de Terremotos<br>Diagrama de Flujo Sankey',
    font=dict(size=14, family='Arial'),
    height=600,
    title_font=dict(size=20, family='Arial Black')
)

fig_sankey.write_html('sankey_magnitud_profundidad.html')
print("✓ Diagrama Sankey guardado: sankey_magnitud_profundidad.html")

# ============================================
# GRÁFICO 3: GRÁFICO 3D DE DISPERSIÓN - MAGNITUD, PROFUNDIDAD Y TIEMPO
# ============================================
print("\nGenerando gráfico 3D de dispersión...")

# Filtrar terremotos significativos
df_3d = df[df['Magnitude'] > 6.0].copy()
df_3d = df_3d.sample(min(2000, len(df_3d)))  # Limitar para mejor rendimiento

fig_3d = px.scatter_3d(
    df_3d,
    x='Longitude',
    y='Latitude',
    z='Depth',
    color='Magnitude',
    size='Magnitude',
    hover_data=['Date', 'Magnitude', 'Type'],
    color_continuous_scale='Viridis',
    title='Visualización 3D: Ubicación y Profundidad de Terremotos Mayores<br>Magnitud > 6.0',
    labels={
        'Longitude': 'Longitud',
        'Latitude': 'Latitud',
        'Depth': 'Profundidad (km)',
        'Magnitude': 'Magnitud'
    }
)

fig_3d.update_layout(
    scene=dict(
        xaxis_title='Longitud',
        yaxis_title='Latitud',
        zaxis_title='Profundidad (km)',
        zaxis=dict(autorange='reversed'),  # Profundidad hacia abajo
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.2)
        )
    ),
    height=700,
    title_font=dict(size=20, family='Arial Black')
)

fig_3d.write_html('terremotos_3d_scatter.html')
print("✓ Gráfico 3D guardado: terremotos_3d_scatter.html")

# ============================================
# GRÁFICO 4: TREEMAP - DISTRIBUCIÓN POR TIPO Y MAGNITUD
# ============================================
print("\nGenerando Treemap...")

# Preparar datos para treemap
df_treemap = df.groupby(['Type', 'Categoria_Magnitud']).size().reset_index(name='count')
df_treemap = df_treemap[df_treemap['count'] > 50]  # Filtrar categorías pequeñas

fig_treemap = px.treemap(
    df_treemap,
    path=['Type', 'Categoria_Magnitud'],
    values='count',
    color='count',
    color_continuous_scale='RdYlBu_r',
    title='Distribución Jerárquica de Eventos Sísmicos<br>Por Tipo y Categoría de Magnitud',
    labels={'count': 'Cantidad de Eventos'}
)

fig_treemap.update_layout(
    height=600,
    title_font=dict(size=20, family='Arial Black')
)

fig_treemap.update_traces(
    textinfo='label+value+percent parent',
    hovertemplate='<b>%{label}</b><br>Eventos: %{value}<br>%{percentParent}<extra></extra>'
)

fig_treemap.write_html('treemap_tipos_magnitud.html')
print("✓ Treemap guardado: treemap_tipos_magnitud.html")

# ============================================
# GRÁFICO 5: GRÁFICO DE RADAR - DISTRIBUCIÓN MENSUAL
# ============================================
print("\nGenerando gráfico de radar...")

# Distribución mensual de terremotos por categoría de magnitud
monthly_data = df.groupby(['Month', 'Categoria_Magnitud']).size().unstack(fill_value=0)

meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

fig_radar = go.Figure()

colors = ['#a50f15', '#de2d26', '#fb6a4a', '#fcae91', '#fee5d9']

for i, categoria in enumerate(mag_categories):
    if categoria in monthly_data.columns:
        fig_radar.add_trace(go.Scatterpolar(
            r=monthly_data[categoria].values,
            theta=meses,
            fill='toself',
            name=categoria,
            line=dict(color=colors[i]),
            opacity=0.7
        ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            gridcolor='lightgray'
        ),
        angularaxis=dict(
            gridcolor='lightgray'
        )
    ),
    showlegend=True,
    title='Distribución Mensual de Terremotos por Categoría de Magnitud<br>Patrón Circular Anual',
    height=600,
    title_font=dict(size=20, family='Arial Black'),
    legend=dict(
        orientation='v',
        yanchor='middle',
        y=0.5,
        xanchor='left',
        x=1.1
    )
)

fig_radar.write_html('radar_distribucion_mensual.html')
print("✓ Gráfico de radar guardado: radar_distribucion_mensual.html")

# ============================================
# GRÁFICO 6: GRÁFICO DE CASCADA (WATERFALL)
# ============================================
print("\nGenerando gráfico de cascada...")

# Evolución de terremotos mayores por década
decade_major = df[df['Magnitude'] >= 7.0].groupby('Decade').size().reset_index(name='count')
decade_major = decade_major.sort_values('Decade')

# Calcular cambios
changes = [decade_major.iloc[0]['count']]
for i in range(1, len(decade_major)):
    changes.append(decade_major.iloc[i]['count'] - decade_major.iloc[i-1]['count'])

# Crear labels
labels = [str(int(d)) for d in decade_major['Decade']]
labels.append('Total Acumulado')

# Preparar valores para waterfall
measures = ['absolute'] + ['relative'] * (len(changes) - 1) + ['total']
values = changes + [decade_major['count'].sum()]

fig_waterfall = go.Figure(go.Waterfall(
    name='Terremotos',
    orientation='v',
    measure=measures,
    x=labels,
    textposition='outside',
    text=[f"+{v}" if v > 0 else str(v) for v in values],
    y=values,
    connector={'line': {'color': 'rgb(63, 63, 63)'}},
    increasing={'marker': {'color': '#fb6a4a'}},
    decreasing={'marker': {'color': '#3182bd'}},
    totals={'marker': {'color': '#31a354'}}
))

fig_waterfall.update_layout(
    title='Evolución Temporal de Terremotos Mayores (Magnitud ≥ 7.0)<br>Cambio por Década',
    showlegend=False,
    height=600,
    title_font=dict(size=20, family='Arial Black'),
    xaxis_title='Década',
    yaxis_title='Cantidad de Terremotos Mayores'
)

fig_waterfall.write_html('waterfall_evolucion_decadas.html')
print("✓ Gráfico de cascada guardado: waterfall_evolucion_decadas.html")

# ============================================
# GRÁFICO 7: HEATMAP INTERACTIVO CON ANIMACIÓN
# ============================================
print("\nGenerando heatmap interactivo...")

# Crear matriz año-mes de terremotos significativos
df_heatmap = df[df['Magnitude'] >= 6.0].copy()
pivot_data = df_heatmap.groupby(['Year', 'Month']).size().reset_index(name='count')
pivot_matrix = pivot_data.pivot(index='Month', columns='Year', values='count').fillna(0)

fig_heatmap = px.imshow(
    pivot_matrix,
    labels=dict(x='Año', y='Mes', color='Cantidad'),
    x=pivot_matrix.columns,
    y=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    color_continuous_scale='YlOrRd',
    title='Intensidad Temporal de Terremotos Significativos (Magnitud ≥ 6.0)<br>Mapa de Calor Año-Mes',
    aspect='auto'
)

fig_heatmap.update_layout(
    height=600,
    title_font=dict(size=20, family='Arial Black'),
    xaxis_title='Año',
    yaxis_title='Mes'
)

fig_heatmap.update_xaxes(side='bottom')

fig_heatmap.write_html('heatmap_temporal.html')
print("✓ Heatmap guardado: heatmap_temporal.html")

# ============================================
# ESTADÍSTICAS PARA EL REPORTE
# ============================================
print("\n" + "="*50)
print("ESTADÍSTICAS PARA EL REPORTE")
print("="*50)

print(f"\n📊 INFORMACIÓN DEL DATASET:")
print(f"   • Total de registros: {len(df):,}")
print(f"   • Rango temporal: {df['Year'].min()} - {df['Year'].max()}")
print(f"   • Tipos de eventos: {df['Type'].nunique()}")
print(f"   • Principales tipos: {', '.join(df['Type'].value_counts().head(3).index.tolist())}")

print(f"\n📈 MAGNITUDES:")
print(f"   • Magnitud mínima: {df['Magnitude'].min():.2f}")
print(f"   • Magnitud máxima: {df['Magnitude'].max():.2f}")
print(f"   • Magnitud promedio: {df['Magnitude'].mean():.2f}")
print(f"   • Terremotos ≥ 7.0: {len(df[df['Magnitude'] >= 7.0]):,}")
print(f"   • Terremotos ≥ 8.0: {len(df[df['Magnitude'] >= 8.0]):,}")

print(f"\n🌍 DISTRIBUCIÓN GEOGRÁFICA:")
print(f"   • Latitud: {df['Latitude'].min():.2f}° a {df['Latitude'].max():.2f}°")
print(f"   • Longitud: {df['Longitude'].min():.2f}° a {df['Longitude'].max():.2f}°")

print(f"\n⬇️ PROFUNDIDAD:")
df_depth = df.dropna(subset=['Depth'])
print(f"   • Profundidad mínima: {df_depth['Depth'].min():.2f} km")
print(f"   • Profundidad máxima: {df_depth['Depth'].max():.2f} km")
print(f"   • Profundidad promedio: {df_depth['Depth'].mean():.2f} km")

print("\n✅ Todos los gráficos generados exitosamente!")
print("\nArchivos creados:")
print("  1. mapa_terremotos_3d.html")
print("  2. sankey_magnitud_profundidad.html")
print("  3. terremotos_3d_scatter.html")
print("  4. treemap_tipos_magnitud.html")
print("  5. radar_distribucion_mensual.html")
print("  6. waterfall_evolucion_decadas.html")
print("  7. heatmap_temporal.html")
