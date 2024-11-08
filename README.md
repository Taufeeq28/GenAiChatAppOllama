AI Assistant Hub 🤖
A powerful AI assistant application built with Streamlit and GROQ AI, offering chat capabilities, resume optimization, and content analysis.

Features ✨
📄 Document Processing
Multiple file support
Smart text extraction
Detailed analysis
🎥 Video & Web Content
YouTube video summarization
Website article analysis
Multiple summary styles
📊 Smart Summarization
Concise summaries
Detailed analysis
Bullet points
🌍 Multilingual Support
English, Hindi, Spanish
French, German
Real-time translation
🤖 Advanced AI Models
Mixtral 8x7B
LLaMA2 70B
Claude 3 Opus
💡 Context-Aware
Conversation history
Source references
Smart responses
Installation 🚀
Clone the repository:

cmd
Copy code
git clone https://github.com/yourusername/GenAiChatAppOllama.git
cd GenAiChatAppOllama
Create a virtual environment:

cmd
Copy code
python -m venv venv
venv\Scripts\activate
Install dependencies:

cmd
Copy code
pip install -r requirements.txt
Create a .env file in the root directory and add your GROQ API key:

plaintext
Copy code
GROQ_API_KEY=your_api_key_here
Usage 💻
Start the application:

cmd
Copy code
streamlit run app\main.py
Open your browser and navigate to:

arduino
Copy code
http://localhost:8501
Features in Detail 🔍
Chat Interface
Real-time AI conversations
Multiple language support
Context-aware responses
File upload capabilities
YouTube video analysis
Website content summarization
Resume Optimizer
ATS optimization
Skills matching
Project suggestions
Format preservation
Keyword optimization
Industry-specific enhancements
Project Structure 📁
plaintext
Copy code
GenAiChatAppOllama/
├── app/
│   ├── pages/
│   │   ├── chat.py
│   │   └── resume_optimizer.py
│   ├── utils/
│   │   ├── chat_utils.py
│   │   └── resume_processor.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
Dependencies 📦
streamlit==1.40.0
langchain
langchain-community
python-dotenv
PyPDF2
pypdf
langchain-text-splitters
langchain_groq
langchain_core
streamlit-lottie
youtube-transcript-api
beautifulsoup4
requests
python-docx
Configuration ⚙️
The application uses several AI models from GROQ:

Mixtral 8x7B (Default)
LLaMA2 70B
Gemma 7B
Claude 3 Opus
Contributing 🤝
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m "Add some AmazingFeature")
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
License 📄
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments 🙏
GROQ AI for providing the AI models
Streamlit for the amazing web framework
LangChain for the powerful AI capabilities
Author ✍️
Taufeeq

Support 💪
If you find this project helpful, please give it a ⭐️!

