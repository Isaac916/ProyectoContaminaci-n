import pandas as pd
import streamlit as st
import plotly.express as px

dataElche = pd.read_csv("Data/Elche-Limpio.csv", decimal=",", sep=";")
dataOrihuela = pd.read_csv("Data/Orihuela-Limpio.csv", decimal=",", sep=";")
dataTorrevieja = pd.read_csv("Data/Torrevieja-Limpio.csv", decimal=",", sep=";")


st.set_page_config(page_title="Proyecto Contaminación", page_icon=":mask:", layout="wide")
st.markdown("## Datos generales sobre la contaminación en las siguientes estaciones de la provincia de Alicante: Elche, Orihuela y Torrevieja.")
st.sidebar.image("Assets/Contaminacion.png")

if "mostrar_leyenda" not in st.session_state:
    st.session_state.mostrar_leyenda = False

if st.button("¿Qué es cada variable?"):
    st.session_state.mostrar_leyenda = not st.session_state.mostrar_leyenda

if st.session_state.mostrar_leyenda:
    st.markdown("**Leyenda de las variables:**")
    st.table([
        ["NOx", "Óxidos de nitrógeno, compuestos que incluyen NO (óxido nítrico) y NO2 (dióxido de nitrógeno)."],
        ["CO", "Monóxido de carbono, gas producido por la combustión incompleta de carbono."],
        ["SO2", "Dióxido de azufre, gas emitido principalmente por la quema de combustibles fósiles."],
        ["NO", "Óxido nítrico, un componente principal de los NOx."],
        ["NO2", "Dióxido de nitrógeno, otro componente de los NOx."],
        ["O3", "Ozono, gas presente en la atmósfera que puede ser tanto beneficioso (en la estratósfera) como dañino (en la troposfera)."],
        ["PM10", "Partículas en suspensión con un diámetro menor a 10 micrómetros, causantes de problemas respiratorios."],
        ["PM2.5", "Partículas en suspensión con un diámetro menor a 2.5 micrómetros, más finas que las PM10, con mayor riesgo para la salud."],
        ["PM1", "Partículas en suspensión de tamaño aún más pequeño (menos de 1 micrómetro)."],
        ["NH3", "Amoníaco, gas que puede contribuir a la formación de partículas en el aire."],
        ["C6H6", "Benceno, un compuesto químico volátil y cancerígeno."],
        ["C7H8", "Tolueno, compuesto químico utilizado en solventes y pinturas."],
        ["C8H10", "Xileno, compuesto químico usado en la industria de la pintura."],
        ["Direc.", "Dirección del viento, expresada en grados."],
        ["H.Rel.", "Humedad relativa, porcentaje de la cantidad máxima de vapor de agua que el aire puede contener."],
        ["Precip.", "Precipitación, cantidad de lluvia o nieve caída en un período de tiempo."],
        ["Pres.", "Presión atmosférica, la fuerza por unidad de área que ejerce el aire sobre la superficie terrestre."],
        ["R.Sol.", "Radiación solar, cantidad de energía recibida del sol en un área dada."],
        ["Ruido", "Nivel de ruido ambiental medido en decibelios."],
        ["Temp.", "Temperatura del aire, medida en grados Celsius."],
        ["UV-B", "Radiación ultravioleta tipo B, perjudicial para la salud humana en grandes cantidades."],
        ["Veloc.", "Velocidad del viento."],
        ["Veloc.max.", "Velocidad máxima del viento registrada."],
        ["As", "Arsénico, metal pesado tóxico."],
        ["BaA", "Benceno-antraceno, compuestos tóxicos derivados de la combustión."],
        ["BaP", "Benzo(a)pireno, compuesto cancerígeno derivado de la quema de combustibles."],
        ["BbFA", "Bifenilos poliacilados, compuestos químicos contaminantes."],
        ["BjFA", "Bifenilos bifenilos, otro tipo de compuestos contaminantes."],
        ["BkFA", "Bifenilos naftilados, similares a los anteriores."],
        ["Cd", "Cadmio, metal pesado tóxico."],
        ["DahA", "Dibenzo(a,h)antraceno, compuesto tóxico derivado de la combustión."],
        ["FA", "Fluoruros, compuestos químicos que pueden afectar la salud en grandes cantidades."],
        ["HMN", "Metales pesados como el mercurio."],
        ["H2S", "Sulfuro de hidrógeno, gas tóxico y maloliente."],
        ["IcdP", "Indeno(1,2,3-cd)pireno, compuesto tóxico generado por la combustión."],
        ["Ni", "Níquel, metal pesado."],
        ["Pb", "Plomo, metal pesado altamente tóxico."],
        ["PST", "Partículas suspendidas totales, combinación de PM10, PM2.5 y PM1."]
    ])


opciones_unicas = pd.concat(
    [dataElche["NOM_ESTACION"], dataOrihuela["NOM_ESTACION"], dataTorrevieja["NOM_ESTACION"]]
).drop_duplicates()

st.sidebar.header("Filtra los datos que necesites consultar.")
nom_estacion = st.sidebar.selectbox("Nombre de la estación", opciones_unicas)

st.sidebar.markdown("---")

rango_nox = st.sidebar.slider(
    "Rango de NOx",
    min_value=1,
    max_value=200,
    value=(3, 6),
    step=1
)

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
        st.write(data_filtrado.head(10)) 
        break

st.markdown("## Visualización de datos")

tipo_grafico = st.selectbox(
    "Selecciona el tipo de gráfico", 
    ["Línea (CO)", "Barras (SO₂)", "Histograma (NOx)"]
)

data_combinada = pd.concat([dataElche, dataOrihuela, dataTorrevieja])

data_filtrada_grafico = data_combinada[data_combinada["NOM_ESTACION"] == nom_estacion]

if data_filtrada_grafico.empty:
    st.warning(f"No hay datos disponibles para la estación {nom_estacion}.")
else:
    if tipo_grafico == "Línea (CO)":
        fig = px.line(
            data_filtrada_grafico,
            x="HORA",
            y="CO",
            title=f"Concentración de CO a lo largo del día en {nom_estacion}",
            labels={"CO": "Concentración de CO (mg/m³)", "HORA": "Hora del día"},
            line_shape="spline",
        )
    elif tipo_grafico == "Barras (SO₂)":
        fig = px.bar(
            data_filtrada_grafico,
            x="HORA",
            y="SO2",
            title=f"Concentración de SO₂ a lo largo del día en {nom_estacion}",
            labels={"SO2": "Concentración de SO₂ (µg/m³)", "HORA": "Hora del día"},
            text="SO2"
        )
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    elif tipo_grafico == "Histograma (NOx)":
        fig = px.histogram(
            data_filtrada_grafico,
            x="NOx",
            title=f"Distribución de NOx en {nom_estacion}",
            labels={"NOx": "Concentración de NOx (µg/m³)"},
            nbins=20
        )

    fig.update_layout(
        xaxis_title="Hora del día" if tipo_grafico != "Histograma (NOx)" else "Concentración de NOx (µg/m³)",
        yaxis_title="Concentración" if tipo_grafico != "Histograma (NOx)" else "Frecuencia",
        title_x=0.5,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
