import streamlit as st
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

# Now use absolute imports
from utils.chat_utils import (
    get_pdf_text,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
    initialize_chain
)
GROQ_MODELS = {
    "Mixtral 8x7B": {
        "id": "mixtral-8x7b-32768",
        "description": "Powerful open-source model with broad capabilities",
        "context_length": 32768,
    },
    "LLaMA2 70B": {
        "id": "llama2-70b-4096",
        "description": "Meta's largest model with strong general capabilities",
        "context_length": 4096,
    },
    "Gemma 7B": {
        "id": "gemma-7b-it",
        "description": "Google's efficient model optimized for instruction following",
        "context_length": 8192,
    },
    "Claude 3 Opus": {
        "id": "claude-3-opus-20240229",
        "description": "Anthropic's most powerful model",
        "context_length": 200000,
    }
}

def show_chat_interface():
    # Custom CSS for chat interface
    st.markdown("""
        <style>
        .chat-container {
            background-color: #1E2129;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        }
        .user-message {
            background-color: #FF4B4B;
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px 0;
            max-width: 70%;
            float: right;
        }
        .assistant-message {
            background-color: #2E3440;
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px 0;
            max-width: 70%;
            float: left;
        }
        .sidebar .stButton>button {
            width: 100%;
            margin: 5px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("🤖 Chat Settings")  # Using emoji instead of logo
        
        # API Key input
        st.session_state.groq_api_key = st.text_input(
            "GROQ API Key",
            type="password",
            help="Get your API key from console.groq.com",
            placeholder="Enter your API key..."
        )
                # Add Model selector before language selector
        st.markdown("### 🧠 Model Selection")
        selected_model = st.selectbox(
            "Choose a Model",
            options=list(GROQ_MODELS.keys()),
            index=0,
        )
        
        # Show model details
        with st.expander("Model Details", expanded=False):
            model_info = GROQ_MODELS[selected_model]
            st.markdown(f"""
                **Model ID:** `{model_info['id']}`\n
                **Description:** {model_info['description']}\n
                **Context Length:** {model_info['context_length']} tokens
            """)
        
        # Store selected model ID in session state
        st.session_state.selected_model_id = GROQ_MODELS[selected_model]['id']
        # Language selector
        language_options = {
            "🇺🇸 English": "English",
            "🇮🇳 Hindi": "Hindi",
            "🇪🇸 Spanish": "Spanish",
            "🇫🇷 French": "French",
            "🇩🇪 German": "German"
        }
        selected_lang = st.selectbox(
            "Select Language",
            options=list(language_options.keys())
        )
        language = language_options[selected_lang]
        
        # PDF uploader
        st.markdown("### 📄 Upload Documents")
        pdf_docs = st.file_uploader(
            "Drag and drop your PDFs here",
            accept_multiple_files=True,
            type="pdf"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Process", use_container_width=True):
                if pdf_docs:
                    with st.spinner("Processing documents..."):
                        try:
                            raw_text = get_pdf_text(pdf_docs)
                            text_chunks = get_text_chunks(raw_text)
                            st.session_state.vectorstore = get_vectorstore(text_chunks)
                            st.success("✅ Success!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Upload PDFs first")
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.session_state.message_store = {}
                st.session_state.chat_history = []
                st.session_state.vectorstore = None
                st.rerun()

    # Main chat interface
    st.title("💬 Chat Interface")

    # Display chat messages
    message_container = st.container()
    with message_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not st.session_state.groq_api_key:
            st.error("⚠️ Please enter your GROQ API key in the sidebar.")
        else:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        if st.session_state.vectorstore:
                            conversation = get_conversation_chain(st.session_state.vectorstore)
                            chat_history = [(st.session_state.messages[i]["content"], 
                                           st.session_state.messages[i+1]["content"]) 
                                          for i in range(0, len(st.session_state.messages)-1, 2)]
                            
                            response = conversation({
                                "question": prompt,
                                "chat_history": chat_history
                            })
                            
                            st.markdown(response["answer"])
                            if "source_documents" in response:
                                with st.expander("📚 Source Documents"):
                                    for i, doc in enumerate(response["source_documents"], 1):
                                        st.markdown(f"**Source {i}:**")
                                        st.markdown(doc.page_content)
                        else:
                            chain = initialize_chain()
                            response = chain.invoke(
                                {"messages": [{"role": "user", "content": prompt}],
                                 "language": language},
                                {"configurable": {"session_id": "streamlit_chat"}}
                            )
                            st.markdown(response.content)
                        
                        # Add assistant response to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["answer"] if st.session_state.vectorstore else response.content
                        })
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Initialize session state
    if "message_store" not in st.session_state:
        st.session_state.message_store = {}
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_model_id" not in st.session_state:
        st.session_state.selected_model_id = GROQ_MODELS["Mixtral 8x7B"]["id"]
    show_chat_interface()