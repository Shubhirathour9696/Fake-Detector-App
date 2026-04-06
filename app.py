import streamlit as st
import numpy as np
from PIL import Image
import io
import hashlib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ML
from sklearn.linear_model import LogisticRegression

# Page config
st.set_page_config(page_title="Ultimate Detector v3.0", layout="wide")

# -------------------------------
# 🔬 IMAGE ANALYSIS
# -------------------------------
@st.cache_data
def analyze_image(_img_bytes):
    img = Image.open(io.BytesIO(_img_bytes)).convert('RGB')
    img_array = np.array(img, dtype=np.float32) / 255.0
    
    gray = np.mean(img_array, axis=2)
    
    # Entropy
    flat = img_array.flatten()
    hist, _ = np.histogram(flat, bins=256, density=True)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist + 1e-12))
    
    # Laplacian variance
    lap_var = np.var(np.gradient(np.gradient(gray)))
    
    # Edge sharpness
    edges = np.sqrt(np.diff(gray, axis=1, append=0)**2 + np.diff(gray, axis=0, append=0)**2)
    edge = np.mean(edges)
    
    # Noise
    noise = np.std(np.diff(gray.flatten()))
    
    # Color balance
    color_std = np.std(img_array, axis=(0,1))
    color_balance = np.min(color_std) / (np.max(color_std) + 1e-8)
    
    return {
        "entropy": entropy,
        "laplacian": lap_var,
        "edge": edge,
        "noise": noise,
        "color": color_balance,
        "width": img.width,
        "height": img.height
    }

# -------------------------------
# 🤖 ML MODEL
# -------------------------------
@st.cache_resource
def train_model():
    X = [
        [7.5,150,0.08,0.02,0.6],
        [7.2,130,0.09,0.03,0.7],
        [6.5,70,0.15,0.01,0.3],
        [6.2,60,0.18,0.01,0.2],
        [7.8,180,0.07,0.04,0.8],
        [6.0,50,0.20,0.005,0.25]
    ]
    y = [0,0,1,1,0,1]  # 0=real, 1=AI
    
    model = LogisticRegression()
    model.fit(X, y)
    return model

def predict_ml(model, m):
    f = [[m["entropy"], m["laplacian"], m["edge"], m["noise"], m["color"]]]
    pred = model.predict(f)[0]
    prob = model.predict_proba(f)[0]
    return pred, max(prob)

# -------------------------------
# 🧠 FORENSIC LOGIC
# -------------------------------
def forensic_score(m):
    score = 0
    
    if m["entropy"] < 6.8: score += 30
    elif m["entropy"] < 7.2: score += 15
    
    if m["laplacian"] < 80: score += 25
    elif m["laplacian"] < 120: score += 12
    
    if m["edge"] > 0.15: score += 20
    elif m["edge"] > 0.12: score += 10
    
    if m["color"] < 0.4: score += 15
    
    return min(100, score)

# -------------------------------
# UI
# -------------------------------
st.title("🔍 Ultimate Detector v3.0")

file = st.file_uploader("Upload Image", type=["png","jpg","jpeg","webp"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 Analyze"):
        with st.spinner("Analyzing..."):
            img_bytes = file.read()
            
            # Metrics
            m = analyze_image(img_bytes)
            
            # ML
            model = train_model()
            ml_pred, ml_conf = predict_ml(model, m)
            
            # Forensic
            f_score = forensic_score(m)
            
            # Hybrid Score
            ml_score = 100 if ml_pred == 1 else 0
            final_ai = (0.6 * ml_score) + (0.4 * f_score)
            human = 100 - final_ai
            
            # Verdict
            if final_ai > 70:
                verdict = "❌ AI GENERATED"
                color = "red"
            elif final_ai > 40:
                verdict = "⚠️ UNCERTAIN"
                color = "orange"
            else:
                verdict = "✅ REAL IMAGE"
                color = "green"
            
            # Output
            st.subheader("📊 Results")
            st.write(f"AI Probability: {final_ai:.2f}%")
            st.write(f"Human Probability: {human:.2f}%")
            st.write(f"ML Confidence: {ml_conf*100:.2f}%")
            
            st.markdown(f"## <span style='color:{color}'>{verdict}</span>", unsafe_allow_html=True)
            
            # Report
            report = f"""
AI DETECTION REPORT
Time: {datetime.now()}

Entropy: {m['entropy']:.2f}
Laplacian: {m['laplacian']:.2f}
Edge: {m['edge']:.3f}
Noise: {m['noise']:.3f}
Color: {m['color']:.3f}

Final AI Score: {final_ai:.2f}%
Verdict: {verdict}
"""
            
            st.download_button("📥 Download Report", report, file_name="report.txt")
