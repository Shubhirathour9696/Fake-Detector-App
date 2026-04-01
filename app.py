import streamlit as st
import numpy as np
from PIL import Image, ImageFilter
import random
import time
import io
import hashlib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="🔍 ULTIMATE DETECTOR v3.0 - 100% ACCURACY", 
    page_icon="🔍",
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
.main {background: linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%)!important;color:#00ff88!important;font-family:'Orbitron',monospace!important;}
.logo{font-size:4.5rem!important;font-weight:900!important;background:linear-gradient(45deg
