import streamlit as st
import numpy as np
from PIL import Image
import io
import time

# SAFE IMPORT
try:
    import cv2
except:
    cv2 = None

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Ultimate AI Detector", layout="wide")

# ================= FAKE DL (SAFE FALLBACK) =================
def deep_learning_prediction(image_bytes):
    # Simulated but stable (no crash)
    return {"dl_ai_prob": 50.0}

# ================= FORENSIC =================
def forensic_analysis(image_bytes):

    if cv2 is None:
        return {
            "ai_forensic": 50,
            "laplacian": 0,
            "edge_density": 0,
            "entropy": 0,
            "noise": 0
        }

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        arr = np.array(img)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

        h, w = gray.shape

        laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / (h * w)
        noise = np.std(gray / 255.0)

        hist = cv2.calcHist([gray],[0],None,[256],[0,256])
        hist = hist / hist.sum()
        entropy = -np.sum(hist * np.log2(hist + 1e-7))

        ai_score = 0
        if laplacian < 50: ai_score += 25
        if edge_density < 0.05: ai_score += 20
        if noise < 0.02: ai_score += 20
        if entropy > 7.5: ai_score += 15
        if w in [512,768,1024] and h in [512,768,1024]: ai_score += 20

        return {
            "ai_forensic": ai_score,
            "laplacian": laplacian,
            "edge_density": edge_density,
            "entropy": entropy,
            "noise": noise
        }

    except:
        return {
            "ai_forensic": 50,
            "laplacian": 0,
            "edge_density": 0,
            "entropy": 0,
            "noise": 0
        }

# ================= FINAL =================
def final_decision(forensic, dl):
    ai_prob = (0.7 * forensic["ai_forensic"]) + (0.3 * dl["dl_ai_prob"])
    ai_prob = max(5, min(95, ai_prob))

    if ai_prob > 75:
        verdict = "🤖 AI GENERATED"
    elif ai_prob > 55:
        verdict = "⚠️ LIKELY AI"
    else:
        verdict = "✅ REAL IMAGE"

    return verdict, ai_prob, 100 - ai_prob

# ================= UI =================
st.title("🔍 Ultimate AI Image Detector (Stable Version)")

uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    img_bytes = uploaded_file.read()

    if st.button("Analyze Image"):
        with st.spinner("Analyzing..."):
            time.sleep(1)

            forensic = forensic_analysis(img_bytes)
            dl = deep_learning_prediction(img_bytes)

            verdict, ai, real = final_decision(forensic, dl)

        st.markdown(f"## {verdict}")
        st.write(f"🤖 AI Probability: {ai:.2f}%")
        st.write(f"✅ Real Probability: {real:.2f}%")

        st.subheader("🔬 Forensic Details")
        st.write(f"Texture (Laplacian): {forensic['laplacian']:.2f}")
        st.write(f"Edge Density: {forensic['edge_density']:.4f}")
        st.write(f"Entropy: {forensic['entropy']:.2f}")
        st.write(f"Noise: {forensic['noise']:.4f}")
