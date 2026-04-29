import streamlit as st
import math

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Terzaghi Bearing Capacity (Eccentric)",
    layout="centered"
)

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(to right, #eef2f7, #f8fafc);
}

/* Title */
.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #1f4e79;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 16px;
    color: #555;
    margin-bottom: 25px;
}

/* Card */
.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}

/* Result */
.result {
    font-size: 24px;
    font-weight: bold;
    color: #0a7d5e;
}

/* Button */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 16px;
    font-weight: bold;
}

/* Input box */
input {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- TITLE ----------------------
st.markdown('<div class="title">Terzaghi Bearing Capacity</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Eccentric Footing Analysis</div>', unsafe_allow_html=True)

# ---------------------- INPUT ----------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📥 Input Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📐 Geometry**")
        B = st.number_input("Width B (m)", min_value=0.0, value=2.0)
        L = st.number_input("Length L (m)", min_value=0.0, value=3.0)
        D = st.number_input("Depth D (m)", min_value=0.0, value=1.5)

    with col2:
        st.markdown("**🧱 Soil Properties**")
        c = st.number_input("Cohesion c (kPa)", min_value=0.0, value=25.0)
        phi = st.number_input("Friction angle φ (deg)", min_value=0.0, value=30.0)
        gamma = st.number_input("Unit weight γ (kN/m³)", min_value=0.0, value=18.0)

    with col3:
        st.markdown("**⚖️ Load & Safety**")
        ex = st.number_input("eₓ (m)", min_value=0.0, value=0.0)
        ey = st.number_input("eᵧ (m)", min_value=0.0, value=0.0)
        FS = st.number_input("Factor of Safety (FS)", min_value=1.0, value=3.0)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- FUNCTIONS ----------------------
def bearing_capacity_factors(phi):
    phi_rad = math.radians(phi)

    if phi == 0:
        Nc = 5.7
        Nq = 1
        Ngamma = 0
    else:
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45 + phi/2)))**2
        Nc = (Nq - 1) / math.tan(phi_rad)
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)

    return Nc, Nq, Ngamma

# ---------------------- BUTTONS ----------------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    calculate = st.button("🔍 Calculate")

with col_btn2:
    clear = st.button("🧹 Clear")

# ---------------------- CLEAR ----------------------
if clear:
    st.experimental_rerun()

# ---------------------- CALCULATION ----------------------
if calculate:

    if (B - 2*ex) <= 0 or (L - 2*ey) <= 0:
        st.error("❌ ค่า eccentricity มากเกินไป ทำให้พื้นที่ใช้งานติดลบ")
    else:
        B_eff = B - 2*ex
        L_eff = L - 2*ey

        Nc, Nq, Ngamma = bearing_capacity_factors(phi)

        qult = c * Nc + gamma * D * Nq + 0.5 * gamma * B_eff * Ngamma
        qall = qult / FS

        # ---------------------- OUTPUT ----------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📊 Results")

        st.write(f"Effective Width B' = {B_eff:.2f} m")
        st.write(f"Effective Length L' = {L_eff:.2f} m")

        st.markdown(f'<div class="result">q₍ult₎ = {qult:.2f} kPa</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result">q₍all₎ = {qall:.2f} kPa</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- FOOTER ----------------------
st.markdown("""
<hr>
<p style='text-align:center; color:gray; font-size:14px;'>
Developed for Civil Engineering • Geotechnical Analysis Tool
</p>
""", unsafe_allow_html=True)
