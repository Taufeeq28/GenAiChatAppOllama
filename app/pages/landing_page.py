import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_landing_page():
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
        }
        .hero-text {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(45deg, #FF4B4B, #FF9E9E);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<p class="hero-text">AI Chat Assistant</p>', unsafe_allow_html=True)
        st.markdown("### Powered by GROQ & LangChain")
        st.markdown("Transform your documents into interactive conversations.")
        
        if st.button("Get Started →"):
            st.switch_page("pages/chat.py")

    with col2:
        # Animation
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
        lottie_json = load_lottie_url(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=300)

    # Features Section
    st.markdown("## ✨ Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="feature-card">
                <h3>📄 PDF Processing</h3>
                <p>Upload and analyze multiple PDF documents with ease.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with st.container():
            st.markdown("""
            <div class="feature-card">
                <h3>🌍 Multilingual Support</h3>
                <p>Chat in multiple languages including English, Hindi, Spanish, French, and German.</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown("""
            <div class="feature-card">
                <h3>🤖 Advanced AI</h3>
                <p>Powered by GROQ's Mixtral-8x7B model for intelligent responses.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with st.container():
            st.markdown("""
            <div class="feature-card">
                <h3>💡 Context-Aware</h3>
                <p>Maintains conversation history and provides relevant responses.</p>
            </div>
            """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown("## 🔄 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>1. Upload Documents</h4>
            <p>Upload your PDF documents through the intuitive interface.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>2. Process & Analyze</h4>
            <p>AI processes and indexes your documents for quick retrieval.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>3. Start Chatting</h4>
            <p>Ask questions and get intelligent responses based on your documents.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_landing_page()