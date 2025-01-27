import streamlit as st
import pandas as pd
import requests
from io import StringIO
import plotly.express as px

# URLs de los CSV en GitHub
archivos_csv = {
    0: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Elche-Limpio.csv',
    1: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Orihuela-Limpio.csv',
    2: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Torrevieja-Limpio.csv'
}

# Estilo de la página
st.set_page_config(page_title="Visualización de Series Temporales", page_icon="📈", layout="centered")

# Título principal
st.title("📈 Visualización de Series Temporales de Gases Contaminantes")
st.markdown("### Explora los datos de concentración de gases en diferentes estaciones.")

# Sección 1: Selección de la estación y el gas
st.sidebar.header("Configuración de Visualización")
nom_estacion = st.sidebar.selectbox("Selecciona la estación", ["ELX - AGROALIMENTARI", "ORIHUELA", "TORREVIEJA"])
gas_seleccionado = st.sidebar.selectbox("Selecciona el gas a visualizar", ["SO2", "CO", "O3"])

# Convertir la estación a códigos
estaciones_codificadas = {"ELX - AGROALIMENTARI": 0, "ORIHUELA": 1, "TORREVIEJA": 2}
nom_estacion_codificado = estaciones_codificadas[nom_estacion]

# Sección 2: Cargar y mostrar los datos de la estación
st.markdown("### Datos de la estación seleccionada:")
try:
    # Cargar datos desde la URL
    csv_url = archivos_csv[nom_estacion_codificado]
    response = requests.get(csv_url)
    response.raise_for_status()
    data = pd.read_csv(StringIO(response.text), sep=';', decimal=',')

    # Mostrar datos de muestra
    st.write("Datos de muestra:")
    st.dataframe(data.head(10))

    # Validar que el gas seleccionado esté en las columnas
    if gas_seleccionado not in data.columns:
        st.error(f"El gas seleccionado ({gas_seleccionado}) no se encuentra en los datos disponibles.")
    else:
        # Convertir la columna de tiempo si existe
        if 'FECHA' in data.columns:
            data['FECHA'] = pd.to_datetime(data['FECHA'], errors='coerce')

        # Filtrar datos para el gas seleccionado y graficar
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

# Pie de página
st.markdown("---")
st.markdown("**Desarrollado por [Isaac Abarca | Javi Gomez | Troy Barker]** • [GitHub](https://github.com/Isaac916/ProyectoContaminaci-n) • © 2025")