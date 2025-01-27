import os
import requests
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
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

# Entrenamiento del modelo
# Preprocesamiento similar al del código original
df_combined = pd.concat([
    pd.read_csv('https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Elche-Limpio.csv', sep=';'),
    pd.read_csv('https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Orihuela-Limpio.csv', sep=';'),
    pd.read_csv('https://raw.githubusercontent.com/Isaac916/ProyectoContaminaci-n/feature/procesamientoDatos/Proyecto/Procesamiento/Torrevieja-Limpio.csv', sep=';')
], ignore_index=True)

# Procesar fechas y eliminar filas nulas
df_combined['FECHA'] = pd.to_datetime(df_combined['FECHA'], errors='coerce')
df_combined['año'] = df_combined['FECHA'].dt.year
df_combined['mes'] = df_combined['FECHA'].dt.month
df_combined['dia'] = df_combined['FECHA'].dt.day
columns_to_keep = ['año', 'mes', 'dia', 'HORA', 'NOM_ESTACION', gas_seleccionado]
df_combined = df_combined[columns_to_keep]
df_combined.dropna(subset=[gas_seleccionado], inplace=True)

# Convertir columnas categóricas a números
df_combined = df_combined.apply(lambda col: col.astype('category').cat.codes if col.dtypes == 'object' else col)

# Preparar datos para entrenamiento
X = df_combined.drop([gas_seleccionado], axis=1)
y = df_combined[gas_seleccionado]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Modelos
rf_model = RandomForestClassifier()
lr_model = LogisticRegression(max_iter=1000)
rf_model.fit(X_train, y_train)
lr_model.fit(X_train, y_train)

# Evaluación
rf_predictions = rf_model.predict(X_test)
lr_predictions = lr_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_predictions)
lr_accuracy = accuracy_score(y_test, lr_predictions)

best_model = rf_model if rf_accuracy > lr_accuracy else lr_model

# Mostrar precisión
st.write(f"Precisión del modelo RandomForest: {rf_accuracy * 100:.2f}%")
st.write(f"Precisión del modelo LogisticRegression: {lr_accuracy * 100:.2f}%")

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
    prediction = best_model.predict(X_input)[0]
    st.success(f"El valor predicho para {gas_seleccionado} es: {prediction:.2f}")
    st.balloons()

# Pie de página
st.markdown("---")
st.markdown("**Desarrollado por [Isaac Abarca | Javi Gomez | Troy Barker]** • [GitHub](https://github.com/Isaac916/ProyectoContaminaci-n) • © 2025")
