import streamlit as st
import math
import matplotlib.pyplot as plt

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="AASHTO 1993 Pavement Design",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ Pavement Design (AASHTO 1993)")

# ==============================
# FLEXIBLE PAVEMENT (SN)
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
    mode = st.radio("M_R input", ["Direct (psi)", "From CBR"])
    if mode == "Direct (psi)":
        MR = st.number_input("M_R (psi)", 1000, 50000, 7500)
    else:
        CBR = st.number_input("CBR (%)", 1.0, 100.0, 5.0)
        MR = 1500 * CBR
        st.write(f"M_R = {MR:.0f} psi")

    pi = st.number_input("p_i", 3.0, 5.0, 4.2)
    pt = st.number_input("p_t", 1.5, 3.0, 2.5)
    dpsi = pi - pt

# ==============================
# SN SOLVER
# ==============================
def f_SN(SN):
    try:
        return (
            ZR*S0
            + 9.36*math.log10(SN+1) - 0.20
            + math.log10(max(dpsi,0.01)) / (0.40 + 1094/((SN+1)**5.19))
            + 2.32*math.log10(MR) - 8.07
            - math.log10(W18)
        )
    except:
        return 999

def solve_SN():
    SN = 3
    for _ in range(100):
        f = f_SN(SN)
        df = (f_SN(SN+0.001) - f) / 0.001
        if abs(df) < 1e-6:
            break
        SN_new = SN - f/df
        if abs(SN_new - SN) < 1e-4:
            return SN_new
        SN = max(SN_new, 0.1)
    return SN

# ==============================
# BUTTON SN
# ==============================
SN = None

if st.button("🔢 Calculate SN"):
    SN = solve_SN()
    st.success(f"SN = {SN:.2f}")

# ==============================
# LAYER DESIGN
# ==============================
st.markdown("---")
st.header("🧱 Pavement Layer Design")

if SN:

    l1, l2, l3 = st.columns(3)

    with l1:
        a1 = st.number_input("a1 (Asphalt)", 0.30, 0.50, 0.44)
        D1 = st.number_input("Asphalt Thickness (inch)", 1.0, 10.0, 3.0)

    with l2:
        a2 = st.number_input("a2 (Base)", 0.10, 0.30, 0.14)
        m2 = st.number_input("m2", 0.5, 1.5, 1.0)

    with l3:
        a3 = st.number_input("a3 (Subbase)", 0.05, 0.20, 0.11)
        m3 = st.number_input("m3", 0.5, 1.5, 1.0)

    if st.button("📐 Calculate Layers"):

        SN1 = a1 * D1

        SN2_req = max(SN - SN1, 0)
        D2 = SN2_req / (a2 * m2)

        SN2 = a2 * m2 * D2

        SN3_req = max(SN - (SN1 + SN2), 0)
        D3 = SN3_req / (a3 * m3) if SN3_req > 0 else 0

        st.subheader("📊 Result")

        st.write(f"SN Required = {SN:.2f}")
        st.write(f"Asphalt = {D1:.2f} in")
        st.write(f"Base = {D2:.2f} in")
        st.write(f"Subbase = {D3:.2f} in")

        # ==============================
        # DRAW GRAPH
        # ==============================
        st.subheader("🧱 Pavement Section")

        layers = [
            ("Asphalt", D1, "#333333"),
            ("Base", D2, "#c2b280"),
            ("Subbase", D3, "#8fbc8f"),
        ]

        fig, ax = plt.subplots(figsize=(4,6))
        current_height = 0

        for name, thickness, color in layers:
            if thickness > 0:
                ax.bar(0, thickness, bottom=current_height, color=color, edgecolor="black")
                ax.text(0, current_height + thickness/2,
                        f"{name}\n{thickness:.1f} in",
                        ha='center', va='center', color='white')
                current_height += thickness

        ax.bar(0, 2, bottom=current_height, color="#d3d3d3", edgecolor="black")
        ax.text(0, current_height + 1, "Subgrade", ha='center')

        ax.set_xticks([])
        ax.set_ylabel("Thickness (inch)")

        st.pyplot(fig)

# ==============================
# RIGID
# ==============================
st.markdown("---")
st.header("🧱 Rigid Pavement")

c1, c2 = st.columns(2)

with c1:
    W18_r = st.number_input("ESAL (Rigid)", 1000.0, 1e8, 5e6)
    R = st.selectbox("Reliability (Rigid)", list(ZR_map.keys()), index=6)
    ZR_r = ZR_map[R]
    S0_r = st.number_input("S₀ (Rigid)", 0.30, 0.50, 0.35)

with c2:
    k = st.number_input("k (pci)", 50, 500, 150)
    Sc = st.number_input("S'c (psi)", 400, 1000, 650)
    Cd = st.number_input("Cd", 0.7, 1.25, 1.0)

def f_D(D):
    try:
        return (
            ZR_r*S0_r
            + 7.35*math.log10(D+1) - 0.06
            + (math.log10(Sc)*Cd)/(1+(1.624e7/((D+1)**8.46)))
            + 4.22*math.log10(k) - 8.07
            - math.log10(W18_r)
        )
    except:
        return 999

def solve_D():
    D = 8
    for _ in range(100):
        f = f_D(D)
        df = (f_D(D+0.01) - f)/0.01
        if abs(df) < 1e-6:
            break
        D_new = D - f/df
        if abs(D_new - D) < 0.001:
            return D_new
        D = max(D_new, 4)
    return D

if st.button("🔢 Calculate Rigid"):
    D = solve_D()
    st.success(f"Thickness = {D:.2f} inch")
    st.info(f"Recommended = {math.ceil(D)} inch")
