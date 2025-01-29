import streamlit as st
import pandas as pd
import requests
from io import StringIO
import plotly.express as px

archivos_csv = {
    0: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Elche-Limpio.csv',
    1: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Orihuela-Limpio.csv',
    2: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Torrevieja-Limpio.csv'
}

st.set_page_config(page_title="Visualización de Series Temporales", page_icon="📈", layout="centered")

st.title("📈 Visualización de Series Temporales de Gases Contaminantes")
st.markdown("### Explora los datos de concentración de gases en diferentes estaciones.")

st.sidebar.header("Configuración de Visualización")
nom_estacion = st.sidebar.selectbox("Selecciona la estación", ["ELX - AGROALIMENTARI", "ORIHUELA", "TORREVIEJA"])
gas_seleccionado = st.sidebar.selectbox("Selecciona el gas a visualizar", ["SO2", "CO", "O3"])

estaciones_codificadas = {"ELX - AGROALIMENTARI": 0, "ORIHUELA": 1, "TORREVIEJA": 2}
nom_estacion_codificado = estaciones_codificadas[nom_estacion]

st.markdown("### Datos de la estación seleccionada:")
try:
    pd.set_option("styler.render.max_elements", None)

    csv_url = archivos_csv[nom_estacion_codificado]
    response = requests.get(csv_url)
    response.raise_for_status()
    data = pd.read_csv(StringIO(response.text), sep=';', decimal=',')

    columnas_relevantes = ['FECHA', 'HORA', 'NOM_ESTACION', 'SO2', 'CO', 'O3']
    data = data[columnas_relevantes]

    data = data.dropna(subset=['FECHA', 'HORA', 'NOM_ESTACION', 'SO2', 'CO', 'O3'])

    st.dataframe(data)

    if gas_seleccionado not in data.columns:
        st.error(f"El gas seleccionado ({gas_seleccionado}) no se encuentra en los datos disponibles.")
    else:
        if 'FECHA' in data.columns:
            data['FECHA'] = pd.to_datetime(data['FECHA'], errors='coerce')

        st.markdown("### Gráfica de la serie temporal para el gas seleccionado:")
        fig = px.line(
            data, x='FECHA', y=gas_seleccionado,
            title=f"Concentración de {gas_seleccionado} en {nom_estacion}",
            labels={"FECHA": "Fecha", gas_seleccionado: f"Concentración de {gas_seleccionado}"},
            template="plotly_white"
        )
        st.plotly_chart(fig)

except Exception as e:
    st.error(f"Error al cargar los datos de la estación desde GitHub: {e}")

st.markdown("---")
st.markdown("**Desarrollado por [Isaac Abarca | Javi Gomez | Troy Barker]** • [GitHub](https://github.com/Isaac916/ProyectoContaminaci-n) • © 2025")