import streamlit as st
from scipy.optimize import linprog

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Optimización Imprenta",
    page_icon="📄",
    layout="wide"
)

# ---------------- CSS PERSONALIZADO ----------------
st.markdown("""
    <style>
        .main {
            background-color: #0f172a;
            color: white;
        }

        h1 {
            color: #38bdf8;
            text-align: center;
        }

        .stButton>button {
            background-color: #38bdf8;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }

        .card {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 10px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("📄 Optimización de Producción - Imprenta")
st.markdown("### 📊 Maximiza la ganancia de folletos y afiches")
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Parámetros")

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
        ganancia = -resultado.fun

        st.success("✅ Solución encontrada")

        # ---------------- RESULTADOS VISUALES ----------------
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

        # ---------------- DETALLES ----------------
        st.subheader("📊 Verificación del modelo")

        st.info(f"📦 Total impresos: {folletos + afiches}")
        st.info(f"📄 Hojas utilizadas: {hojas_folleto * folletos + hojas_afiche * afiches}")
        st.info(f"💸 Costo total: ${costo_folleto * folletos + costo_afiche * afiches:,.0f}")

    else:
        st.error("❌ No se encontró solución factible")
