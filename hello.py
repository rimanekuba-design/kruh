import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(page_title="Body na kružnici", page_icon="⭕")

st.title("Body na kružnici")

# --- Vstupy ---
st.sidebar.header("Parametry")
x0 = st.sidebar.number_input("Souřadnice středu X", value=0.0)
y0 = st.sidebar.number_input("Souřadnice středu Y", value=0.0)
r = st.sidebar.number_input("Poloměr (m)", min_value=0.1, value=5.0)
n = st.sidebar.number_input("Počet bodů", min_value=1, value=8)
barva = st.sidebar.color_picker("Barva bodů", "#ff0000")

# --- Výpočet souřadnic ---
angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x_points = x0 + r * np.cos(angles)
y_points = y0 + r * np.sin(angles)

# --- Vykreslení ---
fig, ax = plt.subplots()
circle = plt.Circle((x0, y0), r, color="blue", fill=False, linestyle="--")
ax.add_artist(circle)
ax.scatter(x_points, y_points, color=barva, label="Body na kružnici")
for i, (x, y) in enumerate(zip(x_points, y_points), 1):
    ax.text(x, y, str(i), fontsize=8, ha="right")

ax.set_aspect("equal")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.grid(True)
st.pyplot(fig)

# --- Informace ---
st.sidebar.markdown("---")
st.sidebar.subheader("Informace o autorovi")
st.sidebar.write("**Autor:** Jakub Říman")  
st.sidebar.write("**Kontakt:** 278331@vutbr.cz")  
st.sidebar.write("**Technologie:** Python, Streamlit, Matplotlib, ReportLab")

# --- Export do PDF ---
def create_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Body na kružnici – Výstup", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Střed: ({x0}, {y0})", styles["Normal"]))
    story.append(Paragraph(f"Poloměr: {r} m", styles["Normal"]))
    story.append(Paragraph(f"Počet bodů: {n}", styles["Normal"]))
    story.append(Paragraph(f"Barva bodů: {barva}", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Autor: Jakub Říman", styles["Normal"]))
    story.append(Paragraph("Kontakt: 278331@vutbr.cz", styles["Normal"]))
    doc.build(story)
    buffer.seek(0)
    return buffer

if st.button("📄 Exportovat do PDF"):
    pdf_bytes = create_pdf()
    st.download_button(
        label="Stáhnout PDF",
        data=pdf_bytes,
        file_name="body_na_kruznici.pdf",
        mime="application/pdf"
    )

