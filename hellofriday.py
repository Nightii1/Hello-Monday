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
    
    # ESAL Input
    esal_input = st.number_input(
        "ESAL (W₁₈)",
        min_value=1000.0,
        max_value=100000000.0,
        value=5000000.0,
        step=100000.0,
        format="%.0f",
        help="Equivalent Single Axle Load (18-kip)"
    )
    
    st.subheader("🎯 ความน่าเชื่อถือ (Reliability)")
    
    # Reliability Selection
    reliability_percent = st.selectbox(
        "ระดับความน่าเชื่อถือ (%)",
        options=[50, 60, 70, 75, 80, 85, 90, 95, 99, 99.9],
        index=6,  # default 90%
        help="เลือกตามประเภทถนน: ทางหลวง 85-99.9%, ทางรอง 80-95%"
    )
    
    # Z_R values based on reliability
    z_r_dict = {
        50: 0.000,
        60: -0.253,
        70: -0.524,
        75: -0.674,
        80: -0.841,
        85: -1.037,
        90: -1.282,
        95: -1.645,
        99: -2.327,
        99.9: -3.090
    }
    
    z_r = z_r_dict[reliability_percent]
    st.info(f"ค่า Z_R = {z_r}")
    
    # Standard Error
    s0 = st.number_input(
        "Overall Standard Deviation (S₀)",
        min_value=0.30,
        max_value=0.50,
        value=0.45,
        step=0.01,
        help="ค่าปกติอยู่ระหว่าง 0.40-0.50 สำหรับผิวทางแอสฟัลต์"
    )

with col2:
    st.subheader("🏗️ คุณสมบัติชั้นดิน")
    
    # Resilient Modulus Input with options
    mr_input_type = st.radio(
        "วิธีการกรอกค่า Resilient Modulus",
        options=["ใช้ค่า M_R โดยตรง (psi)", "แปลงจากค่า CBR (%)"],
        index=1
    )
    
    if mr_input_type == "ใช้ค่า M_R โดยตรง (psi)":
        mr = st.number_input(
            "Resilient Modulus (M_R) - psi",
            min_value=1000,
            max_value=50000,
            value=7500,
            step=500,
            help="ค่า M_R ของชั้นดินเดิม"
        )
    else:
        cbr = st.number_input(
            "CBR (%)",
            min_value=1.0,
            max_value=100.0,
            value=5.0,
            step=0.5,
            help="California Bearing Ratio"
        )
        # สูตรแปลง CBR เป็น M_R (AASHTO)
        mr = 1500 * cbr
        st.info(f"M_R คำนวณได้ = {mr:,.0f} psi")
    
    st.subheader("📉 การสูญเสียความสามารถในการให้บริการ")
    
    # Initial PSI
    p_i = st.number_input(
        "Initial Serviceability Index (p_i)",
        min_value=3.0,
        max_value=5.0,
        value=4.2,
        step=0.1,
        help="ค่าปกติสำหรับผิวทางใหม่ = 4.2"
    )
    
    # Terminal PSI
    p_t = st.number_input(
        "Terminal Serviceability Index (p_t)",
        min_value=1.5,
        max_value=3.0,
        value=2.5,
        step=0.1,
        help="ค่าปกติสำหรับทางหลวง = 2.5, ทางรอง = 2.0"
    )
    
    delta_psi = p_i - p_t
    st.info(f"ΔPSI = {delta_psi:.1f}")

st.markdown("---")

# ฟังก์ชันสำหรับแก้สมการ AASHTO
def aashto_equation(SN, W18, ZR, S0, delta_psi, MR):
    """
    AASHTO 1993 equation for flexible pavement design
    Returns the difference (should be zero when solved)
    """
    try:
        log_W18 = math.log10(W18)
        
        term1 = ZR * S0
        term2 = 9.36 * math.log10(SN + 1) - 0.20
        
        # Calculate ΔPSI term carefully
        psi_ratio = delta_psi / 4.2 - 1.5
        if psi_ratio <= 0:
            psi_ratio = 0.001
        term3_numerator = math.log10(psi_ratio)
        term3_denominator = 0.40 + (1094 / ((SN + 1) ** 5.19))
        term3 = term3_numerator / term3_denominator
        
        term4 = 2.32 * math.log10(MR) - 8.07
        
        result = term1 + term2 + term3 + term4
        
        return result - log_W18
    except:
        return float('inf')

def solve_for_sn(W18, ZR, S0, delta_psi, MR, initial_guess=3.0, tolerance=0.0001, max_iterations=100):
    """
    Newton-Raphson method to solve for SN
    """
    SN = initial_guess
    
    for i in range(max_iterations):
        f = aashto_equation(SN, W18, ZR, S0, delta_psi, MR)
        
        # Calculate derivative numerically
        h = 0.001
        f_plus = aashto_equation(SN + h, W18, ZR, S0, delta_psi, MR)
        df = (f_plus - f) / h
        
        if abs(df) < 1e-10:
            break
            
        # Newton-Raphson update
        SN_new = SN - f / df
        
        # Check convergence
        if abs(SN_new - SN) < tolerance:
            return SN_new
            
        SN = SN_new
        
        # Keep SN positive
        if SN < 0:
            SN = 0.1
    
    return SN

