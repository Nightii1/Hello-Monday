import streamlit as st
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Terzaghi Foundation Design",
    page_icon="🏗️",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.main {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
}
h1 {
    color: #2c3e50;
    text-align: center;
}
.metric-box {
    background-color: #ecf0f1;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown("<h1>🏗️ Terzaghi Bearing Capacity Calculator</h1>", unsafe_allow_html=True)

# -----------------------------
# INPUT SECTION
# -----------------------------
st.subheader("📥 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    c = st.number_input("Cohesion, c (kPa)", value=0.0)
    gamma = st.number_input("Unit weight, γ (kN/m³)", value=18.0)
    phi = st.number_input("Friction angle, φ (degree)", value=30.0)

with col2:
    B = st.number_input("Width of footing, B (m)", value=2.0)
    Df = st.number_input("Depth of foundation, Df (m)", value=1.0)
    FS = st.number_input("Factor of Safety", value=3.0)

# -----------------------------
# CALCULATION
# -----------------------------
def bearing_capacity_factors(phi):
    phi_rad = np.radians(phi)

    Nq = np.exp(np.pi * np.tan(phi_rad)) * (np.tan(np.radians(45 + phi/2)))**2

    if phi == 0:
        Nc = 5.7
        Ngamma = 0
    else:
        Nc = (Nq - 1) / np.tan(phi_rad)
        Ngamma = 2 * (Nq + 1) * np.tan(phi_rad)

    return Nc, Nq, Ngamma

if st.button("🚀 Calculate"):

    Nc, Nq, Ngamma = bearing_capacity_factors(phi)

    qult = c * Nc + gamma * Df * Nq + 0.5 * gamma * B * Ngamma
    qallow = qult / FS

    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Nc", f"{Nc:.2f}")
        st.metric("Nq", f"{Nq:.2f}")

    with col2:
        st.metric("Nγ", f"{Ngamma:.2f}")
        st.metric("qult (kPa)", f"{qult:.2f}")

    with col3:
        st.metric("qallow (kPa)", f"{qallow:.2f}")

    # -----------------------------
    # DESIGN STATUS
    # -----------------------------
    st.subheader("🧠 Interpretation")

    if qallow < 100:
        st.error("⚠️ Bearing capacity ต่ำ อาจต้องปรับขนาดฐานราก")
    elif qallow < 300:
        st.warning("⚠️ อยู่ในช่วงใช้งานได้ แต่ควรตรวจสอบเพิ่มเติม")
    else:
        st.success("✅ ปลอดภัย สามารถใช้งานได้")
