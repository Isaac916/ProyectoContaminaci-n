import pandas as pd
import streamlit as st

dataElche = pd.read_csv(
    "C:/Users/javie/Documents/ProyectoIABD25/ProyectoContaminaci-n/Proyecto/Procesamiento/Elche-Limpio.csv",
    decimal=",", sep=";"
)
dataOrihuela = pd.read_csv(
    "C:/Users/javie/Documents/ProyectoIABD25/ProyectoContaminaci-n/Proyecto/Procesamiento/Orihuela-Limpio.csv",
    decimal=",", sep=";"
)
dataTorrevieja = pd.read_csv(
    "C:/Users/javie/Documents/ProyectoIABD25/ProyectoContaminaci-n/Proyecto/Procesamiento/Torrevieja-Limpio.csv",
    decimal=",", sep=";"
)

st.set_page_config(page_title="Proyecto Contaminación", page_icon=":mask:", layout="wide")
st.subheader("Datos de la contaminación")
st.markdown("##")
st.sidebar.image("C:/Users/javie/Documents/ProyectoIABD25/ProyectoContaminaci-n/Proyecto/Assets/Contaminacion.png")

opciones_unicas = pd.concat(
    [dataElche["NOM_ESTACION"], dataOrihuela["NOM_ESTACION"], dataTorrevieja["NOM_ESTACION"]]
).drop_duplicates()

# Filtros en la barra lateral
st.sidebar.header("Filtra los datos que necesites consultar.")
nom_estacion = st.sidebar.selectbox("Nombre de la estación", opciones_unicas)

st.sidebar.markdown("---")

# Slider para rango de NOx
rango_nox = st.sidebar.slider(
    "Rango de NOx",
    min_value=1,
    max_value=200,
    value=(3, 6),
    step=1
)

# Slider para rango horario
rango_horas = st.sidebar.slider(
    "Rango horario",
    min_value=1, 
    max_value=24,
    value=(3, 6),
    step=1
)

conjuntoDeDatos = [dataElche, dataOrihuela, dataTorrevieja]

for data in conjuntoDeDatos:
    if nom_estacion in data["NOM_ESTACION"].values:
        data_filtrado = data[
            (data["NOM_ESTACION"] == nom_estacion) & 
            (data["NOx"] >= rango_nox[0]) & 
            (data["NOx"] <= rango_nox[1]) & 
            (data["HORA"] >= rango_horas[0]) & 
            (data["HORA"] <= rango_horas[1])
        ]
        
        st.write(f"Datos filtrados para {nom_estacion}:")
        st.write(f"- NOx entre {rango_nox[0]} y {rango_nox[1]}")
        st.write(f"- Hora entre {rango_horas[0]} y {rango_horas[1]}")
        st.write(data_filtrado.head(10)) 
        break
