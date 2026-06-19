import streamlit as st
from scipy.optimize import linprog

# Configuración de página

st.set_page_config(
page_title="Optimización de Producción",
page_icon="📈",
layout="wide"
)

# Encabezado

st.title("📈 Optimización de Producción - Imprenta")
st.markdown("---")

st.write("""
Esta aplicación permite determinar la cantidad óptima de **folletos** y **afiches**
para maximizar la ganancia respetando las restricciones de producción.
""")

# Sidebar

st.sidebar.header("⚙️ Parámetros")

hojas_folleto = st.sidebar.number_input(
"Hojas por folleto",
min_value=1,
value=4
)

hojas_afiche = st.sidebar.number_input(
"Hojas por afiche",
min_value=1,
value=6
)

costo_folleto = st.sidebar.number_input(
"Costo por folleto ($)",
min_value=1,
value=15
)

costo_afiche = st.sidebar.number_input(
"Costo por afiche ($)",
min_value=1,
value=40
)

ganancia_folleto = st.sidebar.number_input(
"Ganancia por folleto ($)",
min_value=1,
value=25
)

ganancia_afiche = st.sidebar.number_input(
"Ganancia por afiche ($)",
min_value=1,
value=50
)

max_impresos = st.sidebar.number_input(
"Máximo de impresos",
min_value=1,
value=90
)

min_hojas = st.sidebar.number_input(
"Mínimo de hojas utilizadas",
min_value=1,
value=391
)

presupuesto = st.sidebar.number_input(
"Presupuesto máximo ($)",
min_value=1,
value=2000
)

st.markdown("### 📋 Restricciones actuales")

col1, col2, col3 = st.columns(3)

with col1:
st.info(f"Impresos ≤ {max_impresos}")

with col2:
st.info(f"Hojas ≥ {min_hojas}")

with col3:
st.info(f"Costo ≤ ${presupuesto}")

# Botón principal

if st.button("🚀 Calcular Solución Óptima", use_container_width=True):

```
c = [-ganancia_folleto, -ganancia_afiche]

A = [
    [1, 1],
    [costo_folleto, costo_afiche],
    [-hojas_folleto, -hojas_afiche]
]

b = [
    max_impresos,
    presupuesto,
    -min_hojas
]

resultado = linprog(
    c,
    A_ub=A,
    b_ub=b,
    bounds=[(0, None), (0, None)],
    method="highs"
)

if resultado.success:

    folletos = round(resultado.x[0])
    afiches = round(resultado.x[1])

    st.success("✅ Solución encontrada")

    c1, c2, c3 = st.columns(3)

    c1.metric("📚 Folletos", folletos)
    c2.metric("🖼️ Afiches", afiches)
    c3.metric(
        "💰 Ganancia Máxima",
        f"${-resultado.fun:,.2f}"
    )

    st.markdown("### 📊 Verificación")

    st.write(
        f"**Impresos Totales:** {folletos + afiches}"
    )

    st.write(
        f"**Hojas Utilizadas:** {hojas_folleto*folletos + hojas_afiche*afiches}"
    )

    st.write(
        f"**Costo Total:** ${costo_folleto*folletos + costo_afiche*afiches:,.0f}"
    )

else:
    st.error(
        "❌ No existe una solución factible para los parámetros seleccionados."
    )
```
