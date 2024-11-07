import streamlit as st
from pages.landing_page import show_landing_page

# Configure Streamlit page
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "message_store" not in st.session_state:
    st.session_state.message_store = {}
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def main():
    show_landing_page()

if __name__ == "__main__":
    main()