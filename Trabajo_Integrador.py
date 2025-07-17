import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Desplazamiento y Precipitación",
    page_icon="📊",
    layout="wide"
)

def process_excel_data(df):
    """
    Procesa los datos del Excel para crear la gráfica
    """
    # Limpiar los datos
    df_clean = df.copy()
    
    # Remover filas completamente vacías
    df_clean = df_clean.dropna(how='all')
    
    # Convertir las fechas
    if 'FECHA' in df_clean.columns:
        # Intentar convertir fechas en formato día/mes/año
        try:
            df_clean['FECHA'] = pd.to_datetime(df_clean['FECHA'], format='%d/%m/%Y', errors='coerce')
        except:
            # Si falla, intentar otros formatos
            df_clean['FECHA'] = pd.to_datetime(df_clean['FECHA'], errors='coerce')
    
    # Convertir valores numéricos (reemplazar comas por puntos)
    numeric_columns = []
    for col in df_clean.columns:
        if col not in ['FECHA', 'Unnamed: 1']:  # Excluir columnas no numéricas
            try:
                # Reemplazar comas por puntos si es string
                if df_clean[col].dtype == 'object':
                    df_clean[col] = df_clean[col].astype(str).str.replace(',', '.')
                
                # Convertir a numérico
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                numeric_columns.append(col)
            except:
                pass
    
    return df_clean, numeric_columns

def calculate_displacement_statistics(df, selected_points):
    """
    Calcula estadísticas avanzadas de desplazamiento
    """
    stats = {}
    
    for point in selected_points:
        if point in df.columns:
            # Filtrar datos válidos
            valid_data = df[df[point].notna() & df['FECHA'].notna()].copy()
            valid_data = valid_data.sort_values('FECHA')
            
            if len(valid_data) > 1:
                # Calcular diferencias temporales en días
                valid_data['days_diff'] = (valid_data['FECHA'] - valid_data['FECHA'].shift(1)).dt.days
                valid_data['displacement_diff'] = valid_data[point] - valid_data[point].shift(1)
                
                # Calcular velocidades (mm/día)
                valid_data['velocity'] = valid_data['displacement_diff'] / valid_data['days_diff']
                
                # Estadísticas del punto
                stats[point] = {
                    'total_displacement': valid_data[point].iloc[-1] - valid_data[point].iloc[0],
                    'max_displacement': valid_data[point].max(),
                    'min_displacement': valid_data[point].min(),
                    'average_velocity': valid_data['velocity'].mean(),
                    'max_velocity': valid_data['velocity'].max(),
                    'min_velocity': valid_data['velocity'].min(),
                    'max_velocity_date': valid_data.loc[valid_data['velocity'].idxmax(), 'FECHA'],
                    'min_velocity_date': valid_data.loc[valid_data['velocity'].idxmin(), 'FECHA'],
                    'total_days': (valid_data['FECHA'].iloc[-1] - valid_data['FECHA'].iloc[0]).days,
                    'measurements_count': len(valid_data)
                }
    
    return stats

def find_critical_events(df, selected_points, rainfall_col):
    """
    Encuentra eventos críticos en los datos
    """
    events = {
        'max_displacement_events': [],
        'max_velocity_events': [],
        'high_rainfall_events': [],
        'correlation_events': []
    }
    
    # Eventos de máximo desplazamiento
    for point in selected_points:
        if point in df.columns:
            max_disp_idx = df[point].idxmax()
            if pd.notna(max_disp_idx):
                events['max_displacement_events'].append({
                    'point': point,
                    'date': df.loc[max_disp_idx, 'FECHA'],
                    'value': df.loc[max_disp_idx, point]
                })
    
    # Eventos de alta precipitación
    if rainfall_col in df.columns:
        high_rainfall_threshold = df[rainfall_col].quantile(0.9)
        high_rainfall_events = df[df[rainfall_col] > high_rainfall_threshold]
        
        for idx, row in high_rainfall_events.iterrows():
            events['high_rainfall_events'].append({
                'date': row['FECHA'],
                'rainfall': row[rainfall_col]
            })
    
    return events

