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
# FLEXIBLE
# ========================
if mode == "Flexible Pavement":

    st.header("Flexible Pavement")

    a1 = st.sidebar.number_input("a1 (AC)", value=0.40)
    m1 = st.sidebar.number_input("m1", value=1.10)
    d1 = st.sidebar.number_input("AC (cm)", value=20.3)

    a2 = st.sidebar.number_input("a2 (Base)", value=0.18)
    m2 = st.sidebar.number_input("m2", value=1.10)
    d2 = st.sidebar.number_input("Base (cm)", value=22.2)

    a3 = st.sidebar.number_input("a3 (Subbase)", value=0.13)
    m3 = st.sidebar.number_input("m3", value=1.10)
    d3 = st.sidebar.number_input("Subbase (cm)", value=10.2)

    d4 = st.sidebar.number_input("Improvement (cm)", value=10.2)

    def SN(a, m, D):
        return a * m * (D / 2.54)

    SN1 = SN(a1, m1, d1)
    SN2 = SN(a2, m2, d2)
    SN3 = SN(a3, m3, d3)
    SN4 = 0.10 * 1.10 * (d4 / 2.54)

    SN_total = SN1 + SN2 + SN3 + SN4

    st.info(f"W18 = {W18:,.0f}")

    st.subheader("📋 ตารางสรุป")

    table = {
        "Layer": ["AC", "Base (CTBAC)", "Subbase", "Improvement"],
        "Thickness (cm)": [d1, d2, d3, d4],
        "SN": [SN1, SN2, SN3, SN4]
    }

    st.dataframe(table, use_container_width=True)

    if SN_total >= SN_required:
        st.success(f"SN = {SN_total:.3f} ≥ {SN_required} (ผ่าน)")
    else:
        st.error(f"SN = {SN_total:.3f} < {SN_required} (ไม่ผ่าน)")

    # ------------------------
    # CROSS SECTION
    # ------------------------
    st.subheader("🏗️ หน้าตัดโครงสร้างทาง")

    layers = [
        {"name": "AC", "thickness": d1, "color": "#222222"},
        {"name": "Base (CTBAC)", "thickness": d2, "color": "#6b8e9e"},
        {"name": "Subbase", "thickness": d3, "color": "#8b6b43"},
        {"name": "Improvement", "thickness": d4, "color": "#d4a017"},
    ]

    total = sum([l["thickness"] for l in layers])
    if total == 0:
        total = 1

    scale = 400 / total

    html = '<div style="display:flex; justify-content:center;">'
    html += '<div style="width:280px; border:2px solid #ccc;">'

    for layer in layers:
        h = layer["thickness"] * scale

        html += (
            '<div style="height:' + str(h) + 'px;'
            'background:' + layer["color"] + ';'
            'display:flex;flex-direction:column;'
            'align-items:center;justify-content:center;'
            'color:white;font-weight:bold;">'
            + layer["name"] + '<br>'
            + f'{layer["thickness"]:.1f} cm'
            + '</div>'
        )

    html += (
        '<div style="height:80px;background:#704214;'
        'display:flex;align-items:center;justify-content:center;'
        'color:white;font-weight:bold;">'
        'Subgrade</div>'
    )

    html += '</div></div>'

    st.markdown(html, unsafe_allow_html=True)

# ========================
# RIGID
# ========================
if mode == "Rigid Pavement":

    st.header("Rigid Pavement")

    d = st.sidebar.number_input("Concrete Thickness (cm)", value=25.0)

    st.success(f"Thickness = {d:.1f} cm")

    st.subheader("🏗️ Cross Section")

    scale = 5
    h = d * scale

    html = (
        '<div style="display:flex; justify-content:center;">'
        '<div style="width:280px; border:2px solid #ccc;">'

        '<div style="height:' + str(h) + 'px;'
        'background:#dddddd;'
        'display:flex; flex-direction:column;'
        'align-items:center; justify-content:center;'
        'font-weight:bold;">'
        'Concrete<br>' + str(round(d,1)) + ' cm'
        '</div>'

        '<div style="height:80px;background:#704214;'
        'display:flex;align-items:center;justify-content:center;'
        'color:white;font-weight:bold;">'
        'Subgrade</div>'

        '</div></div>'
    )

    st.markdown(html, unsafe_allow_html=True)
