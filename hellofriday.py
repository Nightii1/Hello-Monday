import streamlit as st

st.set_page_config(layout="wide")

st.title("📊 สรุปผลการออกแบบ (Flexible Pavement)")

# ------------------------
# INPUT
# ------------------------
SN_required = st.number_input("SN Required", value=5.240)

st.subheader("กำหนดชั้นทาง")

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

# ------------------------
# CALC SN
# ------------------------
def SN(a, m, D_cm):
    return a * m * (D_cm / 2.54)

SN1 = SN(a1, m1, D1)
SN2 = SN(a2, m2, D2)
SN3 = SN(a3, m3, D3)
SN4 = SN(a4, m4, D4)

SN_total = SN1 + SN2 + SN3 + SN4

# ------------------------
# TABLE
# ------------------------
st.subheader("📋 ตารางสรุป")

data = {
    "ชั้นที่": [1,2,3,4],
    "ชั้นทาง": ["AC","Base","Subbase","Improvement"],
    "ai": [a1,a2,a3,a4],
    "mi": [m1,m2,m3,m4],
    "ความหนา (cm)": [D1,D2,D3,D4],
    "ความหนา (inch)": [D1/2.54, D2/2.54, D3/2.54, D4/2.54],
    "SN": [SN1,SN2,SN3,SN4]
}

st.dataframe(data, use_container_width=True)

# ------------------------
# RESULT
# ------------------------
if SN_total >= SN_required:
    st.success(f"SN = {SN_total:.3f} ≥ {SN_required} (ผ่าน)")
else:
    st.error(f"SN = {SN_total:.3f} < {SN_required} (ไม่ผ่าน)")

# ------------------------
# SECTION (ใช้ Streamlit ล้วน)
# ------------------------
st.subheader("🏗️ หน้าตัดโครงสร้างทาง")

max_val = max(D1, D2, D3, D4, 1)

st.write("AC")
st.progress(D1 / max_val)
st.write(f"{D1:.1f} cm")

st.write("Base")
st.progress(D2 / max_val)
st.write(f"{D2:.1f} cm")

st.write("Subbase")
st.progress(D3 / max_val)
st.write(f"{D3:.1f} cm")

st.write("Improvement")
st.progress(D4 / max_val)
st.write(f"{D4:.1f} cm")

st.write("Subgrade")
st.progress(0.3)
