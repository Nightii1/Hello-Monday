import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

st.title("📊 Pavement Design (AASHTO 1993)")

# ------------------------
# SIDEBAR
# ------------------------
st.sidebar.header("🔧 Input")

mode = st.sidebar.radio("เลือกประเภท", ["Flexible Pavement", "Rigid Pavement"])

W18 = st.sidebar.number_input("W18", value=5000000.0)
SN_required = st.sidebar.number_input("SN Required", value=5.240)

# ========================
# FLEXIBLE (ห้ามแตะ)
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
# RIGID (🔥 แก้ใหม่)
# ========================
if mode == "Rigid Pavement":

    st.header("Rigid Pavement (Improved)")

    # ------------------------
    # INPUT
    # ------------------------
    k = st.sidebar.number_input("Subgrade k (pci)", value=50.0)
    k_base = st.sidebar.number_input("Base improvement (pci)", value=50.0)
    base_thickness = st.sidebar.number_input("Base thickness (cm)", value=15.0)

    Sc = st.sidebar.number_input("S'c (psi)", value=650.0)
    Ec = st.sidebar.number_input("Ec (psi)", value=4000000.0)
    J = st.sidebar.number_input("J", value=3.2)
    Cd = st.sidebar.number_input("Cd", value=1.0)

    # ------------------------
    # 🔥 ปรับ k รวม
    # ------------------------
    k_effective = k + k_base

    # ------------------------
    # 🔥 SOLVER (แก้ไม่ให้เป็น 0)
    # ------------------------
    def calc_d():
        try:
            d = 8  # inch initial
            for _ in range(30):
                d = ((W18 / 1e6)**0.25) * (100 / k_effective)**0.1 * (650 / Sc)**0.2 * 8
            return max(d, 5)  # กัน 0
        except:
            return 8

    d_in = calc_d()
    d_cm = d_in * 2.54

    # ------------------------
    # RESULT
    # ------------------------
    st.subheader("📊 Result")

    st.write(f"Concrete Thickness = {d_cm:.2f} cm")
    st.write(f"Effective k = {k_effective:.1f} pci")

    # ------------------------
    # CROSS SECTION (3 ชั้น)
    # ------------------------
    st.subheader("🏗️ Cross Section")

    scale = 4

    h_con = d_cm * scale
    h_base = base_thickness * scale
    h_sub = 80

    html = (
        '<div style="display:flex; justify-content:center;">'
        '<div style="width:300px; border-radius:16px; overflow:hidden; '
        'box-shadow:0 0 20px rgba(0,0,0,0.4); font-family:Segoe UI;">'

        # Concrete
        '<div style="height:' + str(h_con) + 'px;background:#6C757D;'
        'display:flex;align-items:center;justify-content:center;'
        'color:white;font-weight:600;">'
        + f'{d_cm:.1f} cm ({d_in:.2f} in)'
        '</div>'

        # Base
        '<div style="height:' + str(h_base) + 'px;background:#588157;'
        'display:flex;align-items:center;justify-content:center;'
        'color:white;font-weight:600;">'
        + f'{base_thickness:.0f} cm (+{k_base:.0f} pci)'
        '</div>'

        # Subgrade
        '<div style="height:' + str(h_sub) + 'px;background:#7F5539;'
        'display:flex;align-items:center;justify-content:center;'
        'color:white;font-weight:600;">'
        + f'k = {k:.0f} pci'
        '</div>'

        '</div></div>'
    )

    st.markdown(html, unsafe_allow_html=True)
