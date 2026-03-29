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
# AASHTO FUNCTION
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

W18 = st.sidebar.number_input("W18 (ESAL)", value=10000000.0, format="%.0f")
R = st.sidebar.slider("Reliability (%)",50,99,85)
So = st.sidebar.number_input("Standard Deviation",value=0.45)
deltaPSI = st.sidebar.number_input("ΔPSI",value=1.7)
Mr = st.sidebar.number_input("Mr (psi)",value=8000.0)

ZR_table = {
50:0,60:-0.253,70:-0.524,75:-0.674,
80:-0.841,85:-1.036,90:-1.282,
95:-1.645,98:-2.054,99:-2.327
}

ZR = ZR_table.get(R,-1.036)

# ------------------------
# FLEXIBLE
# ------------------------
if road == "Flexible Pavement":

    st.title("Flexible Pavement — AASHTO 1993")

    SN_req = calc_SN_required(W18, Mr, So, ZR, deltaPSI)

    st.subheader("Layer Properties")

    c1,c2,c3 = st.columns(3)

    with c1:
        a1=st.number_input("a1",0.0,1.0,0.40)
        m1=st.number_input("m1",0.0,2.0,1.0)
        d1=st.number_input("D1 AC (cm)",0.0,100.0,5.0)

    with c2:
        a2=st.number_input("a2",0.0,1.0,0.18)
        m2=st.number_input("m2",0.0,2.0,1.1)
        d2=st.number_input("D2 Base (cm)",0.0,100.0,20.0)

    with c3:
        a3=st.number_input("a3",0.0,1.0,0.13)
        m3=st.number_input("m3",0.0,2.0,1.1)
        d3=st.number_input("D3 Subbase (cm)",0.0,100.0,25.0)

    SN1=a1*m1*(d1/2.54)
    SN2=SN1+a2*m2*(d2/2.54)
    SN3=SN2+a3*m3*(d3/2.54)

    total = d1+d2+d3

    col1,col2,col3,col4 = st.columns(4)

    col1.markdown(f'<div class="metric-box bg1">SN Required<br>{SN_req:.3f}</div>',unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-box bg2">SN Provided<br>{SN3:.3f}</div>',unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-box bg3">Total Thickness<br>{total:.1f} cm</div>',unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-box bg4">W18<br>{W18:,.0f}</div>',unsafe_allow_html=True)

    if SN3 >= SN_req:
        st.success("ผ่าน")
    else:
        st.error("ไม่ผ่าน")

    st.subheader("Summary")

    st.table({
        "Layer":["AC","Base","Subbase"],
        "Thickness (cm)":[d1,d2,d3],
        "SN":[SN1,SN2,SN3]
    })

    # ------------------------
    # CROSS SECTION (FIXED)
    # ------------------------
    st.subheader("Cross Section")

    total_thick = d1 + d2 + d3
    if total_thick == 0:
        total_thick = 1

    scale = 300 / total_thick

    html = f"""
    <div style="width:250px;margin:auto;text-align:center;">

        <div style="height:{d1*scale}px;background:#333;color:white;
        display:flex;align-items:center;justify-content:center;">
        AC {d1:.1f} cm</div>

        <div style="height:{d2*scale}px;background:#c2b280;
        display:flex;align-items:center;justify-content:center;">
        Base {d2:.1f} cm</div>

        <div style="height:{d3*scale}px;background:#8fbc8f;
        display:flex;align-items:center;justify-content:center;">
        Subbase {d3:.1f} cm</div>

        <div style="height:50px;background:#d3d3d3;
        display:flex;align-items:center;justify-content:center;">
        Subgrade</div>

    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

# ------------------------
# RIGID
# ------------------------
if road == "Rigid Pavement":

    st.title("Rigid Pavement — AASHTO 1993")

    d = st.number_input("Concrete Thickness (cm)",0.0,100.0,25.0)

    st.success(f"Thickness = {d:.1f} cm")
