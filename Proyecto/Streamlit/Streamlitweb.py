import os
import requests
import streamlit as st
import pandas as pd
import joblib  # Importar joblib para cargar el modelo
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Archivos CSV
archivos_csv = {
    0: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Elche-Limpio.csv',
    1: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Orihuela-Limpio.csv',
    2: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Torrevieja-Limpio.csv'
}

# Estilo de la página
st.set_page_config(page_title="Predicción de Gases", page_icon="⛅", layout="centered")

# Título principal
st.title("⛅ Predicción de Gases Contaminantes ⛅")
st.markdown("### Bienvenido a la herramienta de predicción de gases. Selecciona el gas y proporciona los parámetros necesarios para obtener la predicción.")

# Selección del gas
st.sidebar.header("Configuración de Predicción")
gas_seleccionado = st.sidebar.selectbox("Selecciona el gas a predecir", ["SO2", "CO", "O3"])

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

# Cargar el modelo preentrenado desde la URL pública
url_modelo = "https://storage.cloud.google.com/almacenamientoproyectocontaminacion/SO2_model.pkl?authuser=1"
response = requests.get(url_modelo)

# Guardar el archivo .pkl en el sistema local temporalmente
with open("/tmp/SO2_model.pkl", "wb") as f:
    f.write(response.content)

# Cargar el modelo desde el archivo .pkl
modelo = joblib.load("/tmp/SO2_model.pkl")

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

# Mostrar los datos ingresados
st.write("### Datos ingresados para la predicción:")
st.dataframe(X_input)

# Predicción
if st.button("Predecir"):
    prediction = modelo.predict(X_input)[0]
    st.success(f"El valor predicho para {gas_seleccionado} es: {prediction:.2f}")
    st.balloons()

# Pie de página
st.markdown("---")
st.markdown("**Desarrollado por [Isaac Abarca | Javi Gomez | Troy Barker]** • [GitHub](https://github.com/Isaac916/ProyectoContaminaci-n) • © 2025")
