import streamlit as st
import pickle
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from io import StringIO

# Configuración de las credenciales de Google Cloud desde los secretos de Streamlit
google_cloud_credentials = st.secrets["google_cloud"]
credentials = service_account.Credentials.from_service_account_info(google_cloud_credentials)
storage_client = storage.Client(credentials=credentials, project=google_cloud_credentials["project_id"])

bucket_name = 'almacenamientoproyectocontaminacion'  # Cambia al nombre de tu bucket

# URLs de los archivos
archivos_csv = {
    0: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Elche-Limpio.csv',
    1: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Orihuela-Limpio.csv',
    2: 'https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Torrevieja-Limpio.csv'
}

modelos = {
    "SO2": 'SO2_model.pkl',
    "CO": 'SO2_model.pkl',
    "O3": 'SO2_model.pkl'
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
estaciones_codificadas = {"ELX - AGROALIMENTARI": 0, "ORIHUELA": 1, "TORREVIEJA": 2}
nom_estacion_codificado = estaciones_codificadas[nom_estacion]

# Cargar el archivo CSV desde Google Cloud Storage
csv_blob_name = archivos_csv[nom_estacion_codificado]

try:
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(csv_blob_name)
    csv_content = blob.download_as_text()
    data = pd.read_csv(StringIO(csv_content), sep=';', decimal=',')
    st.write("### Datos de la estación seleccionada:")
    st.dataframe(data.head(10))
except Exception as e:
    st.error(f"Error al cargar los datos del CSV: {e}")

# Descargar el modelo desde Google Cloud Storage
model_blob_name = modelos[gas_seleccionado]

try:
    blob = bucket.blob(model_blob_name)
    blob.download_to_filename("model.pkl")
    with open("model.pkl", 'rb') as file:
        modelo = pickle.load(file)
    st.write("Modelo cargado correctamente.")
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
    try:
        # Realizar la predicción
        prediccion = modelo.predict(X_input)[0]
        st.success(f"El valor predicho para {gas_seleccionado} es: {prediccion:.2f}")
        st.balloons()
    except Exception as e:
        st.error(f"Error al realizar la predicción: {e}")

# Pie de página
st.markdown("---")
st.markdown("**Desarrollado por [Isaac Abarca | Javi Gomez | Troy Barker]** • [GitHub](https://github.com/Isaac916/ProyectoContaminaci-n) • © 2025")
