from io import BytesIO
import os
import pickle
import requests
import streamlit as st
import pandas as pd
from joblib import load, dump

# Obtener la ruta del directorio actual del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir las rutas relativas de los archivos CSV
archivos_csv = {
    0: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Elche-Limpio.csv',
    1: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Orihuela-Limpio.csv',
    2: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Torrevieja-Limpio.csv'
}

modelos = {
    "SO2": 'https://storage.cloud.google.com/almacenamientoproyectocontaminacion/SO2_model.pkl?authuser=1',
    "CO": 'https://storage.cloud.google.com/almacenamientoproyectocontaminacion/SO2_model.pkl?authuser=1',
    "O3": 'https://storage.cloud.google.com/almacenamientoproyectocontaminacion/SO2_model.pkl?authuser=1'
}

# Estilo de la página
st.set_page_config(page_title="Predicción de Gases", page_icon="⛅", layout="centered")

# Título principal
st.title("⛅ Predicción de Gases Contaminantes ⛅")
st.markdown("### Bienvenido a la herramienta de predicción de gases. Selecciona el gas y proporciona los parámetros necesarios para obtener la predicción.")

def descargar_modelo(url):
    try:
        response = requests.get(url)
        # Verificar si la respuesta es exitosa y contiene datos binarios
        if response.status_code == 200:
            # Verificar si el contenido parece un archivo binario adecuado (típicamente .pkl)
            if b'PK' in response.content[:2]:  # Esto es solo una comprobación inicial
                return BytesIO(response.content)
            else:
                st.error("El archivo descargado no parece ser un archivo binario válido.")
                return None
        else:
            st.error(f"Error al descargar el archivo: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error al intentar descargar el modelo: {e}")
        return None

# Establecer el gas a predecir
gas_seleccionado = "SO2"  # Cambia esto por el gas deseado
modelo_url = 'https://storage.cloud.google.com/almacenamientoproyectocontaminacion/SO2_model.pkl?authuser=1'

# Intentar descargar el modelo
modelo_data = descargar_modelo(modelo_url)

if modelo_data:
    try:
        # Cargar el modelo desde el archivo descargado (usando BytesIO para manejar datos binarios)
        modelo = load(modelo_data)
        st.success("Modelo cargado correctamente.")
    except Exception as e:
        st.error(f"Error al cargar el modelo con joblib: {e}")
else:
    st.error("No se pudo cargar el modelo desde la URL.")

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

# Descargar el modelo
modelo_url = modelos[gas_seleccionado]
modelo_path = f'{gas_seleccionado}_model.pkl'  # Ruta temporal para guardar el archivo

# Descargar y cargar el modelo
if descargar_modelo(modelo_url, modelo_path):
    try:
        # Cargar el modelo con joblib
        modelo = load(modelo_path)
        st.success("Modelo cargado correctamente.")
    except Exception as e:
        st.error(f"Error al cargar el modelo: {e}")
    
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
        if 'modelo' in locals():
            # Realizar la predicción
            prediccion = modelo.predict(X_input)[0]
            st.success(f"El valor predicho para {gas_seleccionado} es: {prediccion:.2f}")
            st.balloons()
        else:
            st.error("Modelo no cargado correctamente, no se puede hacer la predicción.")
else:
    st.error("No se pudo cargar el modelo desde la URL.")

# Pie de página
st.markdown("---")
st.markdown("**Desarrollado por [Isaac Abarca | Javi Gomez | Troy Barker]** • [GitHub](https://github.com/Isaac916/ProyectoContaminaci-n) • © 2025")
