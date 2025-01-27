import joblib
import os
import streamlit as st
import pandas as pd
import requests

# Diccionario con enlaces directos a los archivos CSV en GitHub (usando raw)
archivos_csv = {
    0: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Elche-Limpio.csv',
    1: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Orihuela-Limpio.csv',
    2: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Torrevieja-Limpio.csv'
}

# Diccionario de modelos con enlaces crudos a los archivos .pkl
modelos = {   
    "SO2": 'https://storage.cloud.google.com/almacenamientoproyectocontaminacion/SO2_model.pkl?authuser=1',
    "CO": 'https://storage.cloud.google.com/almacenamientoproyectocontaminacion/CO_model.pkl?authuser=1',
    "O3": 'https://storage.cloud.google.com/almacenamientoproyectocontaminacion/O3_model.pkl?authuser=1'
}

# Estilo de la página
st.set_page_config(page_title="Predicción de Gases", page_icon="⛅", layout="centered")

# Título principal
st.title("⛅ Predicción de Gases Contaminantes ⛅")
st.markdown("### Bienvenido a la herramienta de predicción de gases. Selecciona el gas y proporciona los parámetros necesarios para obtener la predicción.")

# Selección del gas
st.sidebar.header("Configuración de Predicción")
gas_seleccionado = st.sidebar.selectbox("Selecciona el gas a predecir", list(modelos.keys()))

# Selección de la estación
nom_estacion = st.sidebar.selectbox("Nombre de la estación", ["ELX - AGROALIMENTARI", "ORIHUELA", "TORREVIEJA"])

# Convertir la estación a códigos (igual que en el entrenamiento)
estaciones_codificadas = {"ELX - AGROALIMENTARI": 0, "ORIHUELA": 1, "TORREVIEJA": 2}
nom_estacion_codificado = estaciones_codificadas[nom_estacion]

# Cargar el archivo CSV de acuerdo a la estación seleccionada
csv_path = archivos_csv[nom_estacion_codificado]
data = pd.read_csv(csv_path, sep=';', decimal=',')

# Mostrar una tabla con los primeros datos (opcional)
with st.expander("Ver datos de muestra"):
    st.write(data.head(10))

# Función para descargar el archivo desde Google Cloud Storage utilizando requests
def descargar_modelo(url, output):
    response = requests.get(url, stream=True)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        with open(output, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return True
    else:
        st.error("Error al descargar el modelo.")
        return False

# Función para cargar el modelo con caché
@st.cache_resource
def cargar_modelo(url):
    output = 'modelo.pkl'
    if descargar_modelo(url, output):
        # Usamos joblib en lugar de pickle
        import joblib
        modelo = joblib.load(output)
        return modelo
    return None

# Cargar el modelo del gas seleccionado desde la URL con caché
modelo_url = modelos[gas_seleccionado]
with st.spinner('Cargando el modelo...'):
    modelo = cargar_modelo(modelo_url)
st.success("Modelo cargado correctamente")

# Inputs del usuario
st.sidebar.subheader("Parámetros de entrada")
año = st.sidebar.number_input("Año", min_value=2000, max_value=2100, step=1, value=2023)
mes = st.sidebar.number_input("Mes", min_value=1, max_value=12, step=1, value=1)
dia = st.sidebar.number_input("Día", min_value=1, max_value=31, step=1, value=1)
hora = st.sidebar.number_input("Hora", min_value=0, max_value=23, step=1, value=12)

# Crear el DataFrame para la predicción
X_input = pd.DataFrame({
    "año": [año],
    "mes": [mes],
    "dia": [dia],
    "HORA": [hora],
    "NOM_ESTACION": [nom_estacion_codificado]
})

# Mostrar el input en pantalla
st.write("### Datos ingresados para la predicción:")
st.dataframe(X_input)

# Botón para realizar la predicción
if st.button("Predecir"):
    # Verificar si el modelo fue cargado correctamente
    if modelo is not None:
        # Realizar la predicción
        prediccion = modelo.predict(X_input)[0]
        st.success(f"El valor predicho para {gas_seleccionado} es: {prediccion:.2f}")
        st.balloons()
    else:
        st.error("No se pudo cargar el modelo.")
