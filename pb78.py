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
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);
        color: white;
    }

    /* Texto general en blanco */
    html, body, [class*="css"] {
        color: white !important;
    }

    h1, h2, h3, p, div {
        color: white !important;
    }

    /* Títulos */
    h1, h2, h3 {
        text-align: center;
        color: #ffffff;
    }

    /* Botón */
    .stButton>button {
        background-color: #38bdf8;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #0ea5e9;
        transform: scale(1.02);
    }

    /* Tarjetas */
    .card {
        background-color: rgba(30, 41, 59, 0.85);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 12px rgba(0,0,0,0.4);
        text-align: center;
        color: white;
    }

    /* Métricas */
    .stMetric {
        background-color: rgba(15, 23, 42, 0.6);
        padding: 10px;
        border-radius: 10px;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(2, 6, 23, 0.9);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- TÍTULO ----------------
st.title("📄 Optimización de Producción - Imprenta")
st.markdown("### Maximiza la ganancia de folletos y afiches")
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Parámetros del modelo")

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
st.markdown("## 🚀 Ejecutar optimización")

if st.button("Calcular solución óptima"):

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

    # ---------------- RESULTADO ----------------
    if resultado.success:

        folletos = round(resultado.x[0])
        afiches = round(resultado.x[1])
        ganancia = -resultado.fun

        st.success("✅ Solución encontrada")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("📘 Folletos", folletos)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("🖼️ Afiches", afiches)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("💰 Ganancia", f"${ganancia:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ---------------- VERIFICACIÓN ----------------
        st.subheader("📊 Verificación del modelo")

        st.info(f"📦 Total impresos: {folletos + afiches}")
        st.info(f"📄 Hojas utilizadas: {hojas_folleto * folletos + hojas_afiche * afiches}")
        st.info(f"💸 Costo total: ${costo_folleto * folletos + costo_afiche * afiches:,.0f}")

    else:
        st.error("❌ No se encontró una solución factible")
