import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Análisis de Desplazamiento y Precipitación")

# Subida del archivo Excel
uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leer el archivo Excel, omitiendo las primeras filas si es necesario
    df = pd.read_excel(uploaded_file, skiprows=3)

    st.subheader("Datos cargados:")
    st.write(df.head())

    # Intentar detectar la columna de fecha automáticamente
    fecha_col = None
    for col in df.columns:
        if 'fecha' in str(col).lower():
            fecha_col = col
            break

    if fecha_col:
        fecha = pd.to_datetime(df[fecha_col])
        st.success(f"Columna de fecha detectada: {fecha_col}")

        # Definir columnas a quitar si existen
        columnas_a_quitar = [fecha_col, 'Puntos']
        if 'rainfall (mm)' in df.columns:
            columnas_a_quitar.append('rainfall (mm)')

        # Obtener dataframe solo con desplazamientos
        desplazamientos = df.drop(columns=columnas_a_quitar, errors='ignore')

        # Obtener datos de lluvia si existen
        lluvia = df['rainfall (mm)'] if 'rainfall (mm)' in df.columns else None

        # Convertir columnas de desplazamientos a numérico
        for columna in desplazamientos.columns:
            desplazamientos[columna] = pd.to_numeric(desplazamientos[columna], errors='coerce')

        # Crear gráfica
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Graficar desplazamientos (scatter)
        for columna in desplazamientos.columns:
            ax1.scatter(fecha, desplazamientos[columna], label=str(columna), s=30)
        ax1.set_xlabel("Fecha")
        ax1.set_ylabel("Desplazamiento (cm)")
        ax1.tick_params(axis='x', rotation=45)

        # Eje secundario para lluvia si existe
        if lluvia is not None:
            ax2 = ax1.twinx()
            ax2.plot(fecha, lluvia, color='deepskyblue', linewidth=2, label='rainfall (mm)')
            ax2.set_ylabel("Precipitación mensual (mm)")

            # Leyendas combinadas
            lines_1, labels_1 = ax1.get_legend_handles_labels()
            lines_2, labels_2 = ax2.get_legend_handles_labels()
            ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
        else:
            ax1.legend(loc='upper right')

        st.pyplot(fig)

        # Análisis adicional: velocidad media de desplazamiento
        st.subheader("Análisis adicional")

        desplazamientos_mean_speed = {}

        for columna in desplazamientos.columns:
            diff = desplazamientos[columna].diff()
            days = fecha.diff().dt.days.fillna(1)
            speed = (diff / days).abs()
            velocidad_media = speed.mean()
            desplazamientos_mean_speed[columna] = velocidad_media

        st.write("Velocidad media de desplazamiento (cm/día):")
        st.write(desplazamientos_mean_speed)

        # Fecha con mayor tasa de desplazamiento
        st.write("Fecha con mayor tasa de desplazamiento:")
        for columna in desplazamientos.columns:
            diff = desplazamientos[columna].diff()
            days = fecha.diff().dt.days.fillna(1)
            speed = (diff / days).abs()
            max_speed = speed.max()
            max_date = fecha[speed.idxmax()]
            st.write(f"{columna}: {max_date.date()} → {max_speed:.4f} cm/día")

    else:
        st.error("No se encontró una columna de fecha. Asegúrate que tu archivo tenga una columna con 'fecha' en el nombre.")
else:
    st.info("Por favor, carga un archivo Excel para continuar.")
