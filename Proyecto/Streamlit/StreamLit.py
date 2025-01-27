import os
import streamlit as st
import pickle
import pandas as pd

# Obtener la ruta del directorio actual del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir las rutas relativas de los archivos
archivos_csv = {
    0: os.path.join(BASE_DIR, '../Procesamiento/Elche-Limpio.csv'),
    1: os.path.join(BASE_DIR, '../Procesamiento/Orihuela-Limpio.csv'),
    2: os.path.join(BASE_DIR, '../Procesamiento/Torrevieja-Limpio.csv')
}

modelos = {
    "SO2": os.path.join(BASE_DIR, '../MachineLearning/SO2_model.pkl'),
    "CO": os.path.join(BASE_DIR, '../MachineLearning/CO_model.pkl'),
    "O3": os.path.join(BASE_DIR, '../MachineLearning/O3_model.pkl')
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

# Cargar el modelo del gas seleccionado
modelo_path = modelos[gas_seleccionado]
with open(modelo_path, 'rb') as file:
    modelo = pickle.load(file)

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
    # Realizar la predicción
    prediccion = modelo.predict(X_input)[0]
    st.success(f"El valor predicho para {gas_seleccionado} es: {prediccion:.2f}")
    st.balloons()

# Pie de página
st.markdown("---")
st.markdown("**Desarrollado por [Isaac Abarca | Javi Gomez | Troy Barker]** • [GitHub](https://github.com/Isaac916/ProyectoContaminaci-n) • © 2025")
