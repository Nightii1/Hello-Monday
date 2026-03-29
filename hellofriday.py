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
import numpy as np

st.set_page_config(layout="wide")

st.title("📊 สรุปผลการออกแบบ (ชั้นทาง)")

# ------------------------
# INPUT
# ------------------------
W18 = st.number_input("W18", value=10000000.0)
SN_required = 5.240

# Layer data (แก้ค่าได้)
layers = [
    {"name":"AC", "a":0.40, "m":1.10, "D_cm":20.3},
    {"name":"CTBAC", "a":0.18, "m":1.10, "D_cm":22.2},
    {"name":"Subbase", "a":0.13, "m":1.10, "D_cm":10.2},
    {"name":"Subgrade Improvement", "a":0.10, "m":1.10, "D_cm":10.2},
]

# ------------------------
# CALC SN
# ------------------------
SN_list = []
SN_total = 0

for layer in layers:
    D_in = layer["D_cm"]/2.54
    SN = layer["a"] * layer["m"] * D_in
    SN_total += SN
    SN_list.append(SN)

# ------------------------
# TABLE
# ------------------------
st.subheader("📋 ตารางสรุป")

table_data = []

for i, layer in enumerate(layers):
    table_data.append({
        "ชั้นที่": i+1,
        "ชั้นทาง": layer["name"],
        "ai": layer["a"],
        "mi": layer["m"],
        "ความหนา (cm)": layer["D_cm"],
        "ความหนา (inch)": layer["D_cm"]/2.54,
        "SN": round(SN_list[i],3)
    })

st.dataframe(table_data, use_container_width=True)

# ------------------------
# RESULT
# ------------------------
if SN_total >= SN_required:
    st.success(f"SN = {SN_total:.3f} ≥ {SN_required} (ผ่าน)")
else:
    st.error(f"SN = {SN_total:.3f} < {SN_required} (ไม่ผ่าน)")

# ------------------------
# SECTION (เหมือนรูปจริง)
# ------------------------
st.subheader("🏗️ หน้าตัดโครงสร้างทาง")

colors = ["#222222","#6b8e9e","#8b6b43","#d4a017"]

total = sum([l["D_cm"] for l in layers])
scale = 400 / total

html = '<div style="width:300px;margin:auto;border:2px solid #ccc;">'

for i, layer in enumerate(layers):
    h = layer["D_cm"] * scale
    html += f'''
    <div style="
        height:{h}px;
        background:{colors[i]};
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
        font-weight:bold;
        border-bottom:1px solid #000;">
        {layer["D_cm"]:.1f} cm
    </div>
    '''

# subgrade
html += '''
<div style="
    height:80px;
    background:#704214;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-weight:bold;">
    Subgrade
</div>
'''

html += '</div>'

st.markdown(html, unsafe_allow_html=True)
