import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

st.title("📊 Pavement Design (AASHTO 1993)")

# ------------------------
# INPUT
# ------------------------
st.sidebar.header("Input")

W18 = st.sidebar.number_input("W18", value=10000000.0)
R = st.sidebar.slider("Reliability (%)",50,99,85)
So = st.sidebar.number_input("So",value=0.45)
deltaPSI = st.sidebar.number_input("ΔPSI",value=1.7)
Mr = st.sidebar.number_input("Mr (psi)",value=7500.0)

ZR_table = {
50:0,60:-0.253,70:-0.524,75:-0.674,
80:-0.841,85:-1.036,90:-1.282,
95:-1.645,98:-2.054,99:-2.327
}
ZR = ZR_table.get(R,-1.036)

# ------------------------
# FUNCTION SN
# ------------------------
def calc_SN_required(W18, Mr, So, ZR, deltaPSI):
    SN = 3.0
    for _ in range(20):
        term1 = ZR * So
        term2 = 9.36 * np.log10(SN + 1)
        term3 = (np.log10(deltaPSI/(4.2-1.5))) / (0.40 + (1094/(SN+1)**5.19))
        term4 = 2.32 * np.log10(Mr) - 8.07
        SN = 10 ** ((np.log10(W18) + term1 - term2 - term3 - term4)/9.36)
    return SN

SN_required = calc_SN_required(W18, Mr, So, ZR, deltaPSI)

st.subheader("📊 Flexible Pavement")

# ------------------------
# INPUT LAYERS
# ------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    D1 = st.number_input("AC (cm)", value=20.3)
with col2:
    D2 = st.number_input("Base (cm)", value=22.2)
with col3:
    D3 = st.number_input("Subbase (cm)", value=10.2)
with col4:
    D4 = st.number_input("Improvement (cm)", value=10.2)

# coefficients
a1, m1 = 0.40, 1.10
a2, m2 = 0.18, 1.10
a3, m3 = 0.13, 1.10
a4, m4 = 0.10, 1.10

def SN(a, m, D):
    return a*m*(D/2.54)

SN1 = SN(a1,m1,D1)
SN2 = SN(a2,m2,D2)
SN3 = SN(a3,m3,D3)
SN4 = SN(a4,m4,D4)

SN_total = SN1 + SN2 + SN3 + SN4

# ------------------------
# TABLE
# ------------------------
st.subheader("📋 ตารางสรุป")

data = {
    "Layer":["AC","Base","Subbase","Improvement"],
    "Thickness (cm)":[D1,D2,D3,D4],
    "Thickness (inch)":[D1/2.54,D2/2.54,D3/2.54,D4/2.54],
    "SN":[SN1,SN2,SN3,SN4]
}

st.dataframe(data, use_container_width=True)

# ------------------------
# RESULT
# ------------------------
if SN_total >= SN_required:
    st.success(f"SN = {SN_total:.3f} ≥ {SN_required:.3f} (ผ่าน)")
else:
    st.error(f"SN = {SN_total:.3f} < {SN_required:.3f} (ไม่ผ่าน)")

# ------------------------
# CROSS SECTION (HTML FIXED)
# ------------------------
st.subheader("🏗️ หน้าตัดโครงสร้างทาง")

total = D1 + D2 + D3 + D4
if total == 0:
    total = 1

scale = 400 / total

section_html = f"""
<div style="display:flex; justify-content:center;">

    <div style="width:260px; border:2px solid #ccc;">

        <div style="height:{D1*scale}px; background:#222;
        display:flex; align-items:center; justify-content:center;
        color:white; font-weight:bold;">
        {D1:.1f} cm
        </div>

        <div style="height:{D2*scale}px; background:#6b8e9e;
        display:flex; align-items:center; justify-content:center;
        color:white; font-weight:bold;">
        {D2:.1f} cm
        </div>

        <div style="height:{D3*scale}px; background:#8b6b43;
        display:flex; align-items:center; justify-content:center;
        color:white; font-weight:bold;">
        {D3:.1f} cm
        </div>

        <div style="height:{D4*scale}px; background:#d4a017;
        display:flex; align-items:center; justify-content:center;
        color:black; font-weight:bold;">
        {D4:.1f} cm
        </div>

        <div style="height:80px; background:#704214;
        display:flex; align-items:center; justify-content:center;
        color:white; font-weight:bold;">
        Subgrade
        </div>

    </div>

</div>
"""

# 🔥 สำคัญที่สุด
st.markdown(section_html, unsafe_allow_html=True)

# ------------------------
# RIGID
# ------------------------
st.markdown("---")
st.subheader("🧱 Rigid Pavement")

D = st.number_input("Concrete Thickness (cm)", value=25.0)
st.info(f"Recommended Thickness = {D:.1f} cm")
