import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

st.title("📊 Pavement Design (AASHTO 1993)")

# ------------------------
# TABS
# ------------------------
tab1, tab2 = st.tabs(["📊 ผลการออกแบบ", "ℹ️ ทฤษฎีและสูตร"])

# =========================================================
# TAB 1 = DESIGN (ห้ามพัง)
# =========================================================
with tab1:

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

        # Cross Section
        st.subheader("🏗️ หน้าตัดโครงสร้างทาง")

        layers = [
            {"name": "AC", "thickness": d1, "color": "#2B2D42"},
            {"name": "Base (CTBAC)", "thickness": d2, "color": "#3A86FF"},
            {"name": "Subbase", "thickness": d3, "color": "#8338EC"},
        ]

        total = sum([l["thickness"] for l in layers])
        scale = 400 / total if total != 0 else 1

        html = '<div style="display:flex; justify-content:center;">'
        html += '<div style="width:300px; border-radius:16px; overflow:hidden; box-shadow:0 0 20px rgba(0,0,0,0.4); font-family:Segoe UI;">'

        for layer in layers:
            h = layer["thickness"] * scale
            html += (
                f'<div style="height:{h}px;background:{layer["color"]};display:flex;align-items:center;justify-content:center;color:white;font-weight:600;">'
                f'{layer["name"]}<br>{layer["thickness"]:.1f} cm</div>'
            )

        html += '<div style="height:80px;background:#1B4332;color:white;display:flex;align-items:center;justify-content:center;">Subgrade</div>'
        html += '</div></div>'

        st.markdown(html, unsafe_allow_html=True)

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
            st.success(f"✔️ D = {d_cm:.0f} cm รับ W18 = {W18:,.0f} (Ratio = {ratio:.3f})")
        else:
            st.error(f"❌ ไม่ผ่าน (Ratio = {ratio:.3f})")

        # Cross Section
        st.subheader("🏗️ Cross Section")

        scale = 4

        html = (
            f'<div style="display:flex; justify-content:center;">'
            f'<div style="width:300px; border-radius:16px; overflow:hidden; box-shadow:0 0 20px rgba(0,0,0,0.4); font-family:Segoe UI;">'

            f'<div style="height:{d_cm*scale}px;background:#6C757D;display:flex;align-items:center;justify-content:center;color:white;font-weight:600;">'
            f'{d_cm:.1f} cm ({d_in:.2f} in)</div>'

            f'<div style="height:{base_thickness*scale}px;background:#588157;display:flex;align-items:center;justify-content:center;color:white;font-weight:600;">'
            f'{base_thickness:.0f} cm (+{k_base:.0f} pci)</div>'

            f'<div style="height:80px;background:#7F5539;display:flex;align-items:center;justify-content:center;color:white;font-weight:600;">'
            f'k = {k:.0f} pci</div>'

            '</div></div>'
        )

        st.markdown(html, unsafe_allow_html=True)

# =========================================================
# TAB 2 = THEORY (🔥 โปร)
# =========================================================
with tab2:

    st.header("📘 ทฤษฎีและสูตร AASHTO 1993")

    with st.expander("📐 สูตรออกแบบ Rigid (Full Equation)", expanded=True):
        st.latex(r'''
        \log_{10}(W_{18}) = Z_R S_o + 7.35\log_{10}(D+1) - 0.06 
        + \frac{\log_{10}\left(\frac{\Delta PSI}{4.5-1.5}\right)}
        {1 + \frac{1.624\times10^7}{(D+1)^{8.46}}}
        + (4.22 - 0.32p_t)\log_{10}\left(
        \frac{S_c C_d (D^{0.75}-1.132)}
        {215.63 J \left(D^{0.75} - \frac{18.42}{(E_c/k)^{0.25}}\right)}
        \right)
        ''')

    with st.expander("🔧 ความหมายตัวแปร"):
        st.markdown("""
        - **W18** = จำนวน ESAL  
        - **D** = ความหนาแผ่น (inch)  
        - **ZR, So** = Reliability  
        - **ΔPSI** = Serviceability loss  
        - **Sc, Ec** = คุณสมบัติคอนกรีต  
        - **k** = Subgrade  
        - **J, Cd** = Joint & Drainage  
        """)

    with st.expander("📋 ตัวอย่างคำนวณ"):
        st.markdown("""
        ตัวอย่าง:

        - W18 = 5,000,000  
        - k = 50 pci  
        - Sc = 650 psi  

        จะได้ D ≈ 25–28 cm  
        """)

    st.info("📌 1 inch = 2.54 cm")
