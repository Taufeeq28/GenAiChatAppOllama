import streamlit as st
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
        "id": "llama2-70b", # Fixed model ID
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

def get_youtube_id(url):
    """Extract YouTube video ID from URL"""
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path.startswith(('/embed/', '/v/')):
            return parsed_url.path.split('/')[2]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    return None

def get_youtube_transcript(video_id):
    """Get transcript of YouTube video"""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([item['text'] for item in transcript_list])
        return transcript
    except Exception as e:
        st.error(f"Error getting YouTube transcript: {str(e)}")
        return None

def get_website_content(url):
    """Extract main content from website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        st.error(f"Error fetching website content: {str(e)}")
        return None



def summarize_text(text, summary_type="concise"):
    """Summarize the given text"""
    try:
        llm = ChatGroq(
            groq_api_key=st.session_state.groq_api_key,
            model=st.session_state.selected_model_id
        )
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,  # Adjust based on model's context length
            chunk_overlap=200,
            length_function=len,
        )
        
        # Split text into chunks
        texts = text_splitter.split_text(text)
        
        # Process each chunk
        summaries = []
        for chunk in texts:
            # Define prompt template for each chunk
            prompt = PromptTemplate(
                template="Summarize the following text concisely:\n\n{text}\n\nSummary:",
                input_variables=["text"]
            )
            
            # Create chain for chunk
            chain = load_summarize_chain(
                llm,
                chain_type="stuff",
                prompt=prompt
            )
            
            # Process chunk
            doc = [Document(page_content=chunk)]
            chunk_summary = chain.run(doc)
            summaries.append(chunk_summary)
        
        # Combine chunk summaries
        if len(summaries) > 1:
            # Create final summary from all chunks
            final_text = " ".join(summaries)
            prompt = PromptTemplate(
                template="""Combine and create a final {summary_type} summary of the following summaries:
                \n\n{text}\n\nFinal Summary:""",
                input_variables=["text", "summary_type"]
            )
            
            chain = load_summarize_chain(
                llm,
                chain_type="stuff",
                prompt=prompt
            )
            
            final_doc = [Document(page_content=final_text)]
            return chain.run({
                "input_documents": final_doc,
                "text": final_text,
                "summary_type": summary_type
            })
        else:
            return summaries[0]
    
    except Exception as e:
        st.error(f"Error in summarization: {str(e)}")
        return None
def show_chat_interface():
    # Define language options
    language_options = {
        "🇺🇸 English": "English",
        "🇮🇳 Hindi": "Hindi",
        "🇪🇸 Spanish": "Spanish",
        "🇫🇷 French": "French",
        "🇩🇪 German": "German"
    }

    # Custom CSS for enhanced UI
    st.markdown("""
        <style>
        /* Reset background colors */
        .sidebar .block-container {
            padding: 2rem 1rem;
            background-color: transparent !important;
        }
        
        /* Remove dark backgrounds from sections */
        .sidebar .element-container {
            background-color: transparent !important;
            margin-bottom: 1rem;
        }
        
        /* Style section headers */
        .section-header {
            color: #FFFFFF;
            font-size: 1.2rem;
            margin: 1.5rem 0 1rem 0;
            padding: 0;
            background: transparent;
        }
        
        /* Style input fields */
        .stTextInput > div > div > input {
            background-color: #2E3440 !important;
            color: white;
            border: 1px solid #4C566A;
            border-radius: 8px;
        }
        
        /* Style selectboxes */
        .stSelectbox > div > div {
            background-color: #2E3440 !important;
            color: white;
            border: 1px solid #4C566A;
            border-radius: 8px;
        }
        
        /* Style expander */
        .streamlit-expanderHeader {
            background-color: #2E3440 !important;
            border: 1px solid #4C566A;
            border-radius: 8px;
            color: white;
        }
        
        /* Style file uploader */
        .stFileUploader > div {
            background-color: #2E3440 !important;
            border: 2px dashed #4C566A;
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Style buttons */
        .stButton > button {
            background-color: #4C566A;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #5E81AC;
            transform: translateY(-1px);
        }
        
        /* Remove any unwanted backgrounds */
        div[data-testid="stSidebarNav"] {
            background-color: transparent !important;
        }
        
        .sidebar-content {
            background-color: transparent !important;
        }
        
        /* Main background color for sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1E2129 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        # Header
        st.markdown("""
            <div class="sidebar-header">
                <h1 style='color: white; font-size: 1.8rem; margin-bottom: 0.5rem;'>🤖 AI Chat Assistant</h1>
                <p style='color: #9E9E9E; font-size: 0.9rem;'>Powered by GROQ</p>
            </div>
        """, unsafe_allow_html=True)
        
        # API Configuration
        st.markdown('<div class="section-header">🔑 API Configuration</div>', unsafe_allow_html=True)
        st.session_state.groq_api_key = st.text_input(
            "GROQ API Key",
            type="password",
            help="Get your API key from console.groq.com",
            placeholder="Enter your API key...",
            label_visibility="collapsed"
        )
        
        # Model Selection
        st.markdown('<div class="section-header">🧠 Model Selection</div>', unsafe_allow_html=True)
        selected_model = st.selectbox(
            "Choose a Model",
            options=list(GROQ_MODELS.keys()),
            index=0,
            label_visibility="collapsed"
        )
        
        # Model Details
        with st.expander("ℹ️ Model Details", expanded=False):
            model_info = GROQ_MODELS[selected_model]
            st.markdown(f"""
                <div style='padding: 1rem; border-radius: 8px;'>
                    <p><strong>Model ID:</strong> <code>{model_info['id']}</code></p>
                    <p><strong>Description:</strong> {model_info['description']}</p>
                    <p><strong>Context Length:</strong> {model_info['context_length']} tokens</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Language Selection
        st.markdown('<div class="section-header">🌐 Language</div>', unsafe_allow_html=True)
        selected_lang = st.selectbox(
            "Select Language",
            options=list(language_options.keys()),
            label_visibility="collapsed"
        )
        language = language_options[selected_lang]
        
        # Document Upload
        st.markdown('<div class="section-header">📄 Upload Documents</div>', unsafe_allow_html=True)
        pdf_docs = st.file_uploader(
            "Drag and drop your PDFs here",
            accept_multiple_files=True,
            type="pdf",
            label_visibility="collapsed"
        )
        
        # Action Buttons
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

        # URL Summarization
        with st.expander("🔗 Summarize URL Content", expanded=False):
            url_input = st.text_input(
                "Enter YouTube URL or website URL",
                placeholder="https://..."
            )
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                content_type = st.radio(
                    "Content Type",
                    ["YouTube Video", "Website"],
                    horizontal=True
                )
                
            with col2:
                summary_type = st.selectbox(
                    "Summary Type",
                    ["concise", "detailed", "bullet_points"],
                    help="Choose the type of summary"
                )
            
            if st.button("📝 Generate Summary", use_container_width=True):
                if not st.session_state.groq_api_key:
                    st.error("⚠️ Please enter your GROQ API key first.")
                elif not url_input:
                    st.warning("⚠️ Please enter a URL.")
                else:
                    with st.spinner("Processing content..."):
                        try:
                            if content_type == "YouTube Video":
                                video_id = get_youtube_id(url_input)
                                if not video_id:
                                    st.error("Invalid YouTube URL")
                                    return
                                
                                transcript = get_youtube_transcript(video_id)
                                if not transcript:
                                    st.error("Could not get video transcript")
                                    return
                                
                                summary = summarize_text(transcript, "video")
                                if summary:
                                    st.markdown("### Video Summary")
                                    st.markdown(summary)
                                    
                                    # Add to chat history
                                    st.session_state.messages.append({
                                        "role": "user",
                                        "content": f"Please summarize this YouTube video: {url_input}"
                                    })
                                    st.session_state.messages.append({
                                        "role": "assistant",
                                        "content": f"Here's a summary of the video:\n\n{summary}"
                                    })
                                    st.rerun()
                            
                            else:  # Website
                                content = get_website_content(url_input)
                                if not content:
                                    st.error("Could not fetch website content")
                                    return
                                
                                summary = summarize_text(content, "article")
                                if summary:
                                    st.markdown("### Article Summary")
                                    st.markdown(summary)
                                    
                                    # Add to chat history
                                    st.session_state.messages.append({
                                        "role": "user",
                                        "content": f"Please summarize this article: {url_input}"
                                    })
                                    st.session_state.messages.append({
                                        "role": "assistant",
                                        "content": f"Here's a summary of the article:\n\n{summary}"
                                    })
                                    st.rerun()
                        
                        except Exception as e:
                            st.error(f"Error processing URL: {str(e)}")
        
        # Footer
        st.markdown("""
            <div class="sidebar-footer">
                <p style='color: #9E9E9E; font-size: 0.8rem; margin: 0;'>by Taufeeq</p>
            </div>
        """, unsafe_allow_html=True)

    # Store selected model ID in session state
    st.session_state.selected_model_id = GROQ_MODELS[selected_model]['id']

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