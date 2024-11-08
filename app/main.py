import streamlit as st
from pathlib import Path
import sys
from dotenv import load_dotenv
import os
from streamlit_lottie import st_lottie
import json
import requests

# Add the app directory to the Python path
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# Load environment variables
load_dotenv()

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Page configuration
st.set_page_config(
    page_title="AI Assistant Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .feature-card {
        background-color: #1E2129;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2E3440;
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .hero-text {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #FF4B4B, #FF9E9E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-feature {
        font-size: 0.9rem;
        color: #8F9AAB;
        margin-top: 5px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-1rs6os {visibility: hidden;}
    .css-17ziqus {visibility: hidden;}
    .css-1dp5vir {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Store API key and model in session state (you can move this configuration to the chat page)
st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")
st.session_state.selected_model_id = "mixtral-8x7b-32768"  # Default model

# Main content
# Hero Section
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<p class="hero-text">AI Assistant Hub</p>', unsafe_allow_html=True)
    st.markdown("### Powered by GROQ & LangChain")
    st.markdown("Transform your content with AI-powered conversations and analysis.")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Start Chat →"):
            st.switch_page("pages/chat.py")
    with col_btn2:
        if st.button("Optimize Resume →"):
            st.switch_page("pages/resume_optimizer.py")

with col2:
    # Animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
    lottie_json = load_lottie_url(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=300)

# Features Section
st.markdown("## ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>💬 AI Chat</h3>
        <p>Intelligent conversations powered by advanced AI:</p>
        <p class="sub-feature">• Multiple AI models</p>
        <p class="sub-feature">• Context awareness</p>
        <p class="sub-feature">• Smart responses</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📄 Resume Optimizer</h3>
        <p>Enhance your resume with AI:</p>
        <p class="sub-feature">• ATS optimization</p>
        <p class="sub-feature">• Skills matching</p>
        <p class="sub-feature">• Project suggestions</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 Advanced Features</h3>
        <p>Powerful capabilities:</p>
        <p class="sub-feature">• Multiple languages</p>
        <p class="sub-feature">• Document analysis</p>
        <p class="sub-feature">• Real-time processing</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>📄 Document Processing</h3>
        <p>Upload and analyze PDF documents with ease:</p>
        <p class="sub-feature">• Multiple file support</p>
        <p class="sub-feature">• Smart text extraction</p>
        <p class="sub-feature">• Detailed analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <h3>🎥 Video & Web Content</h3>
        <p>Summarize content from:</p>
        <p class="sub-feature">• YouTube videos</p>
        <p class="sub-feature">• Website articles</p>
        <p class="sub-feature">• Multiple summary styles</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Smart Summarization</h3>
        <p>Multiple summary types:</p>
        <p class="sub-feature">• Concise summaries</p>
        <p class="sub-feature">• Detailed analysis</p>
        <p class="sub-feature">• Bullet points</p>
    </div>
    """, unsafe_allow_html=True)

# How It Works Section
st.markdown("## 🔄 How It Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>1. Choose Service</h4>
        <p>Select chat or resume optimization</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>2. Input Content</h4>
        <p>Start chat or upload resume</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>3. AI Processing</h4>
        <p>Advanced AI analyzes your content</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h4>4. Get Results</h4>
        <p>Receive optimized output</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 20px;'>
        <p style='color: #8F9AAB;'>Built with ❤️ using Streamlit and GROQ AI</p>
    </div>
""", unsafe_allow_html=True)