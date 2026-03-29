import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

# ------------------------
# STYLE
# ------------------------
st.markdown("""
<style>
.metric-box{
    padding:15px;
    border-radius:12px;
    color:white;
    text-align:center;
    font-size:20px;
    font-weight:bold;
}
.bg1{background:#1f77b4;}
.bg2{background:#2ca02c;}
.bg3{background:#ff7f0e;}
.bg4{background:#9467bd;}
</style>
""", unsafe_allow_html=True)

# ------------------------
# FUNCTION
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

# ------------------------
# SIDEBAR
# ------------------------
st.sidebar.title("🚧 AASHTO 1993")

road = st.sidebar.radio(
    "เลือกประเภทผิวทาง",
    ["Flexible Pavement","Rigid Pavement"]
)

W18 = st.sidebar.number_input("W18", value=10000000.0)
R = st.sidebar.slider("Reliability (%)",50,99,85)
So = st.sidebar.number_input("So",value=0.45)
deltaPSI = st.sidebar.number_input("ΔPSI",value=1.7)
Mr = st.sidebar.number_input("Mr",value=8000.0)

ZR_table = {
50:0,60:-0.253,70:-0.524,75:-0.674,
80:-0.841,85:-1.036,90:-1.282,
95:-1.645,98:-2.054,99:-2.327
}
ZR = ZR_table.get(R,-1.036)

# ========================
# FLEXIBLE
# ========================
if road == "Flexible Pavement":

    st.title("Flexible Pavement")

    SN_req = calc_SN_required(W18, Mr, So, ZR, deltaPSI)

    c1,c2,c3 = st.columns(3)

    with c1:
        a1=st.number_input("a1",0.0,1.0,0.40)
        m1=st.number_input("m1",0.0,2.0,1.0)
        d1=st.number_input("AC (cm)",0.0,100.0,5.0)

    with c2:
        a2=st.number_input("a2",0.0,1.0,0.18)
        m2=st.number_input("m2",0.0,2.0,1.1)
        d2=st.number_input("Base (cm)",0.0,100.0,20.0)

    with c3:
        a3=st.number_input("a3",0.0,1.0,0.13)
        m3=st.number_input("m3",0.0,2.0,1.1)
        d3=st.number_input("Subbase (cm)",0.0,100.0,25.0)

    SN1=a1*m1*(d1/2.54)
    SN2=SN1+a2*m2*(d2/2.54)
    SN3=SN2+a3*m3*(d3/2.54)

    total = d1+d2+d3

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("SN Required", f"{SN_req:.2f}")
    col2.metric("SN Provided", f"{SN3:.2f}")
    col3.metric("Total Thickness", f"{total:.1f} cm")
    col4.metric("W18", f"{W18:,.0f}")

    if SN3 >= SN_req:
        st.success("ผ่าน")
    else:
        st.error("ไม่ผ่าน")

    # ------------------------
    # SECTION (แก้แล้วแน่นอน)
    # ------------------------
    st.subheader("Cross Section")

    max_val = max(d1,d2,d3,1)

    st.write("AC")
    st.progress(d1/max_val)

    st.write("Base")
    st.progress(d2/max_val)

    st.write("Subbase")
    st.progress(d3/max_val)

    st.write("Subgrade")
    st.progress(0.3)

# ========================
# RIGID
# ========================
if road == "Rigid Pavement":

    st.title("Rigid Pavement")

    d = st.number_input("Concrete Thickness (cm)",0.0,100.0,25.0)

    st.metric("Thickness", f"{d:.1f} cm")

    st.subheader("Cross Section")

    st.write("Concrete")
    st.progress(1.0)

    st.write("Subgrade")
    st.progress(0.3)
import streamlit as st

st.set_page_config(layout="wide")

st.title("🏗️ หน้าตัดโครงสร้างทาง")

# ------------------------
# INPUT
# ------------------------
D1 = st.number_input("AC (cm)", value=20.3)
D2 = st.number_input("Base (cm)", value=22.2)
D3 = st.number_input("Subbase (cm)", value=10.2)
D4 = st.number_input("Improvement (cm)", value=10.2)

# ------------------------
# SCALE
# ------------------------
total = D1 + D2 + D3 + D4
if total == 0:
    total = 1

scale = 400 / total

# ------------------------
# HTML SECTION (FIX REAL)
# ------------------------
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

# 🔥 ใช้ตัวนี้เท่านั้น
st.markdown(section_html, unsafe_allow_html=True)
