import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

st.title("📊 Pavement Design (AASHTO 1993)")

# ------------------------
# INPUT
# ------------------------
W18 = st.number_input("W18", value=10000000.0)
SN_required = 5.240

layers = [
    {"name":"AC", "a":0.40, "m":1.10, "D_cm":20.3},
    {"name":"CTBAC", "a":0.18, "m":1.10, "D_cm":22.2},
    {"name":"Subbase", "a":0.13, "m":1.10, "D_cm":10.2},
    {"name":"Improvement", "a":0.10, "m":1.10, "D_cm":10.2},
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
        "Layer": layer["name"],
        "Thickness (cm)": layer["D_cm"],
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
# SECTION (แก้สมบูรณ์)
# ------------------------
st.subheader("🏗️ หน้าตัดโครงสร้างทาง")

colors = ["#222222","#6b8e9e","#8b6b43","#d4a017"]

total = sum([l["D_cm"] for l in layers])
if total == 0:
    total = 1

scale = 400 / total

html = '<div style="display:flex; justify-content:center;">'
html += '<div style="width:260px; border:2px solid #ccc;">'

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
        font-weight:bold;">
        {layer["D_cm"]:.1f} cm
    </div>
    '''

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

html += '</div></div>'

st.markdown(html, unsafe_allow_html=True)
