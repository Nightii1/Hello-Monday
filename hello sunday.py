import streamlit as st
import math

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Bearing Capacity", layout="centered")

# ---------------------- CSS ----------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f1f3f6;
}

/* Title */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: #0b3c5d;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 15px;
    color: #333333;
    margin-bottom: 20px;
}

/* Card */
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #dcdcdc;
    margin-bottom: 20px;
}

/* Section title */
.section {
    font-size: 18px;
    font-weight: 600;
    color: #0b3c5d;
    margin-bottom: 10px;
}

/* Labels */
label {
    color: #111 !important;
    font-weight: 500;
}

/* Result */
.result {
    font-size: 22px;
    font-weight: bold;
    color: #1a7f37;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    height: 45px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 15px;
}

/* Input fields */
input {
    color: black !important;
}

/* Divider */
hr {
    border: 1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)

# ---------------------- TITLE ----------------------
st.markdown('<div class="title">Bearing Capacity Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Terzaghi Method (Eccentric Footing)</div>', unsafe_allow_html=True)

# ---------------------- INPUT ----------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section">Geometry</div>', unsafe_allow_html=True)
    B = st.number_input("Width B (m)", min_value=0.0, value=2.0)
    L = st.number_input("Length L (m)", min_value=0.0, value=3.0)
    D = st.number_input("Depth D (m)", min_value=0.0, value=1.5)

    st.markdown('<div class="section">Eccentricity</div>', unsafe_allow_html=True)
    ex = st.number_input("eₓ (m)", min_value=0.0, value=0.0)
    ey = st.number_input("eᵧ (m)", min_value=0.0, value=0.0)

with col2:
    st.markdown('<div class="section">Soil Properties</div>', unsafe_allow_html=True)
    c = st.number_input("Cohesion c (kPa)", min_value=0.0, value=25.0)
    phi = st.number_input("Friction angle φ (deg)", min_value=0.0, value=30.0)
    gamma = st.number_input("Unit weight γ (kN/m³)", min_value=0.0, value=18.0)

    st.markdown('<div class="section">Safety</div>', unsafe_allow_html=True)
    FS = st.number_input("Factor of Safety", min_value=1.0, value=3.0)

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

# ---------------------- BUTTON ----------------------
colb1, colb2 = st.columns(2)

with colb1:
    calculate = st.button("🔍 Calculate")

with colb2:
    clear = st.button("🧹 Clear")

if clear:
    st.experimental_rerun()

# ---------------------- RESULT ----------------------
if calculate:

    if (B - 2*ex) <= 0 or (L - 2*ey) <= 0:
        st.error("❌ Eccentricity มากเกินไป → พื้นที่ใช้งานติดลบ")
    else:
        B_eff = B - 2*ex
        L_eff = L - 2*ey

        Nc, Nq, Ngamma = bearing_capacity_factors(phi)

        qult = c * Nc + gamma * D * Nq + 0.5 * gamma * B_eff * Ngamma
        qall = qult / FS

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<div class="section">Results</div>', unsafe_allow_html=True)

        st.write(f"Effective Width B' = {B_eff:.2f} m")
        st.write(f"Effective Length L' = {L_eff:.2f} m")

        st.markdown(f'<div class="result">q₍ult₎ = {qult:.2f} kPa</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result">q₍all₎ = {qall:.2f} kPa</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- FOOTER ----------------------
st.markdown("""
<hr>
<p style='text-align:center; color:#666; font-size:13px;'>
Civil Engineering Tool • Geotechnical Design
</p>
""", unsafe_allow_html=True)