# ปุ่มคำนวณ
if st.button("🔢 คำนวณ Structural Number (SN)", type="primary", use_container_width=True):
    try:
        # แก้สมการเพื่อหา SN
        SN_required = solve_for_sn(esal_input, z_r, s0, delta_psi, mr)
        
        # แสดงผลลัพธ์
        st.success("✅ คำนวณสำเร็จ!")
        
        # ผลลัพธ์หลัก
        st.markdown("---")
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            st.metric(
                label="Structural Number ที่ต้องการ",
                value=f"{SN_required:.2f}",
                help="ค่า SN ขั้นต่ำที่ต้องใช้"
            )
        
        with result_col2:
            st.metric(
                label="SN (ปัดขึ้น)",
                value=f"{math.ceil(SN_required * 2) / 2:.1f}",
                help="ปัดขึ้นเป็น 0.5"
            )
        
        with result_col3:
            reliability_color = "🟢" if reliability_percent >= 90 else "🟡" if reliability_percent >= 80 else "🔴"
            st.metric(
                label="ระดับความน่าเชื่อถือ",
                value=f"{reliability_color} {reliability_percent}%"
            )
        
        # สรุปข้อมูลที่ใช้คำนวณ
        st.markdown("---")
        st.subheader("📋 สรุปข้อมูลที่ใช้ในการคำนวณ")
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown(f"""
            **ข้อมูลการจราจร:**
            - ESAL (W₁₈): {esal_input:,.0f}
            - Reliability: {reliability_percent}% (Z_R = {z_r})
            - Overall Std Dev (S₀): {s0}
            """)
        
        with summary_col2:
            st.markdown(f"""
            **ข้อมูลชั้นดินและการบริการ:**
            - Resilient Modulus (M_R): {mr:,.0f} psi
            - Initial PSI (p_i): {p_i}
            - Terminal PSI (p_t): {p_t}
            - ΔPSI: {delta_psi:.1f}
            """)
        
        # คำแนะนำการออกแบบชั้นทาง
        st.markdown("---")
        st.subheader("💡 คำแนะนำการออกแบบชั้นทาง")
        
        # คำนวณตัวอย่างความหนาชั้นทาง
        asphalt_thickness = (SN_required / 3) / 0.44
        base_thickness = (SN_required / 3) / 0.14
        subbase_thickness = (SN_required / 3) / 0.11
        
        st.info(f"""
        **สำหรับ SN = {SN_required:.2f}** คุณสามารถออกแบบชั้นทางได้หลายแบบ เช่น:
        
        **ตัวอย่างการออกแบบ (ใช้ค่า layer coefficient มาตรฐาน):**
        - ชั้นผิว Asphalt Concrete (a₁ = 0.44): D₁ ≈ {asphalt_thickness:.1f} นิ้ว
        - ชั้นฐาน Base Course (a₂ = 0.14, m₂ = 1.0): D₂ ≈ {base_thickness:.1f} นิ้ว  
        - ชั้นรอง Subbase (a₃ = 0.11, m₃ = 1.0): D₃ ≈ {subbase_thickness:.1f} นิ้ว
        
        **หมายเหตุ:** สูตร SN = a₁D₁ + a₂D₂m₂ + a₃D₃m₃
        - a = layer coefficient (ค่าสัมประสิทธิ์ชั้นทาง)
        - D = ความหนาชั้นทาง (นิ้ว)
        - m = drainage coefficient (ค่าสัมประสิทธิ์การระบายน้ำ)
        """)
        
        # แสดงตัวอย่างการออกแบบที่เป็นไปได้
        st.subheader("🏗️ ตัวอย่างการออกแบบชั้นทางที่เป็นไปได้")
        
        design_col1, design_col2 = st.columns(2)
        
        with design_col1:
            st.markdown("**แบบที่ 1: Thick Asphalt**")
            d1_opt1 = 5.0
            sn1_opt1 = 0.44 * d1_opt1
            remaining_sn1 = SN_required - sn1_opt1
            d2_opt1 = (remaining_sn1 / 2) / 0.14
            d3_opt1 = (remaining_sn1 / 2) / 0.11
            
            st.markdown(f"""
            - Asphalt: {d1_opt1:.1f} นิ้ว
            - Base: {d2_opt1:.1f} นิ้ว
            - Subbase: {d3_opt1:.1f} นิ้ว
            - **SN รวม: {(0.44*d1_opt1 + 0.14*d2_opt1 + 0.11*d3_opt1):.2f}**
            """)
        
        with design_col2:
            st.markdown("**แบบที่ 2: Balanced Design**")
            d1_opt2 = 3.5
            sn1_opt2 = 0.44 * d1_opt2
            remaining_sn2 = SN_required - sn1_opt2
            d2_opt2 = (remaining_sn2 * 0.6) / 0.14
            d3_opt2 = (remaining_sn2 * 0.4) / 0.11
            
            st.markdown(f"""
            - Asphalt: {d1_opt2:.1f} นิ้ว
            - Base: {d2_opt2:.1f} นิ้ว
            - Subbase: {d3_opt2:.1f} นิ้ว
            - **SN รวม: {(0.44*d1_opt2 + 0.14*d2_opt2 + 0.11*d3_opt2):.2f}**
            """)
        
        # คำเตือน
        if SN_required > 6:
            st.warning("⚠️ SN ที่คำนวณได้สูงมาก อาจต้องพิจารณาปรับปรุงชั้นดินเดิมหรือใช้วัสดุคุณภาพสูง")
        elif SN_required < 2:
            st.warning("⚠️ SN ที่คำนวณได้ต่ำมาก กรุณาตรวจสอบข้อมูลที่ป้อนให้ถูกต้อง")
            
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการคำนวณ: {str(e)}")
        st.info("กรุณาตรวจสอบข้อมูลที่ป้อนและลองใหม่อีกครั้ง")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📚 อ้างอิง: AASHTO Guide for Design of Pavement Structures, 1993</p>
    <p>⚠️ โปรแกรมนี้เป็นเครื่องมือช่วยคำนวณเบื้องต้น ควรตรวจสอบโดยวิศวกรผู้เชี่ยวชาญก่อนนำไปใช้งานจริง</p>
</div>
""", unsafe_allow_html=True)
        """)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
