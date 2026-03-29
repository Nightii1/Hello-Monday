import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(layout="wide")

st.title("🚀 Pavement Design Pro (AASHTO 1993)")

# ------------------------
# TABS
# ------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 ผลการออกแบบ",
    "📘 ทฤษฎีและสูตร",
    "📈 Sensitivity"
])

# =========================================================
# TAB 1 = DESIGN
# =========================================================
with tab1:

    st.sidebar.header("🔧 Input")

    mode = st.sidebar.radio("เลือกประเภท", ["Flexible Pavement", "Rigid Pavement"])

    W18 = st.sidebar.number_input("W18", value=5000000.0)

    # ========================
    # FLEXIBLE (เดิม)
    # ========================
    if mode == "Flexible Pavement":

        st.header("Flexible Pavement")

        a1, m1, d1 = 0.40, 1.10, 20.3
        a2, m2, d2 = 0.18, 1.10, 22.2
        a3, m3, d3 = 0.13, 1.10, 10.2

        def SN(a, m, D):
            return a * m * (D / 2.54)

        SN_total = SN(a1, m1, d1) + SN(a2, m2, d2) + SN(a3, m3, d3)

        st.success(f"SN = {SN_total:.3f}")

    # ========================
    # RIGID (🔥 PRO)
    # ========================
    if mode == "Rigid Pavement":

        st.header("Rigid Pavement (Advanced)")

        k = st.sidebar.number_input("k (pci)", value=50.0)
        k_base = st.sidebar.number_input("Base improvement", value=50.0)
        Sc = st.sidebar.number_input("Sc (psi)", value=650.0)

        k_eff = k + k_base

        def calc_d(W):
            d = ((W / 1e6)**0.25) * (100 / k_eff)**0.1 * (650 / Sc)**0.2 * 8
            return max(d, 5)

        d_in = calc_d(W18)
        d_cm = d_in * 2.54

        st.subheader("📊 Result")
        st.success(f"D = {d_cm:.2f} cm")

        # 🔥 STEP BY STEP
        with st.expander("📐 แสดงขั้นตอนคำนวณ"):
            st.write(f"1. W18 = {W18:,.0f}")
            st.write(f"2. k_effective = {k_eff}")
            st.write(f"3. ใช้ empirical formula")
            st.write(f"4. ได้ D = {d_cm:.2f} cm")

        # 🔥 EXPORT PDF
        def create_pdf():
            doc = SimpleDocTemplate("report.pdf")
            styles = getSampleStyleSheet()
            story = []
            story.append(Paragraph(f"D = {d_cm:.2f} cm", styles["Normal"]))
            doc.build(story)

        if st.button("📄 Export PDF"):
            create_pdf()
            st.success("ดาวน์โหลด report.pdf ได้เลย")

# =========================================================
# TAB 2 = THEORY
# =========================================================
with tab2:

    st.header("📘 Theory (AASHTO 1993)")

    st.latex(r'''
    \log_{10}(W_{18}) = Z_R S_o + 7.35\log(D+1)
    ''')

    st.info("Full equation + parameters")

# =========================================================
# TAB 3 = SENSITIVITY
# =========================================================
with tab3:

    st.header("📈 Sensitivity Analysis")

    W_range = np.linspace(1e5, 1e7, 50)

    k = 50
    Sc = 650

    def calc_d(W):
        return ((W / 1e6)**0.25) * (100 / k)**0.1 * (650 / Sc)**0.2 * 8

    d_vals = [calc_d(w)*2.54 for w in W_range]

    fig = plt.figure()
    plt.plot(W_range, d_vals)
    plt.xlabel("W18")
    plt.ylabel("Thickness (cm)")

    st.pyplot(fig)
