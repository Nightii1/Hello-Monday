import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

# =========================
# HEADER + LOGO
# =========================
col1, col2 = st.columns([1,5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/th/5/5c/KMUTNB_logo.png", width=80)
with col2:
    st.title("📊 Pavement Design Dashboard")
    st.caption("AASHTO 1993 | Civil Engineering Tool")

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Design",
    "📘 Theory",
    "📈 Sensitivity",
    "📄 Report (PDF)"
])

# =========================
# TAB 1: DESIGN
# =========================
with tab1:

    st.sidebar.header("🔧 Input")

    mode = st.sidebar.radio("Type", ["Flexible", "Rigid"])
    W18 = st.sidebar.number_input("W18", value=5000000.0)

    if mode == "Rigid":

        k = st.sidebar.number_input("k (pci)", value=50.0)
        k_base = st.sidebar.number_input("Base improvement (pci)", value=50.0)
        Sc = st.sidebar.number_input("S'c (psi)", value=650.0)

        k_eff = k + k_base

        d_in = max(((W18/1e6)**0.25)*(100/k_eff)**0.1*(650/Sc)**0.2*8,5)
        d_cm = d_in * 2.54

        st.metric("Concrete Thickness", f"{d_cm:.2f} cm")

        st.progress(min(d_cm/50,1.0))

        st.subheader("🏗️ Cross Section")

        st.markdown(f"""
        <div style="width:300px;margin:auto;border-radius:12px;overflow:hidden;">
            <div style="height:{d_cm*4}px;background:#495057;color:white;display:flex;align-items:center;justify-content:center;">
                Concrete {d_cm:.1f} cm
            </div>
            <div style="height:80px;background:#7F5539;color:white;display:flex;align-items:center;justify-content:center;">
                Subgrade (k={k})
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# TAB 2: THEORY
# =========================
with tab2:
    st.header("📘 AASHTO Equation")
    st.latex(r"\log_{10}(W_{18}) = Z_R S_o + 7.35\log(D+1)")

# =========================
# TAB 3: SENSITIVITY
# =========================
with tab3:
    st.header("📈 Sensitivity")

    W = np.linspace(1e5,1e7,50)
    d = ((W/1e6)**0.25)*8*2.54

    st.line_chart({"Thickness (cm)": d})

# =========================
# TAB 4: REPORT (🔥 PDF READY)
# =========================
with tab4:

    st.header("📄 Professional Report")

    W_test = st.number_input("W18 (Report)", value=5000000.0)
    d_opt = ((W_test/1e6)**0.25)*8*2.54

    st.success(f"Recommended Thickness = {d_opt:.2f} cm")

    # -------- HTML REPORT --------
    report_html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Arial; padding:40px; }}
        h1 {{ color:#1d3557; }}
        .box {{ border:1px solid #ccc; padding:20px; border-radius:10px; }}
    </style>
    </head>
    <body>

    <h1>📊 Pavement Design Report</h1>
    <div class="box">
        <p><b>Traffic (W18):</b> {W_test:,.0f}</p>
        <p><b>Recommended Thickness:</b> {d_opt:.2f} cm</p>
        <p><b>Method:</b> AASHTO 1993</p>
        <p><b>Status:</b> ✅ Design OK</p>
    </div>

    <br>
    <p>KMUTNB Civil Engineering</p>

    </body>
    </html>
    """

    st.markdown(report_html, unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download Report (Open & Save as PDF)",
        report_html,
        file_name="pavement_report.html",
        mime="text/html"
    )

    st.info("👉 เปิดไฟล์ → กด Ctrl+P → Save as PDF")
