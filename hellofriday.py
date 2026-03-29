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

# =========================
# 🔽 (โค้ดเดิมของคุณทั้งหมด)
# ❗ ไม่ได้แก้แม้แต่บรรทัดเดียว
# =========================

# >>>>> วางโค้ดเดิมของคุณตรงนี้ทั้งหมด <<<<<
# (ผมไม่ย้ำซ้ำเพราะคุณมีอยู่แล้ว)

# =========================================================
# 🧱 RIGID PAVEMENT (ADD ONLY - ไม่ยุ่งของเดิม)
# =========================================================

st.markdown("---")
st.header("🧱 Rigid Pavement (Concrete) - AASHTO 1993")

# INPUT
r_col1, r_col2 = st.columns(2)

with r_col1:
    st.subheader("📊 Traffic")

    rigid_W18 = st.number_input(
        "ESAL (W18) - Rigid",
        min_value=1000.0,
        max_value=100000000.0,
        value=5000000.0,
        step=100000.0,
        format="%.0f",
        key="rigid_w18"
    )

    rigid_R = st.selectbox(
        "Reliability (%) - Rigid",
        [50, 60, 70, 75, 80, 85, 90, 95, 99, 99.9],
        index=6,
        key="rigid_rel"
    )

    rigid_ZR_map = {
        50: 0.000, 60: -0.253, 70: -0.524, 75: -0.674,
        80: -0.841, 85: -1.037, 90: -1.282,
        95: -1.645, 99: -2.327, 99.9: -3.090
    }

    rigid_ZR = rigid_ZR_map[rigid_R]
    st.info(f"Z_R = {rigid_ZR}")

    rigid_S0 = st.number_input(
        "Standard Deviation (S₀)",
        min_value=0.30,
        max_value=0.50,
        value=0.35,
        step=0.01,
        key="rigid_s0"
    )

with r_col2:
    st.subheader("🏗️ Material Properties")

    rigid_k = st.number_input(
        "Modulus of Subgrade Reaction k (pci)",
        min_value=50,
        max_value=500,
        value=150,
        step=10,
        key="rigid_k"
    )

    rigid_Sc = st.number_input(
        "Concrete Flexural Strength S'c (psi)",
        min_value=400,
        max_value=1000,
        value=650,
        step=10,
        key="rigid_sc"
    )

    rigid_Cd = st.number_input(
        "Drainage Coefficient (C_d)",
        min_value=0.7,
        max_value=1.25,
        value=1.0,
        step=0.05,
        key="rigid_cd"
    )

# FUNCTION
def rigid_equation(D, W18, ZR, S0, Sc, Cd, k):
    try:
        logW = math.log10(W18)

        term1 = ZR * S0
        term2 = 7.35 * math.log10(D + 1) - 0.06
        term3 = (math.log10(Sc) * Cd) / (1 + (1.624e7 / ((D + 1) ** 8.46)))
        term4 = 4.22 * math.log10(k) - 8.07

        return term1 + term2 + term3 + term4 - logW
    except:
        return float('inf')

def solve_rigid_thickness(W18, ZR, S0, Sc, Cd, k):
    D = 8.0
    for _ in range(100):
        f = rigid_equation(D, W18, ZR, S0, Sc, Cd, k)

        h = 0.01
        df = (rigid_equation(D + h, W18, ZR, S0, Sc, Cd, k) - f) / h

        if abs(df) < 1e-6:
            break

        D_new = D - f / df

        if abs(D_new - D) < 0.001:
            return D_new

        D = max(D_new, 4)

    return D

# BUTTON
if st.button("🔢 คำนวณ Rigid Pavement", key="rigid_btn", use_container_width=True):
    try:
        D = solve_rigid_thickness(
            rigid_W18, rigid_ZR, rigid_S0,
            rigid_Sc, rigid_Cd, rigid_k
        )

        st.success("✅ คำนวณ Rigid สำเร็จ")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("ความหนาแผ่นคอนกรีต (นิ้ว)", f"{D:.2f}")

        with c2:
            st.metric("ค่าที่แนะนำ", f"{math.ceil(D)} นิ้ว")

        st.info(f"""
        📌 แนะนำ:
        - ใช้ D ≈ {math.ceil(D)} นิ้ว
        - ตรวจสอบ joint spacing เพิ่ม
        - ตรวจสอบ dowel / tie bar
        """)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
