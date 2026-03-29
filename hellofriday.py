import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Pavement Design (AASHTO 1993)")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 ผลการออกแบบ",
    "ℹ️ ทฤษฎีและสูตร",
    "📈 Sensitivity",
    "🚀 Advanced Tools"
])

# ================= TAB 1 =================
with tab1:

    st.sidebar.header("🔧 Input")

    mode = st.sidebar.radio("เลือกประเภท", ["Flexible Pavement", "Rigid Pavement"])

    W18 = st.sidebar.number_input("W18", value=5000000.0)
    SN_required = st.sidebar.number_input("SN Required", value=5.240)

    # ---------- FLEXIBLE ----------
    if mode == "Flexible Pavement":

        st.header("Flexible Pavement")

        st.sidebar.markdown("## 🧱 Layer Configuration")

        with st.sidebar.expander("Layer 1: Asphalt (AC)", expanded=True):
            a1 = st.number_input("a1", value=0.40)
            m1 = st.number_input("m1", value=1.10)
            d1 = st.number_input("Thickness (cm)", value=20.3)

        with st.sidebar.expander("Layer 2: Base"):
            a2 = st.number_input("a2", value=0.18)
            m2 = st.number_input("m2", value=1.10)
            d2 = st.number_input("Thickness (cm)", value=22.2)

        with st.sidebar.expander("Layer 3: Subbase"):
            a3 = st.number_input("a3", value=0.13)
            m3 = st.number_input("m3", value=1.10)
            d3 = st.number_input("Thickness (cm)", value=10.2)

        # ---- CALC ----
        SN1 = a1*m1*(d1/2.54)
        SN2 = a2*m2*(d2/2.54)
        SN3 = a3*m3*(d3/2.54)
        SN_total = SN1 + SN2 + SN3

        st.subheader("📊 Result")

        if SN_total >= SN_required:
            st.success(f"SN = {SN_total:.3f} ≥ {SN_required}")
        else:
            st.error(f"SN = {SN_total:.3f} < {SN_required}")

        # ---- CROSS ----
        st.subheader("🏗️ Cross Section")

        total = d1 + d2 + d3
        scale = 400 / total if total else 1

        html = f"""
        <div style="width:300px;margin:auto;">
        <div style="height:{d1*scale}px;background:#2B2D42;color:white;text-align:center;">AC {d1:.1f} cm</div>
        <div style="height:{d2*scale}px;background:#3A86FF;color:white;text-align:center;">Base {d2:.1f} cm</div>
        <div style="height:{d3*scale}px;background:#8338EC;color:white;text-align:center;">Subbase {d3:.1f} cm</div>
        <div style="height:80px;background:#1B4332;color:white;text-align:center;">Subgrade</div>
        </div>
        """

        st.markdown(html, unsafe_allow_html=True)

    # ---------- RIGID ----------
    if mode == "Rigid Pavement":

        st.header("Rigid Pavement")

        k = st.sidebar.number_input("k", value=50.0)
        k_base = st.sidebar.number_input("Base", value=50.0)
        Sc = st.sidebar.number_input("Sc", value=650.0)

        k_eff = k + k_base
        d = max(((W18/1e6)**0.25)*(100/k_eff)**0.1*(650/Sc)**0.2*8,5)
        d_cm = d*2.54

        st.subheader("📊 Result")
        st.write(f"{d_cm:.2f} cm")

# ================= TAB 2 =================
with tab2:

    st.header("📘 ทฤษฎีและสูตร AASHTO 1993")

    st.subheader("Flexible Pavement")

    st.latex(r"SN = a_1 D_1 m_1 + a_2 D_2 m_2 + a_3 D_3 m_3")

    st.markdown("""
    **ตัวแปร:**
    - SN = Structural Number  
    - aᵢ = layer coefficient  
    - Dᵢ = thickness (inch)  
    - mᵢ = drainage factor  
    """)

    st.subheader("Rigid Pavement")

    st.latex(r"""
    \log_{10}(W_{18}) =
    Z_R S_o + 7.35\log_{10}(D+1)
    """)

    st.markdown("""
    **ตัวแปร:**
    - W18 = ESAL  
    - D = thickness  
    - k = subgrade reaction  
    - Sc = modulus of rupture  
    """)
