import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from PyPDF2 import PdfReader

# Initialize session state
if "message_store" not in st.session_state:
    st.session_state.message_store = {}
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_pdf_text(pdf_docs):
    """Extract text from PDF documents"""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """Split text into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    """Create vector store from text chunks"""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    """Create conversation chain with RAG"""
    llm = ChatGroq(
        model="mixtral-8x7b-32768",
        groq_api_key=st.session_state.groq_api_key,
        temperature=0.7
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        verbose=True
    )
    
    return conversation_chain

def get_session_history(session_id: str):
    """Get or create chat history for a session"""
    if session_id not in st.session_state.message_store:
        st.session_state.message_store[session_id] = ChatMessageHistory()
    return st.session_state.message_store[session_id]

def initialize_chain():
    """Initialize the chat model and chain"""
    model = ChatGroq(
        model="mixtral-8x7b-32768",
        groq_api_key=st.session_state.groq_api_key
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer all questions to the best of your ability in {language}. If the question is about a PDF document, use the provided context to answer accurately."),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    chain = prompt | model
    
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="messages"
    )

def main():
    st.title("AI Chat Assistant with PDF Support")
    
    # Sidebar configuration
    with st.sidebar:
        # API Key input
        st.session_state.groq_api_key = st.text_input(
            "Enter GROQ API Key",
            type="password",
            help="Get your API key from https://console.groq.com/"
        )
        
        # Language selector
        language = st.selectbox(
            "Select Language",
            ["English", "Hindi", "Spanish", "French", "German"]
        )
        
        # PDF uploader
        pdf_docs = st.file_uploader(
            "Upload your PDFs",
            accept_multiple_files=True,
            type="pdf"
        )
        
        if st.button("Process PDFs"):
            if pdf_docs:
                with st.spinner("Processing PDFs..."):
                    try:
                        # Get PDF text
                        raw_text = get_pdf_text(pdf_docs)
                        
                        # Get text chunks
                        text_chunks = get_text_chunks(raw_text)
                        
                        # Create vector store
                        st.session_state.vectorstore = get_vectorstore(text_chunks)
                        
                        st.success("PDFs processed successfully!")
                    except Exception as e:
                        st.error(f"Error processing PDFs: {str(e)}")
            else:
                st.warning("Please upload PDF documents first.")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.message_store = {}
            st.session_state.chat_history = []
            st.session_state.vectorstore = None
            st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        if not st.session_state.groq_api_key:
            st.error("Please enter your GROQ API key in the sidebar.")
            return
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if st.session_state.vectorstore:  # If PDFs are processed
                        conversation = get_conversation_chain(st.session_state.vectorstore)
                        
                        # Format chat history for the conversation chain
                        chat_history = []
                        for i in range(0, len(st.session_state.messages)-1, 2):
                            if i+1 < len(st.session_state.messages):
                                chat_history.append(
                                    (st.session_state.messages[i]["content"],
                                     st.session_state.messages[i+1]["content"])
                                )
                        
                        response = conversation({
                            "question": prompt,
                            "chat_history": chat_history
                        })
                        response_content = response["answer"]
                        
                        # Display source documents if available
                        if "source_documents" in response:
                            with st.expander("Source Documents"):
                                for doc in response["source_documents"]:
                                    st.write(doc.page_content)
                    
                    else:  # Regular chat without PDF context
                        chain = initialize_chain()
                        config = {"configurable": {"session_id": "streamlit_chat"}}
                        response = chain.invoke(
                            {
                                "messages": [HumanMessage(content=prompt)],
                                "language": language
                            },
                            config=config
                        )
                        response_content = response.content
                    
                    st.markdown(response_content)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_content
                    })
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error("Full error details:", exc_info=True)

if __name__ == "__main__":
    main()