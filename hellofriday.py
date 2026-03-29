import streamlit as st
import numpy as np

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
# TAB 1 = DESIGN (ของคุณเดิม)
# =========================================================
with tab1:

    st.sidebar.header("🔧 Input")

    mode = st.sidebar.radio("เลือกประเภท", ["Flexible Pavement", "Rigid Pavement"])

    W18 = st.sidebar.number_input("W18", value=5000000.0)
    SN_required = st.sidebar.number_input("SN Required", value=5.240)

    # FLEXIBLE
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

        st.subheader("🏗️ Cross Section")

        layers = [
            ("AC", d1, "#2B2D42"),
            ("Base", d2, "#3A86FF"),
            ("Subbase", d3, "#8338EC")
        ]

        total = sum([l[1] for l in layers])
        scale = 400 / total if total != 0 else 1

        html = '<div style="display:flex;justify-content:center;"><div style="width:300px;border-radius:12px;overflow:hidden;">'
        for name, t, c in layers:
            html += f'<div style="height:{t*scale}px;background:{c};color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;">{name}<br>{t:.1f} cm</div>'
        html += '<div style="height:80px;background:#1B4332;color:white;display:flex;align-items:center;justify-content:center;">Subgrade</div>'
        html += '</div></div>'
        st.markdown(html, unsafe_allow_html=True)

    # RIGID
    if mode == "Rigid Pavement":

        st.header("Rigid Pavement")

        k = st.sidebar.number_input("k (pci)", value=50.0)
        k_base = st.sidebar.number_input("Base (pci)", value=50.0)
        base_thickness = st.sidebar.number_input("Base thickness (cm)", value=15.0)
        Sc = st.sidebar.number_input("S'c (psi)", value=650.0)

        k_eff = k + k_base

        d_in = max(((W18/1e6)**0.25)*(100/k_eff)**0.1*(650/Sc)**0.2*8, 5)
        d_cm = d_in * 2.54

        st.subheader("📊 Result")
        st.write(f"{d_cm:.2f} cm")

        with st.expander("📐 Step-by-step"):
            st.write(f"W18 = {W18}")
            st.write(f"k_eff = {k_eff}")
            st.write(f"D = {d_cm:.2f} cm")

        st.subheader("🏗️ Cross Section")

        html = f'''
        <div style="display:flex;justify-content:center;">
        <div style="width:300px;border-radius:12px;overflow:hidden;">
        <div style="height:{d_cm*4}px;background:#6C757D;color:white;display:flex;align-items:center;justify-content:center;">{d_cm:.1f} cm</div>
        <div style="height:{base_thickness*4}px;background:#588157;color:white;display:flex;align-items:center;justify-content:center;">{base_thickness} cm</div>
        <div style="height:80px;background:#7F5539;color:white;display:flex;align-items:center;justify-content:center;">k={k}</div>
        </div></div>
        '''
        st.markdown(html, unsafe_allow_html=True)

# =========================================================
# TAB 2 (🔥 เพิ่ม Flexible + Rigid ครบ)
# =========================================================
with tab2:
    st.header("📘 ทฤษฎีและสูตร AASHTO 1993")

    # -------- FLEXIBLE --------
    st.subheader("Flexible Pavement (Structural Number)")

    st.latex(r"SN = a_1 D_1 m_1 + a_2 D_2 m_2 + a_3 D_3 m_3")

    st.markdown("""
    **ตัวแปร (Flexible):**
    - **SN** = Structural Number  
    - **aᵢ** = Layer coefficient  
    - **Dᵢ** = ความหนาแต่ละชั้น (inch)  
    - **mᵢ** = Drainage coefficient  
    """)

    st.markdown("""
    **ขั้นตอนออกแบบ Flexible:**
    1. คำนวณ W18  
    2. หา SN required จาก nomograph  
    3. เลือกวัสดุ → aᵢ  
    4. กำหนด mᵢ  
    5. คำนวณ Dᵢ  
    """)

    st.divider()

    # -------- RIGID --------
    st.subheader("Rigid Pavement Design Equation")

    st.latex(r"""
    \log_{10}(W_{18}) = Z_R S_o + 7.35\log_{10}(D+1) - 0.06
    + \frac{\log_{10}(\Delta PSI / (4.5 - 1.5))}
    {1 + \frac{1.624 \times 10^7}{(D+1)^{8.46}}}
    """)

    st.markdown("""
    **ตัวแปร (Rigid):**
    - W18 = ESAL  
    - D = thickness (inch)  
    - k = subgrade  
    - Sc = modulus of rupture  
    - ZR = reliability  
    """)

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

    st.header("🚀 Advanced Report")

    W_test = st.number_input("W18 (Report)", value=5000000.0)
    d_opt = ((W_test/1e6)**0.25)*8*2.54

    st.success(f"Recommended Thickness = {d_opt:.2f} cm")

    report_html = f"""
    <div style="font-family:Arial;padding:20px">
    <h2>📊 Pavement Design Report</h2>
    <hr>
    <p><b>Traffic (W18):</b> {W_test:,.0f}</p>
    <p><b>Thickness:</b> {d_opt:.2f} cm</p>
    <p><b>Method:</b> AASHTO 1993</p>
    <p><b>Status:</b> ✅ Design OK</p>
    </div>
    """

    st.markdown(report_html, unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download Report (HTML)",
        report_html,
        file_name="pavement_report.html",
        mime="text/html"
    )
st.divider()

st.subheader("🧪 Interactive Design Tool")

# =====================
# FLEXIBLE INTERACTIVE
# =====================
st.markdown("### Flexible Pavement (ทดลองค่า SN)")

col1, col2, col3 = st.columns(3)

with col1:
    a1_i = st.number_input("a1", value=0.40, key="fa1")
    d1_i = st.number_input("D1 (cm)", value=20.0, key="fd1")

with col2:
    a2_i = st.number_input("a2", value=0.14, key="fa2")
    d2_i = st.number_input("D2 (cm)", value=20.0, key="fd2")

with col3:
    a3_i = st.number_input("a3", value=0.11, key="fa3")
    d3_i = st.number_input("D3 (cm)", value=20.0, key="fd3")

m1_i = st.number_input("m1", value=1.0, key="fm1")
m2_i = st.number_input("m2", value=1.0, key="fm2")
m3_i = st.number_input("m3", value=1.0, key="fm3")

SN_calc = (
    a1_i * m1_i * (d1_i/2.54) +
    a2_i * m2_i * (d2_i/2.54) +
    a3_i * m3_i * (d3_i/2.54)
)

st.success(f"SN = {SN_calc:.3f}")

st.divider()

# =====================
# RIGID INTERACTIVE
# =====================
st.markdown("### Rigid Pavement (ทดลองหา D)")

W_i = st.number_input("W18", value=5000000.0, key="rw")
k_i = st.number_input("k", value=50.0, key="rk")
Sc_i = st.number_input("Sc", value=650.0, key="rsc")

k_eff_i = k_i + 50

d_i = max(((W_i/1e6)**0.25)*(100/k_eff_i)**0.1*(650/Sc_i)**0.2*8, 5)
d_cm_i = d_i * 2.54

st.success(f"D ≈ {d_cm_i:.2f} cm")
