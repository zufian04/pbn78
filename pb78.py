import streamlit as st
from scipy.optimize import linprog

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(
    page_title="Optimización de Imprenta",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Optimización de Producción - Imprenta")
st.markdown("Determina la mejor combinación de folletos y afiches para maximizar la ganancia.")

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Parámetros del problema")

hojas_folleto = st.sidebar.number_input("Hojas por folleto", value=4, min_value=1)
hojas_afiche = st.sidebar.number_input("Hojas por afiche", value=6, min_value=1)

costo_folleto = st.sidebar.number_input("Costo por folleto ($)", value=15, min_value=1)
costo_afiche = st.sidebar.number_input("Costo por afiche ($)", value=40, min_value=1)

ganancia_folleto = st.sidebar.number_input("Ganancia por folleto ($)", value=25, min_value=1)
ganancia_afiche = st.sidebar.number_input("Ganancia por afiche ($)", value=50, min_value=1)

max_impresos = st.sidebar.number_input("Máximo de impresos", value=90, min_value=1)
min_hojas = st.sidebar.number_input("Mínimo de hojas", value=391, min_value=1)
presupuesto = st.sidebar.number_input("Presupuesto máximo ($)", value=2000, min_value=1)

# ---------------- BOTÓN ----------------
st.markdown("### 🚀 Ejecutar optimización")

if st.button("Calcular solución óptima", use_container_width=True):

    # ---------------- MODELO ----------------
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

    # ---------------- RESULTADOS ----------------
    if resultado.success:

        folletos = round(resultado.x[0])
        afiches = round(resultado.x[1])
        ganancia = -resultado.fun

        st.success("✅ Solución encontrada")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📘 Folletos", folletos)

        with col2:
            st.metric("🖼️ Afiches", afiches)

        with col3:
            st.metric("💰 Ganancia máxima", f"${ganancia:,.0f}")

        st.markdown("---")
        st.subheader("📊 Verificación del modelo")

        st.write(f"**Total de impresos:** {folletos + afiches}")
        st.write(f"**Hojas utilizadas:** {hojas_folleto * folletos + hojas_afiche * afiches}")
        st.write(f"**Costo total:** ${costo_folleto * folletos + costo_afiche * afiches:,.0f}")

    else:
        st.error("❌ No se encontró una solución factible con estos parámetros.")
