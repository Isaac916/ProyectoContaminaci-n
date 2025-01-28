import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from io import StringIO

# Configuración de la página
st.set_page_config(page_title="Análisis de Contaminación", layout="wide")
st.title("📊 Análisis de Datos de Contaminación")
st.markdown("## Visualiza, filtra y analiza los datos de contaminación ambiental de Elche, Orihuela y Torrevieja.")

# URLs de los CSV en GitHub
archivos_csv = {
    0: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Elche-Limpio.csv',
    1: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Orihuela-Limpio.csv',
    2: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Torrevieja-Limpio.csv'
}

# Función para cargar los datos
def cargar_datos(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text), sep=';')
        return data
    else:
        st.error(f"Error al cargar el archivo desde {url}")
        return None

# Cargar los datos
st.sidebar.header("Configuración de datos")
estacion_opcion = st.sidebar.selectbox("Selecciona la estación de monitoreo:", ["ELX - AGROALIMENTARI", "ORIHUELA", "TORREVIEJA"])
estacion_index = ["ELX - AGROALIMENTARI", "ORIHUELA", "TORREVIEJA"].index(estacion_opcion)
data = cargar_datos(archivos_csv[estacion_index])

if data is not None:
    st.sidebar.markdown("### Opciones de filtrado")
    columnas_seleccionadas = st.sidebar.multiselect("Selecciona las columnas a mostrar:", data.columns, default=data.columns)
    data_filtrada = data[columnas_seleccionadas]

    st.markdown(f"### Datos de la estación: {estacion_opcion}")
    st.dataframe(data_filtrada, use_container_width=True)

    # Gráficos
    st.markdown("## Visualizaciones")

    # Gráfico de línea
    st.markdown("### Evolución temporal de contaminantes")
    contaminante = st.selectbox("Selecciona un contaminante:", ["SO2", "CO", "NO", "NO2", "NOx", "O3"])
    if contaminante in data.columns:
        fig_line = px.line(data, x="FECHA", y=contaminante, title=f"Evolución de {contaminante} en el tiempo")
        st.plotly_chart(fig_line, use_container_width=True)

    # Gráfico de dispersión
    st.markdown("### Relación entre contaminantes")
    x_axis = st.selectbox("Selecciona el eje X:", ["SO2", "CO", "NO", "NO2", "NOx", "O3"], key="x_axis")
    y_axis = st.selectbox("Selecciona el eje Y:", ["SO2", "CO", "NO", "NO2", "NOx", "O3"], key="y_axis")
    if x_axis in data.columns and y_axis in data.columns:
        fig_scatter = px.scatter(data, x=x_axis, y=y_axis, color="Temp.",
                                 title=f"Relación entre {x_axis} y {y_axis}")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Gráfico de barras
    st.markdown("### Promedio de contaminantes por hora")
    contaminante_bar = st.selectbox("Selecciona un contaminante para el gráfico de barras:", ["SO2", "CO", "NO", "NO2", "NOx", "O3"], key="bar")
    if contaminante_bar in data.columns:
        data_bar = data.groupby("HORA")[contaminante_bar].mean().reset_index()
        fig_bar = px.bar(data_bar, x="HORA", y=contaminante_bar, title=f"Promedio de {contaminante_bar} por hora")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de mapa (si hay coordenadas, opcional)
    if "Direc." in data.columns and "Veloc." in data.columns:
        st.markdown("### Dirección y velocidad del viento")
        fig_wind = px.scatter_polar(data, r="Veloc.", theta="Direc.", color="H.Rel.",
                                    title="Dirección y velocidad del viento")
        st.plotly_chart(fig_wind, use_container_width=True)

st.markdown("---")
st.markdown("**Desarrollado por [Isaac Abarca | Javi Gomez | Troy Barker]** • [GitHub](https://github.com/Isaac916/ProyectoContaminaci-n) • © 2025")