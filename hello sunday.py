import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Bearing Capacity Tool", layout="wide")

# ---------------------- CSS ----------------------
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #1f4e79;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.result {
    font-size: 22px;
    font-weight: bold;
    color: #0a7d5e;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- TITLE ----------------------
st.markdown('<div class="title">Bearing Capacity (Eccentric Footing)</div>', unsafe_allow_html=True)

# ---------------------- FUNCTIONS ----------------------
def bearing_capacity_factors(phi):
    phi_rad = math.radians(phi)
    if phi == 0:
        return 5.7, 1, 0
    Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45 + phi/2)))**2
    Nc = (Nq - 1) / math.tan(phi_rad)
    Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)
    return Nc, Nq, Ngamma

def shape_factors(B, L):
    sc = 1 + 0.2*(B/L)
    sq = 1 + 0.1*(B/L)
    sg = 1 - 0.4*(B/L)
    return sc, sq, sg

def depth_factors(D, B):
    dc = 1 + 0.2*(D/B)
    dq = 1 + 0.1*(D/B)
    dg = 1
    return dc, dq, dg

def calculate_bearing(method, B, L, D, c, phi, gamma, ex, ey):
    B_eff = B - 2*ex
    if B_eff <= 0:
        return None

    Nc, Nq, Ngamma = bearing_capacity_factors(phi)

    if method == "Terzaghi":
        return c*Nc + gamma*D*Nq + 0.5*gamma*B_eff*Ngamma

    sc, sq, sg = shape_factors(B_eff, L)
    dc, dq, dg = depth_factors(D, B_eff)

    if method == "Meyerhof":
        return (
            c*Nc*sc*dc +
            gamma*D*Nq*sq*dq +
            0.5*gamma*B_eff*Ngamma*sg*dg
        )

    if method == "Hansen":
        ic = iq = ig = 1
        return (
            c*Nc*sc*dc*ic +
            gamma*D*Nq*sq*dq*iq +
            0.5*gamma*B_eff*Ngamma*sg*dg*ig
        )

# ---------------------- INPUT ----------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    B = st.number_input("Width B (m)", 0.1, 20.0, 2.0)
    L = st.number_input("Length L (m)", 0.1, 20.0, 3.0)
    D = st.number_input("Depth D (m)", 0.0, 10.0, 1.5)

with col2:
    c = st.number_input("c (kPa)", 0.0, 200.0, 25.0)
    phi = st.number_input("φ (deg)", 0.0, 50.0, 30.0)
    gamma = st.number_input("γ (kN/m³)", 0.0, 30.0, 18.0)

with col3:
    ex = st.number_input("eₓ (m)", 0.0, 5.0, 0.0)
    ey = st.number_input("eᵧ (m)", 0.0, 5.0, 0.0)
    FS = st.number_input("FS", 1.0, 10.0, 3.0)

method = st.selectbox("Method", ["Terzaghi", "Meyerhof", "Hansen"])

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- BUTTON ----------------------
colb1, colb2 = st.columns(2)
calc = colb1.button("🔍 Calculate")
clear = colb2.button("🧹 Clear")

if clear:
    st.experimental_rerun()

# ---------------------- RESULT ----------------------
if calc:

    qult = calculate_bearing(method, B, L, D, c, phi, gamma, ex, ey)

    if qult is None:
        st.error("❌ Eccentricity มากเกินไป → B' ติดลบ")
    else:
        qall = qult / FS
        B_eff = B - 2*ex

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📊 Results")
        st.write(f"B' = {B_eff:.2f} m")

        st.markdown(f'<div class="result">q_ult = {qult:.2f} kPa</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result">q_all = {qall:.2f} kPa</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------------- GRAPH q vs B ----------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 q vs B")

        B_vals = np.linspace(0.5, B*2, 30)
        q_vals = []

        for b in B_vals:
            q = calculate_bearing(method, b, L, D, c, phi, gamma, ex, ey)
            q_vals.append(q if q else 0)

        fig, ax = plt.subplots()
        ax.plot(B_vals, q_vals)
        ax.set_xlabel("B (m)")
        ax.set_ylabel("q_ult (kPa)")
        ax.set_title("Variation of q with B")

        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------------- SENSITIVITY ----------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Sensitivity Analysis")

        param = st.selectbox("Parameter", ["B", "D", "c", "φ", "γ"])

        base = {"B": B, "D": D, "c": c, "φ": phi, "γ": gamma}

        var = np.linspace(0.8, 1.2, 25)
        q_sen = []

        for v in var:
            temp = base.copy()
            temp[param] *= v

            q = calculate_bearing(
                method,
                temp["B"], L, temp["D"],
                temp["c"], temp["φ"],
                temp["γ"], ex, ey
            )
            q_sen.append(q if q else 0)

        x = var * base[param]

        fig2, ax2 = plt.subplots()
        ax2.plot(x, q_sen)
        ax2.set_xlabel(param)
        ax2.set_ylabel("q_ult (kPa)")
        ax2.set_title(f"Sensitivity vs {param}")

        st.pyplot(fig2)
        st.markdown('</div>', unsafe_allow_html=True)
