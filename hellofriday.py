st.subheader("🧱 Pavement Section")

total = D1 + D2 + D3
if total == 0:
    total = 1

scale = 300 / total

h1 = D1 * scale
h2 = D2 * scale
h3 = D3 * scale

html = f"""
<div style="width:300px; margin:auto; font-family:sans-serif;">

    <div style="height:{h1}px;background:#2b2b2b;border:2px solid black;
    display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;">
    Asphalt {D1:.1f} in</div>

    <div style="height:{h2}px;background:#c2b280;border:2px solid black;
    display:flex;align-items:center;justify-content:center;font-weight:bold;">
    Base {D2:.1f} in</div>

    <div style="height:{h3}px;background:#8fbc8f;border:2px solid black;
    display:flex;align-items:center;justify-content:center;font-weight:bold;">
    Subbase {D3:.1f} in</div>

    <div style="height:60px;background:#d3d3d3;border:2px solid black;
    display:flex;align-items:center;justify-content:center;font-weight:bold;">
    Subgrade</div>

</div>
"""

st.markdown(html, unsafe_allow_html=True)
