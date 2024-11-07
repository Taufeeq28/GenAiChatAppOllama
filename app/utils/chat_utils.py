import streamlit as st
from PyPDF2 import PdfReader
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain

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