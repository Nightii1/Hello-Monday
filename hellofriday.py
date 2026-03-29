import streamlit as st
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(layout="wide")

# ------------------------
# LOGO + HEADER
# ------------------------
col1, col2 = st.columns([1,5])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/th/5/5c/KMUTNB_logo.png", width=80)

with col2:
    st.title("📊 Pavement Design Dashboard")
    st.caption("AASHTO 1993 | KMUTNB Engineering Tool")

# ------------------------
# TABS
# ------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Design",
    "📘 Theory",
    "📈 Sensitivity",
    "🚀 Report & Dashboard"
])

# =========================================================
# TAB 1
# =========================================================
with tab1:

    st.sidebar.header("🔧 Input")

    mode = st.sidebar.radio("Type", ["Flexible", "Rigid"])

    W18 = st.sidebar.number_input("W18", value=5000000.0)

    if mode == "Rigid":

        k = st.sidebar.number_input("k", value=50.0)
        k_base = st.sidebar.number_input("Base", value=50.0)
        Sc = st.sidebar.number_input("Sc", value=650.0)

        k_eff = k + k_base

        d = max(((W18/1e6)**0.25)*(100/k_eff)**0.1*(650/Sc)**0.2*8,5)
        d_cm = d*2.54

        st.metric("Thickness (cm)", f"{d_cm:.2f}")

        st.progress(min(d_cm/50,1.0))

        st.subheader("Cross Section")

        st.markdown(f"""
        <div style="width:300px;margin:auto;">
        <div style="height:{d_cm*4}px;background:#6C757D;color:white;text-align:center;">
        Concrete {d_cm:.1f} cm
        </div>
        <div style="height:80px;background:#7F5539;color:white;text-align:center;">
        Subgrade
        </div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAB 2
# =========================================================
with tab2:
    st.latex(r"\log_{10}(W_{18}) = Z_R S_o + 7.35\log(D+1)")

# =========================================================
# TAB 3
# =========================================================
with tab3:

    W = np.linspace(1e5,1e7,50)
    d = ((W/1e6)**0.25)*8*2.54

    st.line_chart({"Thickness": d})

# =========================================================
# TAB 4 (🔥 PRO)
# =========================================================
with tab4:

    st.header("📄 Professional Report")

    W_test = st.number_input("W18 Report", value=5000000.0)

    d_opt = ((W_test/1e6)**0.25)*8*2.54

    st.metric("Recommended Thickness", f"{d_opt:.2f} cm")

    # -------- PDF --------
    def create_pdf():
        doc = SimpleDocTemplate("pavement_report.pdf")
        styles = getSampleStyleSheet()

        story = []

        story.append(Paragraph("PAVEMENT DESIGN REPORT", styles["Title"]))
        story.append(Spacer(1,12))

        story.append(Paragraph(f"W18: {W_test:,.0f}", styles["Normal"]))
        story.append(Paragraph(f"Thickness: {d_opt:.2f} cm", styles["Normal"]))
        story.append(Paragraph("Method: AASHTO 1993", styles["Normal"]))

        doc.build(story)

    if st.button("📥 Generate PDF"):
        create_pdf()
        with open("pavement_report.pdf","rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="report.pdf")

    st.success("✔ Dashboard Ready for Presentation")
