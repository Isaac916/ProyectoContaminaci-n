import os
import streamlit as st
import pickle
import pandas as pd

# Obtener la ruta del directorio actual del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir las rutas relativas de los archivos
ruta_orihuela = os.path.join(BASE_DIR, '../Procesamiento/Orihuela-Limpio.csv')
ruta_modelo = os.path.join(BASE_DIR, '../MachineLearning/SO2_model.pkl')

# Leer los datos
dataElche = pd.read_csv(ruta_orihuela, sep=';', decimal=',')
st.write(dataElche.head(10))

# Cargar el modelo desde el archivo pickle
with open(ruta_modelo, 'rb') as file:
    modelo = pickle.load(file)

# Título de la aplicación
st.title("Predicción de O3")

# Input del usuario
st.header("Introduce los parámetros necesarios")

# Inputs para los parámetros
año = st.number_input("Año", min_value=2000, max_value=2100, step=1, value=2023)
mes = st.number_input("Mes", min_value=1, max_value=12, step=1, value=1)
dia = st.number_input("Día", min_value=1, max_value=31, step=1, value=1)
hora = st.number_input("Hora", min_value=0, max_value=23, step=1, value=12)
nom_estacion = st.selectbox("Nombre de la estación", ["ELX - AGROALIMENTARI", "ORIHUELA", "TORREVIEJA"])

# Convertir la estación a códigos (igual que en el entrenamiento)
estaciones_codificadas = {"ELX - AGROALIMENTARI": 0, "ORIHUELA": 1, "TORREVIEJA": 2}
nom_estacion_codificado = estaciones_codificadas[nom_estacion]

# Crear el DataFrame para la predicción
X_input = pd.DataFrame({
    "año": [año],
    "mes": [mes],
    "dia": [dia],
    "HORA": [hora],
    "NOM_ESTACION": [nom_estacion_codificado]
})

# Mostrar el input en pantalla (opcional)
st.write("Datos ingresados para la predicción:")
st.dataframe(X_input)

# Botón para realizar la predicción
if st.button("Predecir"):
    # Realizar la predicción
    prediccion = modelo.predict(X_input)[0]
    st.subheader("Resultado de la predicción")
    st.write(f"El valor predicho para O3 es: {prediccion}")
