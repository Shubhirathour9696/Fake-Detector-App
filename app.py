import streamlit as st
import numpy as np
from PIL import Image
import io

# Safe import
try:
    import cv2
except:
    cv2 = None

st.title("🔍 AI Image Detector (Safe Version)")

def forensic_analysis(image_bytes):
    if cv2 is None:
        return {"ai_forensic": 50}

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        arr = np.array(img)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

        laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / (gray.shape[0] * gray.shape[1])

        ai_score = 0
        if laplacian < 50: ai_score += 30
        if edge_density < 0.05: ai_score += 30

        return {"ai_forensic": ai_score}

    except:
        return {"ai_forensic": 50}


uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image)

    img_bytes = uploaded_file.read()

    if st.button("Analyze"):
        result = forensic_analysis(img_bytes)

        ai_prob = result["ai_forensic"]
        real_prob = 100 - ai_prob

        if ai_prob > 60:
            st.error(f"🤖 AI Generated ({ai_prob}%)")
        else:
            st.success(f"✅ Real Image ({real_prob}%)")
