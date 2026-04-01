import streamlit as st
import numpy as np
from PIL import Image
import random
import time
from datetime import datetime

st.set_page_config(page_title="🔍 All-in-One Detector", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
.main {background: linear-gradient(135deg,#0a0a
