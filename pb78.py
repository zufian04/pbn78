import streamlit as st
from scipy.optimize import linprog

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Optimización Imprenta",
    page_icon="📄",
    layout="wide"
)

# ---------------- ESTILO ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);
        color: white;
    }

    html, body, [class*="css"] {
        color: white !important;
    }

    h1, h2, h3, p, div {
        color: white !important;
    }

    .stButton>button {
        background-color: #38bdf8;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }

    .card {
        background-color: rgba(30, 41, 59, 0.85);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- TÍTULO ----------------
st.title("📄 Optimización de Producción - Imprenta")

st.markdown("### 🎯 Modelo con variación de costos ±50%")

# ---------------- COSTOS BASE ----------------
costo_f_base = 15
costo_a_base = 40
gan_f_base = 25
gan_a_base = 50

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Parámetros")

# Hojas
hojas_folleto = st.sidebar.number_input("Hojas por folleto", 1, value=4)
hojas_afiche = st.sidebar.number_input("Hojas por afiche", 1, value=6)

# 🔥 COSTOS con ±50%
costo_folleto = st.sidebar.slider(
    "Costo folleto (±50%)",
    min_value=float(costo_f_base * 0.5),
    max_value=float(costo_f_base * 1.5),
    value=float(costo_f_base)
)

costo_afiche = st.sidebar.slider(
    "Costo afiche (±50%)",
    min_value=float(costo_a_base * 0.5),
    max_value=float(costo_a_base * 1.5),
    value=float(costo_a_base)
)

# 🔥 GANANCIAS con ±50%
ganancia_folleto = st.sidebar.slider(
    "Ganancia folleto (±50%)",
    min_value=float(gan_f_base * 0.5),
    max_value=float(gan_f_base * 1.5),
    value=float(gan_f_base)
)

ganancia_afiche = st.sidebar.slider(
    "Ganancia afiche (±50%)",
    min_value=float(gan_a_base * 0.5),
    max_value=float(gan_a_base * 1.5),
    value=float(gan_a_base)
)

# Restricciones
max_impresos = st.sidebar.number_input("Máx impresos", 1, value=90)
min_hojas = st.sidebar.number_input("Mín hojas", 1, value=391)
presupuesto = st.sidebar.number_input("Presupuesto", 1, value=2000)

# Límites de producción
st.sidebar.subheader("📌 Límites")

min_folletos = st.sidebar.number_input("Mín folletos", 0, value=5)
max_folletos = st.sidebar.number_input("Máx folletos", 1, value=60)

min_afiches = st.sidebar.number_input("Mín afiches", 0, value=0)
max_afiches = st.sidebar.number_input("Máx afiches", 1, value=80)

# ---------------- BOTÓN ----------------
if st.button("🚀 Calcular solución óptima"):

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

    bounds = [
        (min_folletos, max_folletos),
        (min_afiches, max_afiches)
    ]

    resultado = linprog(
        c,
        A_ub=A,
        b_ub=b,
        bounds=bounds,
        method="highs"
    )

    if resultado.success:

        x = round(resultado.x[0])
        y = round(resultado.x[1])

        st.success("✅ Solución encontrada")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Folletos", x)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Afiches", y)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Ganancia", f"${-resultado.fun:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("❌ No hay solución con estos parámetros")
