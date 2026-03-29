import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

st.title("📊 Pavement Design (AASHTO 1993)")

# ------------------------
# TABS (🔥 เพิ่มตรงนี้)
# ------------------------
tab1, tab2 = st.tabs(["📊 ผลการออกแบบ", "ℹ️ ทฤษฎีและสูตร"])

# ========================
# TAB 1 = ของเดิมทั้งหมด
# ========================
with tab1:

    # ------------------------
    # SIDEBAR
    # ------------------------
    st.sidebar.header("🔧 Input")

    mode = st.sidebar.radio("เลือกประเภท", ["Flexible Pavement", "Rigid Pavement"])

    W18 = st.sidebar.number_input("W18", value=5000000.0)
    SN_required = st.sidebar.number_input("SN Required", value=5.240)

    # ========================
    # FLEXIBLE
    # ========================
    if mode == "Flexible Pavement":

        st.header("Flexible Pavement")

        st.sidebar.markdown("## 🧱 Layer Configuration")

        with st.sidebar.expander("Layer 1: Asphalt (AC)", expanded=True):
            a1 = st.number_input("a1 (AC)", value=0.40)
            m1 = st.number_input("m1 (AC)", value=1.10)
            d1 = st.number_input("Thickness AC (cm)", value=20.3)

        with st.sidebar.expander("Layer 2: Base (CTBAC)"):
            a2 = st.number_input("a2 (Base)", value=0.18)
            m2 = st.number_input("m2 (Base)", value=1.10)
            d2 = st.number_input("Thickness Base (cm)", value=22.2)

        with st.sidebar.expander("Layer 3: Subbase"):
            a3 = st.number_input("a3 (Subbase)", value=0.13)
            m3 = st.number_input("m3 (Subbase)", value=1.10)
            d3 = st.number_input("Thickness Subbase (cm)", value=10.2)

        def SN(a, m, D):
            return a * m * (D / 2.54)

        SN_total = SN(a1, m1, d1) + SN(a2, m2, d2) + SN(a3, m3, d3)

        st.info(f"W18 = {W18:,.0f}")

        if SN_total >= SN_required:
            st.success(f"SN = {SN_total:.3f} ≥ {SN_required}")
        else:
            st.error(f"SN = {SN_total:.3f} < {SN_required}")

    # ========================
    # RIGID
    # ========================
    if mode == "Rigid Pavement":

        st.header("Rigid Pavement (Improved)")

        k = st.sidebar.number_input("Subgrade k (pci)", value=50.0)
        k_base = st.sidebar.number_input("Base improvement (pci)", value=50.0)
        base_thickness = st.sidebar.number_input("Base thickness (cm)", value=15.0)

        Sc = st.sidebar.number_input("S'c (psi)", value=650.0)
        J = st.sidebar.number_input("J", value=3.2)
        Cd = st.sidebar.number_input("Cd", value=1.0)

        k_effective = k + k_base

        def calc_d():
            d = ((W18 / 1e6)**0.25) * (100 / k_effective)**0.1 * (650 / Sc)**0.2 * 8
            return max(d, 5)

        d_in = calc_d()
        d_cm = d_in * 2.54

        st.subheader("📊 Result")
        st.write(f"Concrete Thickness = {d_cm:.2f} cm")

        # Design Check
        st.subheader("✅ Design Check")

        W18_capacity = (d_cm / 20)**4 * 1_000_000
        ratio = W18_capacity / W18

        if ratio >= 1:
            st.success(f"✔️ D = {d_cm:.0f} cm รับ W18 (Ratio = {ratio:.3f})")
        else:
            st.error(f"❌ ไม่ผ่าน (Ratio = {ratio:.3f})")

# ========================
# TAB 2 = 🔥 ทฤษฎีและสูตร
# ========================
with tab2:

    st.header("ℹ️ ทฤษฎีและสูตร AASHTO 1993")

    st.markdown("""
    ### 📘 Rigid Pavement Design Equation

    log(W18) = ZR·So + 7.35·log(D+1) − 0.06  
    + log(ΔPSI / (4.5 − 1.5)) / [1 + 1.624×10⁷ / (D+1)⁸·⁴⁶]  
    + (4.22 − 0.32·pt) × log[Sc·Cd·(D⁰·⁷⁵ − 1.132) / (215.63·J·(D⁰·⁷⁵ − 18.42 / (Ec/k)⁰·²⁵))]

    ---
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🔧 ตัวแปร

        - D = ความหนาแผ่น (inch)  
        - Sc = Modulus of Rupture  
        - Ec = Elastic Modulus  
        - k = Subgrade Reaction  
        - J = Load Transfer  
        - Cd = Drainage Coefficient  
        """)

    with col2:
        st.markdown("""
        ### 📋 ขั้นตอนออกแบบ

        1. กำหนด W18  
        2. เลือก Reliability  
        3. กำหนด ΔPSI  
        4. เลือกวัสดุ  
        5. คำนวณ k  
        6. คำนวณ D  
        """)

    st.info("หน่วย: 1 inch = 2.54 cm | 1 MPa = 145 psi")
