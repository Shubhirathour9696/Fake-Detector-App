import streamlit as st
import numpy as np
from PIL import Image
import io
import time
import joblib

# Safe import
try:
    import cv2
except:
    cv2 = None

# ================= LOAD ML MODEL =================
@st.cache_resource
def load_model():
    try:
        return joblib.load("ai_model.pkl")
    except:
        return None

model = load_model()

# ================= FEATURE EXTRACTION =================
def extract_features(image_bytes):
    if cv2 is None:
        return [50, 0.05, 7.0, 0.02]

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

        return [laplacian, edge_density, entropy, noise]

    except:
        return [50, 0.05, 7.0, 0.02]

# ================= ML PREDICTION =================
def ml_prediction(features):
    if model is None:
        return 50.0

    try:
        pred = model.predict_proba([features])[0][1]
        return float(pred * 100)
    except:
        return 50.0

# ================= FINAL DECISION =================
def final_decision(ai_prob):
    ai_prob = max(5, min(95, ai_prob))

    if ai_prob > 75:
        verdict = "🤖 AI GENERATED"
    elif ai_prob > 55:
        verdict = "⚠️ LIKELY AI"
    else:
        verdict = "✅ REAL IMAGE"

    return verdict, ai_prob, 100 - ai_prob

# ================= UI =================
st.title("🔍 AI Image Detector (ML Version)")

uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    img_bytes = uploaded_file.read()

    if st.button("Analyze Image"):
        with st.spinner("Analyzing..."):
            time.sleep(1)

            features = extract_features(img_bytes)
            ai_prob = ml_prediction(features)

            verdict, ai, real = final_decision(ai_prob)

        st.markdown(f"## {verdict}")
        st.write(f"🤖 AI Probability: {ai:.2f}%")
        st.write(f"✅ Real Probability: {real:.2f}%")

        st.subheader("🔬 Extracted Features")
        st.write(f"Laplacian: {features[0]:.2f}")
        st.write(f"Edge Density: {features[1]:.4f}")
        st.write(f"Entropy: {features[2]:.2f}")
        st.write(f"Noise: {features[3]:.4f}")
        
