import streamlit as st
import math

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="AASHTO 1993 SN Calculator",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ เครื่องคำนวณ Structural Number (SN)")
st.subheader("ตามมาตรฐาน AASHTO 1993 สำหรับผิวทางลาดยาง")

st.markdown("---")

# คำอธิบายสูตร
with st.expander("ℹ️ สูตรการคำนวณ AASHTO 1993"):
    st.latex(r'''
    \log_{10}(W_{18}) = Z_R \cdot S_0 + 9.36 \cdot \log_{10}(SN+1) - 0.20 + 
    \frac{\log_{10}\left[\frac{\Delta PSI}{4.2-1.5}\right]}{0.40 + \frac{1094}{(SN+1)^{5.19}}} + 2.32 \cdot \log_{10}(M_R) - 8.07
    ''')
    st.markdown("""
    **ตัวแปร:**
    - W₁₈ = Predicted number of 18-kip ESAL
    - Z_R = Standard normal deviate for reliability
    - S₀ = Combined standard error
    - SN = Structural Number (ค่าที่ต้องการหา)
    - ΔPSI = Difference between initial and terminal serviceability
    - M_R = Resilient Modulus of subgrade (psi)
    """)

# แบ่งคอลัมน์สำหรับ Input
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 ข้อมูลการจราจร")
    
    esal_input = st.number_input(
        "ESAL (W₁₈)",
        min_value=1000.0,
        max_value=100000000.0,
        value=5000000.0,
        step=100000.0,
        format="%.0f"
    )
    
    st.subheader("🎯 ความน่าเชื่อถือ (Reliability)")
    
    reliability_percent = st.selectbox(
        "ระดับความน่าเชื่อถือ (%)",
        options=[50, 60, 70, 75, 80, 85, 90, 95, 99, 99.9],
        index=6
    )
    
    z_r_dict = {
        50: 0.000, 60: -0.253, 70: -0.524, 75: -0.674,
        80: -0.841, 85: -1.037, 90: -1.282,
        95: -1.645, 99: -2.327, 99.9: -3.090
    }
    
    z_r = z_r_dict[reliability_percent]
    st.info(f"ค่า Z_R = {z_r}")
    
    s0 = st.number_input(
        "Overall Standard Deviation (S₀)",
        min_value=0.30,
        max_value=0.50,
        value=0.45,
        step=0.01
    )

with col2:
    st.subheader("🏗️ คุณสมบัติชั้นดิน")
    
    mr_input_type = st.radio(
        "วิธีการกรอกค่า Resilient Modulus",
        options=["ใช้ค่า M_R โดยตรง (psi)", "แปลงจากค่า CBR (%)"],
        index=1
    )
    
    if mr_input_type == "ใช้ค่า M_R โดยตรง (psi)":
        mr = st.number_input("M_R (psi)", 1000, 50000, 7500, 500)
    else:
        cbr = st.number_input("CBR (%)", 1.0, 100.0, 5.0, 0.5)
        mr = 1500 * cbr
        st.info(f"M_R = {mr:,.0f} psi")
    
    p_i = st.number_input("p_i", 3.0, 5.0, 4.2, 0.1)
    p_t = st.number_input("p_t", 1.5, 3.0, 2.5, 0.1)
    
    delta_psi = p_i - p_t
    st.info(f"ΔPSI = {delta_psi:.1f}")

st.markdown("---")

def aashto_equation(SN, W18, ZR, S0, delta_psi, MR):
    try:
        log_W18 = math.log10(W18)
        term1 = ZR * S0
        term2 = 9.36 * math.log10(SN + 1) - 0.20
        term3 = math.log10(max(delta_psi,0.01)) / (0.40 + (1094 / ((SN + 1) ** 5.19)))
        term4 = 2.32 * math.log10(MR) - 8.07
        return term1 + term2 + term3 + term4 - log_W18
    except:
        return float('inf')

def solve_for_sn(W18, ZR, S0, delta_psi, MR):
    SN = 3.0
    for _ in range(100):
        f = aashto_equation(SN, W18, ZR, S0, delta_psi, MR)
        df = (aashto_equation(SN+0.001,W18,ZR,S0,delta_psi,MR)-f)/0.001
        if abs(df) < 1e-10:
            break
        SN_new = SN - f/df
        if abs(SN_new - SN) < 0.0001:
            return SN_new
        SN = max(SN_new,0.1)
    return SN

if st.button("🔢 คำนวณ SN"):
    SN_required = solve_for_sn(esal_input, z_r, s0, delta_psi, mr)
    st.metric("SN", f"{SN_required:.2f}")

# =========================================================
# 🧱 RIGID PAVEMENT (ADD ONLY)
# =========================================================

st.markdown("---")
st.header("🧱 Rigid Pavement (Concrete)")

r_col1, r_col2 = st.columns(2)

with r_col1:
    rigid_W18 = st.number_input("ESAL (Rigid)", 1000.0, 1e8, 5e6, key="r1")
    rigid_R = st.selectbox("Reliability (Rigid)", [50,60,70,75,80,85,90,95,99,99.9], index=6, key="r2")
    
    rigid_ZR_map = {
        50: 0.000, 60: -0.253, 70: -0.524, 75: -0.674,
        80: -0.841, 85: -1.037, 90: -1.282,
        95: -1.645, 99: -2.327, 99.9: -3.090
    }
    
    rigid_ZR = rigid_ZR_map[rigid_R]
    rigid_S0 = st.number_input("S₀ (Rigid)", 0.30, 0.50, 0.35, key="r3")

with r_col2:
    rigid_k = st.number_input("k (pci)", 50, 500, 150, key="r4")
    rigid_Sc = st.number_input("S'c (psi)", 400, 1000, 650, key="r5")
    rigid_Cd = st.number_input("Cd", 0.7, 1.25, 1.0, key="r6")

def rigid_func(D,W18,ZR,S0,Sc,Cd,k):
    try:
        return ZR*S0 + 7.35*math.log10(D+1) -0.06 + (math.log10(Sc)*Cd)/(1+(1.624e7/((D+1)**8.46))) + 4.22*math.log10(k) -8.07 - math.log10(W18)
    except:
        return float('inf')

def solve_rigid(W18,ZR,S0,Sc,Cd,k):
    D=8
    for _ in range(100):
        f=rigid_func(D,W18,ZR,S0,Sc,Cd,k)
        df=(rigid_func(D+0.01,W18,ZR,S0,Sc,Cd,k)-f)/0.01
        if abs(df)<1e-6:
            break
        D_new=D-f/df
        if abs(D_new-D)<0.001:
            return D_new
        D=max(D_new,4)
    return D

if st.button("🔢 คำนวณ Rigid"):
    D = solve_rigid(rigid_W18, rigid_ZR, rigid_S0, rigid_Sc, rigid_Cd, rigid_k)
    st.metric("Thickness (inch)", f"{D:.2f}")
    st.metric("Recommended", f"{math.ceil(D)} นิ้ว")
import matplotlib.pyplot as plt