def create_displacement_chart(df, selected_points, rainfall_col='rainfall (mm)'):
    """
    Crea la gráfica de desplazamiento y precipitación
    """
    # Crear figura con dos ejes Y
    fig, ax1 = plt.subplots(figsize=(15, 8))
    
    # Colores para cada punto
    colors = ['#2E8B57', '#FF6347', '#4682B4', '#9ACD32', '#FF1493', '#FFD700', '#8A2BE2', '#FF4500']
    
    # Graficar puntos de desplazamiento
    for i, point in enumerate(selected_points):
        if point in df.columns:
            color = colors[i % len(colors)]
            ax1.scatter(df['FECHA'], df[point], 
                       color=color, label=point, s=30, alpha=0.7)
    
    # Configurar primer eje Y (desplazamiento)
    ax1.set_xlabel('Fecha', fontsize=12)
    ax1.set_ylabel('Displacement (mm)', fontsize=12, color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(True, alpha=0.3)
    
    # Configurar el eje X
    ax1.tick_params(axis='x', rotation=45)
    
    # Crear segundo eje Y para precipitación
    ax2 = ax1.twinx()
    
    # Graficar precipitación como barras
    if rainfall_col in df.columns:
        # Filtrar valores no nulos
        rainfall_data = df[df[rainfall_col].notna()]
        
        # Crear barras
        bars = ax2.bar(rainfall_data['FECHA'], rainfall_data[rainfall_col], 
                      color='lightblue', alpha=0.6, width=20, 
                      label='Rainfall (mm)')
        
        # Agregar etiquetas en algunas barras importantes
        max_rainfall = rainfall_data[rainfall_col].max()
        for i, (date, value) in enumerate(zip(rainfall_data['FECHA'], rainfall_data[rainfall_col])):
            if value > max_rainfall * 0.8:  # Mostrar etiqueta si es mayor al 80% del máximo
                ax2.annotate(f'{value:.1f}', 
                           xy=(date, value), 
                           xytext=(0, 5), 
                           textcoords='offset points',
                           ha='center', va='bottom',
                           fontsize=8)
    
    # Configurar segundo eje Y
    ax2.set_ylabel('Monthly precipitation (mm)', fontsize=12, color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.set_ylim(0, df[rainfall_col].max() * 1.1 if rainfall_col in df.columns else 200)
    
    # Configurar límites del eje Y izquierdo
    y_min = min([df[col].min() for col in selected_points if col in df.columns])
    y_max = max([df[col].max() for col in selected_points if col in df.columns])
    margin = (y_max - y_min) * 0.1
    ax1.set_ylim(y_min - margin, y_max + margin)
    
    # Leyenda
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, 
              loc='upper left', bbox_to_anchor=(0, 1))
    
    # Título
    plt.title('Displacement Points vs Monthly Precipitation', fontsize=14, pad=20)
    
    # Ajustar layout
    plt.tight_layout()
    
    return fig

def create_velocity_chart(df, selected_points):
    """
    Crea gráfica de velocidad de desplazamiento
    """
    fig, ax = plt.subplots(figsize=(15, 6))
    
    colors = ['#2E8B57', '#FF6347', '#4682B4', '#9ACD32', '#FF1493', '#FFD700', '#8A2BE2', '#FF4500']
    
    for i, point in enumerate(selected_points):
        if point in df.columns:
            # Calcular velocidad
            valid_data = df[df[point].notna() & df['FECHA'].notna()].copy()
            valid_data = valid_data.sort_values('FECHA')
            
            if len(valid_data) > 1:
                valid_data['days_diff'] = (valid_data['FECHA'] - valid_data['FECHA'].shift(1)).dt.days
                valid_data['displacement_diff'] = valid_data[point] - valid_data[point].shift(1)
                valid_data['velocity'] = valid_data['displacement_diff'] / valid_data['days_diff']
                
                color = colors[i % len(colors)]
                ax.plot(valid_data['FECHA'], valid_data['velocity'], 
                       color=color, label=f'{point} velocity', marker='o', markersize=4)
    
    ax.set_xlabel('Fecha', fontsize=12)
    ax.set_ylabel('Velocity (mm/day)', fontsize=12)
    ax.set_title('Displacement Velocity Over Time', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def main():
    st.title("📊 Análisis de Desplazamiento y Precipitación")
    st.markdown("---")
    
    # Sidebar para configuración
    st.sidebar.header("⚙️ Configuración")
    
    # Cargar archivo
    uploaded_file = st.file_uploader(
        "Cargar archivo Excel", 
        type=['xlsx', 'xls'],
        help="Selecciona un archivo Excel con datos de desplazamiento y precipitación"
    )
    
    if uploaded_file is not None:
        try:
            # Leer el archivo Excel
            df = pd.read_excel(uploaded_file)
            
            # Mostrar vista previa de los datos
            st.subheader("📋 Vista previa de los datos")
            st.dataframe(df.head(10))
            
            # Procesar datos
            df_processed, numeric_columns = process_excel_data(df)
            
            # Filtrar columnas de puntos de desplazamiento
            displacement_points = [col for col in numeric_columns 
                                 if col.isdigit() and col not in ['rainfall (mm)', 'rainfall']]
            
            # Sidebar - Selección de puntos
            st.sidebar.subheader("📍 Seleccionar Puntos de Desplazamiento")
            
            # Preseleccionar algunos puntos comunes
            default_points = ['53763', '53834', '53948', '54092']
            available_defaults = [p for p in default_points if p in displacement_points]
            
            selected_points = st.sidebar.multiselect(
                "Puntos a graficar:",
                options=displacement_points,
                default=available_defaults if available_defaults else displacement_points[:4],
                help="Selecciona hasta 8 puntos para graficar"
            )
            
            # Seleccionar columna de precipitación
            rainfall_columns = [col for col in df_processed.columns 
                              if 'rainfall' in col.lower() or 'precipit' in col.lower()]
            
            if rainfall_columns:
                rainfall_col = st.sidebar.selectbox(
                    "Columna de precipitación:",
                    options=rainfall_columns,
                    index=0
                )
            else:
                rainfall_col = None
                st.sidebar.warning("No se encontró columna de precipitación")
            
            # Información de los datos
            st.sidebar.subheader("📊 Información de los datos")
            st.sidebar.info(f"""
            **Registros:** {len(df_processed)}
            **Puntos disponibles:** {len(displacement_points)}
            **Rango de fechas:** {df_processed['FECHA'].min().strftime('%Y-%m-%d') if 'FECHA' in df_processed.columns else 'N/A'} 
            a {df_processed['FECHA'].max().strftime('%Y-%m-%d') if 'FECHA' in df_processed.columns else 'N/A'}
            """)
            
            # Crear gráfica
            if selected_points and 'FECHA' in df_processed.columns:
                st.subheader("📈 Gráfica de Desplazamiento vs Precipitación")
                
                # Crear la gráfica
                fig = create_displacement_chart(df_processed, selected_points, rainfall_col)
                
                # Mostrar gráfica
                st.pyplot(fig)
                
                # Opción para descargar la gráfica
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                buf.seek(0)
                
                st.download_button(
                    label="💾 Descargar gráfica",
                    data=buf,
                    file_name="displacement_precipitation_chart.png",
                    mime="image/png"
                )
                
                # === FUNCIONALIDADES ADICIONALES OBLIGATORIAS ===
                
                # 1. Calcular estadísticas avanzadas de desplazamiento
                st.subheader("🔍 Análisis Avanzado de Desplazamiento")
                
                displacement_stats = calculate_displacement_statistics(df_processed, selected_points)
                
                # Mostrar velocidades medias
                st.subheader("⚡ Velocidades Medias de Desplazamiento")
                
                if displacement_stats:
                    velocity_data = []
                    for point, stats in displacement_stats.items():
                        velocity_data.append({
                            'Punto': point,
                            'Velocidad Media (mm/día)': f"{stats['average_velocity']:.4f}",
                            'Velocidad Máxima (mm/día)': f"{stats['max_velocity']:.4f}",
                            'Velocidad Mínima (mm/día)': f"{stats['min_velocity']:.4f}",
                            'Desplazamiento Total (mm)': f"{stats['total_displacement']:.3f}",
                            'Período (días)': stats['total_days']
                        })
                    
                    velocity_df = pd.DataFrame(velocity_data)
                    st.dataframe(velocity_df, use_container_width=True)
                
                # 2. Fechas con mayor tasa de desplazamiento
                st.subheader("📅 Fechas con Mayor Tasa de Desplazamiento")
                
                max_velocity_events = []
                for point, stats in displacement_stats.items():
                    if pd.notna(stats['max_velocity_date']):
                        max_velocity_events.append({
                            'Punto': point,
                            'Fecha': stats['max_velocity_date'].strftime('%d/%m/%Y'),
                            'Velocidad Máxima (mm/día)': f"{stats['max_velocity']:.4f}",
                            'Tipo': 'Máxima velocidad'
                        })
                
                if max_velocity_events:
                    events_df = pd.DataFrame(max_velocity_events)
                    st.dataframe(events_df, use_container_width=True)
                
                # 3. Gráfica de velocidad
                st.subheader("📊 Gráfica de Velocidad de Desplazamiento")
                
                velocity_fig = create_velocity_chart(df_processed, selected_points)
                st.pyplot(velocity_fig)
                
                # 4. Eventos críticos
                st.subheader("⚠️ Eventos Críticos")
                
                critical_events = find_critical_events(df_processed, selected_points, rainfall_col)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🎯 Desplazamientos Máximos:**")
                    if critical_events['max_displacement_events']:
                        for event in critical_events['max_displacement_events']:
                            st.write(f"• **{event['point']}**: {event['value']:.3f} mm el {event['date'].strftime('%d/%m/%Y')}")
                    else:
                        st.write("No hay eventos registrados")
                
                with col2:
                    st.write("**🌧️ Precipitaciones Altas (>90% percentil):**")
                    if critical_events['high_rainfall_events']:
                        for event in critical_events['high_rainfall_events'][:5]:  # Mostrar solo los primeros 5
                            st.write(f"• {event['rainfall']:.1f} mm el {event['date'].strftime('%d/%m/%Y')}")
                    else:
                        st.write("No hay eventos registrados")
                
                # 5. Análisis de correlación
                st.subheader("📈 Análisis de Correlación")
                
                if rainfall_col in df_processed.columns:
                    correlation_data = []
                    for point in selected_points:
                        if point in df_processed.columns:
                            corr_coeff = df_processed[point].corr(df_processed[rainfall_col])
                            if pd.notna(corr_coeff):
                                correlation_data.append({
                                    'Punto': point,
                                    'Correlación con Precipitación': f"{corr_coeff:.3f}",
                                    'Interpretación': 'Fuerte' if abs(corr_coeff) > 0.7 else 'Moderada' if abs(corr_coeff) > 0.3 else 'Débil'
                                })
                    
                    if correlation_data:
                        corr_df = pd.DataFrame(correlation_data)
                        st.dataframe(corr_df, use_container_width=True)
                
                # Mostrar estadísticas básicas
                st.subheader("📊 Estadísticas Básicas")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Estadísticas de Desplazamiento:**")
                    stats_df = df_processed[selected_points].describe()
                    st.dataframe(stats_df)
                
                with col2:
                    if rainfall_col:
                        st.write("**Estadísticas de Precipitación:**")
                        rainfall_stats = df_processed[rainfall_col].describe()
                        st.dataframe(rainfall_stats.to_frame(name=rainfall_col))
                
            else:
                st.warning("⚠️ Selecciona al menos un punto de desplazamiento para crear la gráfica")
                
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")
            st.info("💡 Asegúrate de que el archivo tenga el formato correcto con columnas de fecha, puntos de desplazamiento y precipitación")
    
    else:
        # Mostrar ejemplo de datos esperados
        st.info("📤 Sube un archivo Excel para comenzar el análisis")
        
        st.subheader("📋 Formato de datos esperado")
        st.markdown("""
        El archivo Excel debe contener:
        - **Columna FECHA**: Fechas en formato DD/MM/YYYY
        - **Columnas numéricas**: Puntos de desplazamiento (ej: 53763, 53834, etc.)
        - **Columna rainfall (mm)**: Datos de precipitación mensual
        
        Ejemplo de estructura:
        """)
        
        # Crear ejemplo de datos
        example_data = {
            'FECHA': ['28/4/2015', '30/11/2015', '24/12/2015'],
            '53763': [0.0, 0.0395, -0.0882],
            '53834': [0.0, 0.2015, 0.0558],
            '53948': [0.0, -0.0033, -0.3386],
            'rainfall (mm)': [0.0, 18.73, 28.95]
        }
        
        st.dataframe(pd.DataFrame(example_data))

if __name__ == "__main__":
    main()