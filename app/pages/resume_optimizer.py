import streamlit as st
import sys
from pathlib import Path
from dotenv import load_dotenv
import tempfile
import os
from io import BytesIO


# Add the app directory to the Python path
current_dir = Path(__file__).resolve().parent.parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from config import GROQ_MODELS
from utils.resume_processor import ResumeOptimizer

def check_api_key():
    """Check if API key is available and valid"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ GROQ API Key not found!")
        st.info("""
        Please follow these steps:
        1. Create a `.env` file in your project root directory
        2. Add your GROQ API key to the file:
        ```
        GROQ_API_KEY=your_api_key_here
        ```
        3. Restart the application
        """)
        st.stop()
    return api_key

# Get API key
GROQ_API_KEY = check_api_key()
# Page configuration
st.set_page_config(
    page_title="Resume Optimizer",
    page_icon="📄",
    layout="wide",
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .upload-box {
        border: 2px dashed #FF4B4B;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    .info-box {
        background-color: #1E2129;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .download-button {
        background-color: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-align: center;
        margin: 20px 0;
    }
    .changes-box {
        background-color: #2d3748;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    h1 {
        color: #FF4B4B;
        margin-bottom: 2rem;
    }
    h3 {
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

def show_resume_optimizer():
    # Main content
    st.title("🎯 Resume Optimizer")
    
    if "selected_model_id" not in st.session_state:
        st.session_state.selected_model_id = GROQ_MODELS["Mixtral 8x7B"]["id"]
    if "optimization_complete" not in st.session_state:
        st.session_state.optimization_complete = False
    if "optimized_content" not in st.session_state:
        st.session_state.optimized_content = None
    
    # Store API key in session state
    st.session_state.groq_api_key = GROQ_API_KEY
    
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuration")
        
       
        
        # Model Selection
        st.markdown("### 🧠 Model")
        selected_model = st.selectbox(
            "Select AI Model",
            options=list(GROQ_MODELS.keys()),
            key="model_selector"
        )
        st.session_state.selected_model_id = GROQ_MODELS[selected_model]["id"]
        
        # Model Info
        with st.expander("ℹ️ Model Details"):
            st.write(f"**Description:** {GROQ_MODELS[selected_model]['description']}")
            st.write(f"**Context Length:** {GROQ_MODELS[selected_model]['context_length']} tokens")
    
    # Main content columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📄 Upload Resume")
        resume_file = st.file_uploader(
            "Drop your resume here",
            type=["docx"],
            help="Please ensure your resume is in DOCX format",
            key="resume_upload"
        )
        
        if resume_file:
            st.success("✅ Resume uploaded successfully!")
    
    with col2:
        st.markdown("### 💼 Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=200,
            key="job_description",
            help="Copy and paste the complete job description"
        )
    
    # Process button and optimization
    if resume_file and job_description:
        if st.button("🚀 Optimize Resume", key="optimize_button"):
            
                
            try:
                with st.spinner("🔄 Analyzing and optimizing your resume..."):
                    optimizer = ResumeOptimizer(
                        groq_api_key=st.session_state.groq_api_key,
                        model_id=st.session_state.selected_model_id
                    )
                    
                    # Create temporary files for processing
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_input:
                        tmp_input.write(resume_file.getvalue())
                        input_path = tmp_input.name
                    
                    output_path = input_path.replace('.docx', '_optimized.docx')
                    
                    # Process the resume
                    success = optimizer.process_resume(
                        input_path,
                        job_description,
                        output_path
                    )
                    
                    if success:
                        # Read the optimized file
                        with open(output_path, 'rb') as file:
                            st.session_state.optimized_content = file.read()
                            st.session_state.optimization_complete = True
                            st.session_state.added_skills = optimizer.added_skills
                            st.session_state.added_projects = optimizer.added_projects
                        
                        # Clean up temporary files
                        os.unlink(input_path)
                        os.unlink(output_path)
                        
                        st.success("✅ Resume optimized successfully!")
                        
                        # Show download button
                        st.download_button(
                            label="📥 Download Optimized Resume",
                            data=st.session_state.optimized_content,
                            file_name=f"{resume_file.name.split('.')[0]}_optimized.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key="download_button",
                            help="Click to download your optimized resume"
                        )
                        
                        # Show optimization summary
                        st.markdown("### 📋 Optimization Summary")
                        with st.expander("View Changes", expanded=True):
                            st.markdown("**🎯 Skills Matched:**")
                            for skill in st.session_state.added_skills:
                                st.markdown(f"- {skill}")
                            
                            st.markdown("\n**💡 Projects Added:**")
                            for project in st.session_state.added_projects:
                                with st.container():
                                    st.markdown(f"**{project['title']}**")
                                    st.markdown(f"{project['description']}")
                                    st.markdown("**Technologies:** " + ", ".join(project['technologies']))
                                    st.markdown("---")
                    
            except Exception as e:
                st.error(f"❌ Error during optimization: {str(e)}")
                st.info("Please check your API key and try again.")
    
    # Tips and guidelines
    with st.expander("📌 Tips for Better Results"):
        st.markdown("""
        - Make sure your resume is in DOCX format
        - Include the complete job description
        - Ensure your API key is valid
        - Choose the appropriate model for better results
        - Review the generated content before submitting
        - Keep your resume formatting consistent
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>Built By taufeeq</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show_resume_optimizer()