import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.title("Análisis de Desplazamiento y Precipitación")

uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, skiprows=3)

    st.subheader("Datos cargados:")
    st.write(df.head())

    # Detectar columna de fecha
    fecha_col = None
    for col in df.columns:
        if 'fecha' in str(col).lower():
            fecha_col = col
            break

    if fecha_col:
        fecha = pd.to_datetime(df[fecha_col])
        st.success(f"Columna de fecha detectada: {fecha_col}")

        # Quitar columnas innecesarias
        columnas_a_quitar = [fecha_col, 'Puntos']
        if 'rainfall (mm)' in df.columns:
            columnas_a_quitar.append('rainfall (mm)')

        desplazamientos = df.drop(columns=columnas_a_quitar, errors='ignore')
        lluvia = df['rainfall (mm)'] if 'rainfall (mm)' in df.columns else None

        # Asegurar que sean valores numéricos
        for columna in desplazamientos.columns:
            desplazamientos[columna] = pd.to_numeric(desplazamientos[columna], errors='coerce')

        # Crear gráfico interactivo
        fig = go.Figure()

        for columna in desplazamientos.columns:
            hover_text = [
                f"Estación: {columna}<br>Fecha: {f.date()}<br>Desplazamiento: {v:.2f} cm"
                for f, v in zip(fecha, desplazamientos[columna])
            ]
            fig.add_trace(go.Scatter(
                x=fecha,
                y=desplazamientos[columna],
                mode='markers+lines',
                name=f'{columna} (cm)',
                yaxis='y1',
                hoverinfo='text',
                text=hover_text
            ))

        if lluvia is not None:
            hover_text_lluvia = [
                f"Fecha: {f.date()}<br>Precipitación: {v:.2f} mm"
                for f, v in zip(fecha, lluvia)
            ]
            fig.add_trace(go.Scatter(
                x=fecha,
                y=lluvia,
                mode='lines+markers',
                name='Precipitación (mm)',
                line=dict(color='deepskyblue'),
                yaxis='y2',
                hoverinfo='text',
                text=hover_text_lluvia
            ))

        fig.update_layout(
            title="Desplazamientos vs Precipitación",
            xaxis=dict(title='Fecha'),
            yaxis=dict(title='Desplazamiento (cm)', side='left'),
            yaxis2=dict(title='Precipitación (mm)', overlaying='y', side='right'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
            margin=dict(b=120),
            height=600,
            hovermode='closest'
        )

        st.plotly_chart(fig)

        # Análisis adicional corregido
        st.subheader("Análisis adicional de desplazamiento")

        desplazamientos_mean_speed = {}
        fecha_max_speed = {}

        for columna in desplazamientos.columns:
            serie = desplazamientos[columna]
            dif = serie.diff()
            delta_dias = fecha.diff().dt.days.fillna(1)
            velocidad = (dif / delta_dias).abs()

            # Limpiar NaN
            velocidad = velocidad.replace([float('inf'), -float('inf')], pd.NA).dropna()

            velocidad_media = velocidad.mean()
            desplazamientos_mean_speed[columna] = round(velocidad_media, 4)

            if not velocidad.empty:
                idx_max = velocidad.idxmax()
                fecha_max = fecha[idx_max]
                valor_max = velocidad[idx_max]
                fecha_max_speed[columna] = (fecha_max.date(), round(valor_max, 4))
            else:
                fecha_max_speed[columna] = ("Sin datos", 0)

        st.write("🔹 Velocidad media de desplazamiento (cm/día):")
        st.write(desplazamientos_mean_speed)

        st.write("🔸 Fecha con mayor tasa de desplazamiento:")
        for columna, (fecha_mayor, valor) in fecha_max_speed.items():
            st.write(f"{columna}: {fecha_mayor} → {valor} cm/día")

    else:
        st.error("❌ No se encontró una columna de fecha válida.")
else:
    st.info("⬆️ Por favor, carga un archivo Excel para continuar.")
