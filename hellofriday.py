import streamlit as st
import math

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Pavement Design", layout="wide")
st.title("🛣️ Pavement Design (AASHTO 1993)")

# ==============================
# SESSION
# ==============================
if "SN" not in st.session_state:
    st.session_state.SN = None

# ==============================
# INPUT
# ==============================
st.header("📊 Flexible Pavement (SN)")

col1, col2 = st.columns(2)

ZR_map = {
    50: 0.000, 60: -0.253, 70: -0.524, 75: -0.674,
    80: -0.841, 85: -1.037, 90: -1.282,
    95: -1.645, 99: -2.327, 99.9: -3.090
}

with col1:
    W18 = st.number_input("ESAL (W18)", 1000.0, 1e8, 5e6)
    reliability = st.selectbox("Reliability (%)", list(ZR_map.keys()), index=6)
    ZR = ZR_map[reliability]
    S0 = st.number_input("S₀", 0.30, 0.50, 0.45)

with col2:
    MR = st.number_input("M_R (psi)", 1000, 50000, 7500)
    pi = st.number_input("p_i", 3.0, 5.0, 4.2)
    pt = st.number_input("p_t", 1.5, 3.0, 2.5)

dpsi = pi - pt

# ==============================
# SN FUNCTION
# ==============================
def f_SN(SN):
    return (
        ZR*S0
        + 9.36*math.log10(SN+1) - 0.20
        + math.log10(max(dpsi,0.01)) / (0.40 + 1094/((SN+1)**5.19))
        + 2.32*math.log10(MR) - 8.07
        - math.log10(W18)
    )

def solve_SN():
    SN = 3
    for _ in range(100):
        f = f_SN(SN)
        df = (f_SN(SN+0.001) - f)/0.001
        if abs(df) < 1e-6:
            break
        SN_new = SN - f/df
        if abs(SN_new - SN) < 1e-4:
            return SN_new
        SN = max(SN_new, 0.1)
    return SN

# ==============================
# CALCULATE SN
# ==============================
if st.button("🔢 Calculate SN"):
    st.session_state.SN = solve_SN()

if st.session_state.SN is not None:
    SN = st.session_state.SN
    st.success(f"SN = {SN:.2f}")

# ==============================
# LAYER DESIGN
# ==============================
st.markdown("---")
st.header("🧱 Pavement Layer Design")

if st.session_state.SN is not None:

    SN = st.session_state.SN

    colA, colB, colC = st.columns(3)

    with colA:
        a1 = st.number_input("a1 (Asphalt)", 0.30, 0.50, 0.44)
        D1 = st.number_input("Asphalt Thickness (inch)", 1.0, 10.0, 3.0)

    with colB:
        a2 = st.number_input("a2 (Base)", 0.10, 0.30, 0.14)
        m2 = st.number_input("m2", 0.5, 1.5, 1.0)

    with colC:
        a3 = st.number_input("a3 (Subbase)", 0.05, 0.20, 0.11)
        m3 = st.number_input("m3", 0.5, 1.5, 1.0)

    # ==============================
    # CALC
    # ==============================
    SN1 = a1 * D1
    D2 = max((SN - SN1)/(a2*m2), 0)
    SN2 = a2 * m2 * D2
    D3 = max((SN - (SN1 + SN2))/(a3*m3), 0)

    st.subheader("📊 Result")
    st.write(f"SN Required = {SN:.2f}")
    st.write(f"Asphalt = {D1:.2f} in")
    st.write(f"Base = {D2:.2f} in")
    st.write(f"Subbase = {D3:.2f} in")

    # ==============================
    # SECTION (FIXED)
    # ==============================
    st.subheader("🧱 Pavement Section")

    total = D1 + D2 + D3
    if total == 0:
        total = 1

    scale = 300 / total

    h1 = D1 * scale
    h2 = D2 * scale
    h3 = D3 * scale

    html = f"""
    <div style="width:250px;margin:auto;text-align:center;">

        <div style="height:{h1}px;background:#222;border:2px solid black;color:white;
        display:flex;align-items:center;justify-content:center;">
        Asphalt {D1:.1f} in</div>

        <div style="height:{h2}px;background:#c2b280;border:2px solid black;
        display:flex;align-items:center;justify-content:center;">
        Base {D2:.1f} in</div>

        <div style="height:{h3}px;background:#8fbc8f;border:2px solid black;
        display:flex;align-items:center;justify-content:center;">
        Subbase {D3:.1f} in</div>

        <div style="height:50px;background:#d3d3d3;border:2px solid black;
        display:flex;align-items:center;justify-content:center;">
        Subgrade</div>

    </div>
    """

    # 🔥 สำคัญที่สุด
    st.markdown(html, unsafe_allow_html=True)
