# app.py

import streamlit as st
from pulp import *

st.title("Optimización de Producción - Imprenta")

# Crear modelo
modelo = LpProblem("Imprenta", LpMaximize)

# Variables enteras
x = LpVariable("Folletos", lowBound=0, cat="Integer")
y = LpVariable("Afiches", lowBound=0, cat="Integer")

# Función objetivo
modelo += 25*x + 50*y

# Restricciones
modelo += x + y <= 90
modelo += 4*x + 6*y >= 391
modelo += 15*x + 40*y <= 2000

# Resolver
modelo.solve()

st.subheader("Resultado Óptimo")

st.metric("Folletos", int(value(x)))
st.metric("Afiches", int(value(y)))
st.metric("Ganancia Máxima", f"${value(modelo.objective):,.0f}")

st.subheader("Verificación")

st.write(f"Impresos totales: {int(value(x)+value(y))}")
st.write(f"Hojas utilizadas: {int(4*value(x)+6*value(y))}")
st.write(f"Costo total: ${int(15*value(x)+40*value(y))}")
