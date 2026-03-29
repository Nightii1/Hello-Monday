import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

st.title("🚀 Pavement Design Pro (AASHTO 1993)")

tab1, tab2, tab3 = st.tabs([
    "📊 ผลการออกแบบ",
    "📘 ทฤษฎีและสูตร",
    "📈 Sensitivity"
])

# ================= TAB 1 =================
with tab1:

    st.sidebar.header("🔧 Input")

    mode = st.sidebar.radio("เลือกประเภท", ["Flexible Pavement", "Rigid Pavement"])

    W18 = st.sidebar.number_input("W18", value=5000000.0)

    # -------- FLEXIBLE --------
    if mode == "Flexible Pavement":

        st.header("Flexible Pavement")

        a1, m1, d1 = 0.40, 1.10, 20.3
        a2, m2, d2 = 0.18, 1.10, 22.2
        a3, m3, d3 = 0.13, 1.10, 10.2

        def SN(a, m, D):
            return a * m * (D / 2.54)

        SN_total = SN(a1, m1, d1) + SN(a2, m2, d2) + SN(a3, m3, d3)

        st.success(f"SN = {SN_total:.3f}")

    # -------- RIGID --------
    if mode == "Rigid Pavement":

        st.header("Rigid Pavement")

        k = st.sidebar.number_input("k (pci)", value=50.0)
        k_base = st.sidebar.number_input("Base improvement", value=50.0)
        Sc = st.sidebar.number_input("Sc (psi)", value=650.0)

        k_eff = k + k_base

        def calc_d(W):
            d = ((W / 1e6)**0.25) * (100 / k_eff)**0.1 * (650 / Sc)**0.2 * 8
            return max(d, 5)

        d_in = calc_d(W18)
        d_cm = d_in * 2.54

        st.success(f"D = {d_cm:.2f} cm")

        # STEP
        with st.expander("📐 ขั้นตอนคำนวณ"):
            st.write(f"W18 = {W18:,.0f}")
            st.write(f"k_effective = {k_eff}")
            st.write(f"D = {d_cm:.2f} cm")

# ================= TAB 2 =================
with tab2:

    st.header("📘 Theory")

    st.latex(r'''
    \log_{10}(W_{18}) = Z_R S_o + 7.35\log(D+1)
    ''')

# ================= TAB 3 =================
with tab3:

    st.header("📈 Sensitivity")

    W_range = np.linspace(1e5, 1e7, 50)

    k = 50
    Sc = 650

    def calc_d(W):
        return ((W / 1e6)**0.25) * (100 / k)**0.1 * (650 / Sc)**0.2 * 8

    d_vals = [calc_d(w)*2.54 for w in W_range]

    st.line_chart({"Thickness (cm)": d_vals})
