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
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<p class="hero-text">AI Chat & Content Assistant</p>', unsafe_allow_html=True)
        st.markdown("### Powered by GROQ & LangChain")
        st.markdown("Transform documents, videos, and web content into interactive conversations.")
        
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
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Document Processing</h3>
            <p>Upload and analyze PDF documents with ease.</p>
            <p class="sub-feature">• Multiple file support</p>
            <p class="sub-feature">• Smart text extraction</p>
        </div>
        """, unsafe_allow_html=True)
            
        st.markdown("""
        <div class="feature-card">
            <h3>🌍 Multilingual Support</h3>
            <p>Chat in multiple languages:</p>
            <p class="sub-feature">• English, Hindi, Spanish</p>
            <p class="sub-feature">• French, German</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎥 Video & Web Content</h3>
            <p>Summarize content from:</p>
            <p class="sub-feature">• YouTube videos</p>
            <p class="sub-feature">• Website articles</p>
            <p class="sub-feature">• Multiple summary styles</p>
        </div>
        """, unsafe_allow_html=True)
            
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Advanced AI Models</h3>
            <p>Choose from multiple models:</p>
            <p class="sub-feature">• Mixtral 8x7B</p>
            <p class="sub-feature">• LLaMA2 70B</p>
            <p class="sub-feature">• Claude 3 Opus</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Smart Summarization</h3>
            <p>Multiple summary types:</p>
            <p class="sub-feature">• Concise summaries</p>
            <p class="sub-feature">• Detailed analysis</p>
            <p class="sub-feature">• Bullet points</p>
        </div>
        """, unsafe_allow_html=True)
            
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Context-Aware</h3>
            <p>Enhanced conversation features:</p>
            <p class="sub-feature">• Conversation history</p>
            <p class="sub-feature">• Source references</p>
            <p class="sub-feature">• Smart responses</p>
        </div>
        """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown("## 🔄 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>1. Choose Input</h4>
            <p>Upload PDFs, paste URLs, or start chatting directly.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>2. Select Mode</h4>
            <p>Choose between chat, summarization, or document analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>3. Process Content</h4>
            <p>AI processes your content using advanced models.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <h4>4. Get Results</h4>
            <p>Receive summaries, answers, or engage in conversation.</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style='text-align: center; margin-top: 50px; padding: 20px;'>
            <p style='color: #8F9AAB;'>Made with ❤️ by Taufeeq</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_landing_page()