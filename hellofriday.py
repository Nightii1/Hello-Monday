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
# FLEXIBLE (เหมือนเดิม)
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

    SN1 = SN(a1, m1, d1)
    SN2 = SN(a2, m2, d2)
    SN3 = SN(a3, m3, d3)

    SN_total = SN1 + SN2 + SN3

    st.info(f"W18 = {W18:,.0f}")

    st.subheader("📋 ตารางสรุป")

    table = {
        "Layer": ["AC", "Base (CTBAC)", "Subbase"],
        "Thickness (cm)": [d1, d2, d3],
        "SN": [SN1, SN2, SN3]
    }

    st.dataframe(table, use_container_width=True)

    if SN_total >= SN_required:
        st.success(f"SN = {SN_total:.3f} ≥ {SN_required} (ผ่าน)")
    else:
        st.error(f"SN = {SN_total:.3f} < {SN_required} (ไม่ผ่าน)")

    # ------------------------
    # CROSS SECTION FLEXIBLE
    # ------------------------
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
            '<div style="height:' + str(h) + 'px;background:' + layer["color"] +
            ';display:flex;flex-direction:column;align-items:center;justify-content:center;'
            'color:white;font-weight:600;">'
            + layer["name"] + '<br>' + f'{layer["thickness"]:.1f} cm</div>'
        )

    html += '<div style="height:80px;background:#1B4332;color:white;display:flex;align-items:center;justify-content:center;">Subgrade</div>'
    html += '</div></div>'

    st.markdown(html, unsafe_allow_html=True)

# ========================
# RIGID (อัปเกรดแล้ว)
# ========================
if mode == "Rigid Pavement":

    st.header("Rigid Pavement Design")

    # 🔥 INPUT วิศวกรรมจริง
    k = st.sidebar.number_input("k (pci)", value=100.0)
    Sc = st.sidebar.number_input("Modulus of Rupture S'c (psi)", value=650.0)
    J = st.sidebar.number_input("Load Transfer Coefficient J", value=3.2)
    Cd = st.sidebar.number_input("Drainage Coefficient Cd", value=1.0)

    d_input = st.sidebar.number_input("Trial Thickness d (cm)", value=25.0)

    # 🔥 คำนวณ (simplified AASHTO logic)
    d_required = ((W18 / 1000000)**0.25) * (100 / k)**0.1 * (650 / Sc)**0.2 * 20

    st.subheader("📊 Result")

    st.write(f"Required Thickness ≈ {d_required:.2f} cm")
    st.write(f"Provided Thickness = {d_input:.2f} cm")

    if d_input >= d_required:
        st.success("ผ่าน (OK)")
    else:
        st.error("ไม่ผ่าน (Increase thickness)")

    # ------------------------
    # CROSS SECTION RIGID
    # ------------------------
    st.subheader("🏗️ Cross Section")

    scale = 5
    h = d_input * scale

    html = (
        '<div style="display:flex; justify-content:center;">'
        '<div style="width:300px; border-radius:16px; overflow:hidden; '
        'box-shadow:0 0 20px rgba(0,0,0,0.4); font-family:Segoe UI;">'

        '<div style="height:' + str(h) + 'px;background:#ADB5BD;'
        'display:flex;flex-direction:column;align-items:center;justify-content:center;'
        'color:#212529;font-weight:600;">'
        'Concrete Slab<br>' + str(round(d_input,1)) + ' cm</div>'

        '<div style="height:80px;background:#1B4332;color:white;'
        'display:flex;align-items:center;justify-content:center;">Subgrade</div>'

        '</div></div>'
    )

    st.markdown(html, unsafe_allow_html=True)
