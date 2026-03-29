import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Pavement Design (AASHTO 1993)")

# ------------------------
# TABS
# ------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 ผลการออกแบบ",
    "ℹ️ ทฤษฎีและสูตร",
    "📈 Sensitivity",
    "🚀 Advanced Tools"
])

# =========================================================
# TAB 1
# =========================================================
with tab1:

    st.sidebar.header("🔧 Input")

    mode = st.sidebar.radio("เลือกประเภท", ["Flexible Pavement", "Rigid Pavement"])

    W18 = st.sidebar.number_input("W18", value=5000000.0)
    SN_required = st.sidebar.number_input("SN Required", value=5.240)

    # ================= FLEXIBLE =================
    if mode == "Flexible Pavement":

        st.header("Flexible Pavement")

        st.sidebar.markdown("## 🧱 Layer Configuration")

        with st.sidebar.expander("Layer 1: Asphalt (AC)", expanded=True):
            a1 = st.sidebar.number_input("a1", value=0.40)
            m1 = st.sidebar.number_input("m1", value=1.10)
            d1 = st.sidebar.number_input("Thickness (cm)", value=20.3)

        with st.sidebar.expander("Layer 2: Base"):
            a2 = st.sidebar.number_input("a2", value=0.18)
            m2 = st.sidebar.number_input("m2", value=1.10)
            d2 = st.sidebar.number_input("Thickness (cm)", value=22.2)

        with st.sidebar.expander("Layer 3: Subbase"):
            a3 = st.sidebar.number_input("a3", value=0.13)
            m3 = st.sidebar.number_input("m3", value=1.10)
            d3 = st.sidebar.number_input("Thickness (cm)", value=10.2)

        # ===== CALC =====
        SN1 = a1*m1*(d1/2.54)
        SN2 = a2*m2*(d2/2.54)
        SN3 = a3*m3*(d3/2.54)
        SN_total = SN1 + SN2 + SN3

        st.subheader("📊 Result")

        if SN_total >= SN_required:
            st.success(f"SN = {SN_total:.3f} ≥ {SN_required}")
        else:
            st.error(f"SN = {SN_total:.3f} < {SN_required}")

        # ===== CROSS SECTION =====
        st.subheader("🏗️ Cross Section")

        total = d1 + d2 + d3
        scale = 400 / total if total != 0 else 1

        html = '<div style="display:flex;justify-content:center;"><div style="width:300px;">'

        html += f'<div style="height:{d1*scale}px;background:#2B2D42;color:white;text-align:center;">AC<br>{d1:.1f} cm</div>'
        html += f'<div style="height:{d2*scale}px;background:#3A86FF;color:white;text-align:center;">Base<br>{d2:.1f} cm</div>'
        html += f'<div style="height:{d3*scale}px;background:#8338EC;color:white;text-align:center;">Subbase<br>{d3:.1f} cm</div>'
        html += '<div style="height:80px;background:#1B4332;color:white;text-align:center;">Subgrade</div>'

        html += '</div></div>'

        st.markdown(html, unsafe_allow_html=True)

        # ===== TABLE =====
        st.subheader("📊 Layer Summary")

        df = pd.DataFrame({
            "Layer": ["AC", "Base", "Subbase"],
            "Thickness (cm)": [d1, d2, d3],
            "SN": [SN1, SN2, SN3]
        })

        st.dataframe(df)

        # ===== GRAPH =====
        st.bar_chart(df.set_index("Layer")["SN"])

    # ================= RIGID =================
    if mode == "Rigid Pavement":

        st.header("Rigid Pavement")

        k = st.sidebar.number_input("k", value=50.0)
        k_base = st.sidebar.number_input("Base", value=50.0)
        base_thickness = st.sidebar.number_input("Base thickness", value=15.0)
        Sc = st.sidebar.number_input("Sc", value=650.0)

        k_eff = k + k_base

        d = max(((W18/1e6)**0.25)*(100/k_eff)**0.1*(650/Sc)**0.2*8,5)
        d_cm = d*2.54

        st.subheader("📊 Result")
        st.write(f"{d_cm:.2f} cm")

        st.subheader("🏗️ Cross Section")

        st.markdown(f"""
        <div style="width:300px;margin:auto;">
        <div style="height:{d_cm*4}px;background:#6C757D;color:white;text-align:center;">
        Concrete {d_cm:.1f} cm
        </div>
        <div style="height:{base_thickness*4}px;background:#588157;color:white;text-align:center;">
        Base {base_thickness} cm
        </div>
        <div style="height:80px;background:#7F5539;color:white;text-align:center;">
        k={k}
        </div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAB 2 (คืนสูตรครบ)
# =========================================================
with tab2:
    st.header("📘 ทฤษฎีและสูตร AASHTO 1993")

    st.latex(r"SN = a_1D_1m_1 + a_2D_2m_2 + a_3D_3m_3")

    st.markdown("""
    **Flexible Variables:**
    - aᵢ = layer coefficient
    - Dᵢ = thickness (inch)
    - mᵢ = drainage factor
    """)

    st.latex(r"\log_{10}(W_{18}) = Z_RS_o + 7.35\log(D+1)")

# =========================================================
# TAB 3
# =========================================================
with tab3:
    st.header("📈 Sensitivity")
    W = np.linspace(1e5,1e7,50)
    d = ((W/1e6)**0.25)*8*2.54
    st.line_chart({"Thickness": d})

# =========================================================
# TAB 4
# =========================================================
with tab4:
    st.header("🚀 Advanced Tools")
    st.write("Coming soon...")
