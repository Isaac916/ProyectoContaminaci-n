import pandas as pd 
import streamlit as st 

dataElche = pd.read_csv("C:/Users/javgomdav/Desktop/Prueba_proyecto/ESTACIONES_COMBINADAS_NO_LIMPIO/Elche-LIMPIO.csv", decimal=",", sep=";")

st.write(dataElche.head(10))