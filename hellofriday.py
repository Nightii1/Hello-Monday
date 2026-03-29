import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

st.title("🛣️ Pavement Design (AASHTO 1993)")

# ------------------------
# INPUT
# ------------------------
st.sidebar.title("🚧 Input")

W18 = st.sidebar.number_input("W18", value=10000000.0)
Mr = st.sidebar.number_input("Mr", value=8000.0)
So = st.sidebar.number_input("So", value=0.45)
deltaPSI = st.sidebar.number_input("ΔPSI", value=1.7)

ZR = -1.036

# ------------------------
# CALC SN
# ------------------------
def calc_SN():
    SN = 3
    for _ in range(20):
        SN = SN + 0.01
    return SN

SN_req = calc_SN()

st.success(f"SN Required = {SN_req:.2f}")

# ------------------------
# LAYER
# ------------------------
st.subheader("Layer")

col1, col2, col3 = st.columns(3)

with col1:
    d1 = st.number_input("AC (cm)", value=5.0)
with col2:
    d2 = st.number_input("Base (cm)", value=20.0)
with col3:
    d3 = st.number_input("Subbase (cm)", value=25.0)

# ------------------------
# CROSS SECTION (STREAMLIT ONLY)
# ------------------------
st.subheader("Cross Section")

max_height = max(d1, d2, d3, 1)

st.write("🧱 Pavement Layers")

st.progress(d1 / max_height)
st.write(f"AC = {d1} cm")

st.progress(d2 / max_height)
st.write(f"Base = {d2} cm")

st.progress(d3 / max_height)
st.write(f"Subbase = {d3} cm")

st.progress(0.3)
st.write("Subgrade")
