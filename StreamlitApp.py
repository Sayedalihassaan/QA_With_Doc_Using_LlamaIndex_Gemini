# StreamlitApp.py
import streamlit as st
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import gemini_embedding, load_model
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def apply_custom_css():
    """Apply custom CSS for professional styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Section styling */
    .section-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e1e5e9;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Upload area styling */
    .upload-container {
        border: 2px dashed #3498db;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        border-color: #2980b9;
        background: #e3f2fd;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Answer section */
    .answer-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin-top: 2rem;
    }
    
    /* Success message */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    /* Error message */
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    /* Info box */
    .info-box {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create a professional sidebar"""
    with st.sidebar:
        st.markdown("## 📋 **App Information**")
        st.markdown("""
        Welcome to the **Document QA Assistant**!
        
        ### **Features:**
        • 📄 Upload PDF or text documents
        • 🤖 AI-powered question answering
        • 🔍 Intelligent content analysis
        • ⚡ Fast and accurate responses
        
        ### **Supported Files:**
        • PDF documents (.pdf)
        • Text files (.txt)
        • Maximum size: 200MB
        """)
        
        st.markdown("---")
        
        st.markdown("## ⚙️ **Settings**")
        max_tokens = st.slider("Response Length", 100, 1000, 500, help="Maximum length of AI response")
        temperature = st.slider("Creativity Level", 0.0, 1.0, 0.3, help="Higher values = more creative responses")
        
        st.markdown("---")
        
        st.markdown("## 💡 **Tips for Better Results**")
        st.markdown("""
        • **Be specific** in your questions
        • **Upload clear** documents
        • **Ask one question** at a time
        • **Try rephrasing** if needed
        """)
        
        return max_tokens, temperature

def main():
    # Configure page
    st.set_page_config(
        page_title="Document QA Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styling
    apply_custom_css()
    
    # Create sidebar
    max_tokens, temperature = create_sidebar()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Document QA Assistant</h1>
        <p>Upload your documents and get instant AI-powered answers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not GOOGLE_API_KEY:
        st.error("⚠️ **Google API key not found!** Please configure your .env file with GOOGLE_API_KEY.")
        st.stop()
    
    # Create main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Document Upload Section
        st.markdown("""
        <div class="section-container">
            <div class="section-title">📁 Upload Your Document</div>
        </div>
        """, unsafe_allow_html=True)
        
        doc = st.file_uploader(
            "Choose a document to analyze",
            type=["pdf", "txt"],
            help="Upload PDF or text files (max 200MB)",
            key="document_uploader"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Question Section
        st.markdown("""
        <div class="section-container">
            <div class="section-title">❓ Ask Your Question</div>
        </div>
        """, unsafe_allow_html=True)
        
        user_question = st.text_area(
            "What would you like to know about your document?",
            placeholder="Example: What are the main topics discussed in this document?",
            height=120,
            help="Be specific for better results",
            key="question_input"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit Button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submit_button = st.button("🚀 **Analyze Document & Answer Question**", use_container_width=True)
    
    with col2:
        # Document Status
        if doc is not None:
            st.markdown("""
            <div class="success-message">
                <strong>✅ Document Uploaded Successfully!</strong>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📊 **Document Details:**")
            st.write(f"**📝 Name:** {doc.name}")
            st.write(f"**📏 Size:** {doc.size:,} bytes")
            st.write(f"**📄 Type:** {doc.type}")
        else:
            st.markdown("""
            <div class="info-box">
                <strong>ℹ️ No document uploaded yet</strong><br>
                Please upload a PDF or text file to get started.
            </div>
            """, unsafe_allow_html=True)
    
    # Process the request
    if submit_button:
        if doc is None:
            st.warning("⚠️ **Please upload a document first.**")
        elif not user_question.strip():
            st.warning("⚠️ **Please enter a question.**")
        else:
            # Processing section
            with st.container():
                st.markdown("---")
                st.markdown("## 🔄 **Processing Your Request**")
                
                # Create columns for progress
                progress_col1, progress_col2 = st.columns([3, 1])
                
                with progress_col1:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                
                try:
                    # Step 1: Load document
                    status_text.text("📖 Loading document...")
                    progress_bar.progress(20)
                    documents = load_data(doc)
                    time.sleep(0.3)
                    
                    # Step 2: Initialize model
                    status_text.text("🧠 Initializing AI model...")
                    progress_bar.progress(40)
                    model = load_model()
                    time.sleep(0.3)
                    
                    # Step 3: Create embeddings
                    status_text.text("🔗 Creating document embeddings...")
                    progress_bar.progress(60)
                    query_engine = gemini_embedding(model, documents)
                    time.sleep(0.3)
                    
                    # Step 4: Generate answer
                    status_text.text("🎯 Generating your answer...")
                    progress_bar.progress(80)
                    response = query_engine.query(user_question)
                    
                    # Step 5: Complete
                    status_text.text("✅ Complete!")
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Display results
                    st.markdown("## 💡 **Your Answer**")
                    
                    st.markdown("""
                    <div class="answer-container">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"**🤖 AI Response:**")
                    st.write(response.response)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Additional information
                    if hasattr(response, 'source_nodes') and response.source_nodes:
                        with st.expander("📚 **View Source References**"):
                            for i, node in enumerate(response.source_nodes[:3], 1):
                                st.markdown(f"**Source {i}:**")
                                preview_text = node.text[:300] + "..." if len(node.text) > 300 else node.text
                                st.text(preview_text)
                                st.markdown("---")
                    
                    # Feedback section
                    st.markdown("### 📝 **How was this response?**")
                    feedback_col1, feedback_col2, feedback_col3 = st.columns(3)
                    
                    with feedback_col1:
                        if st.button("👍 **Helpful**", use_container_width=True):
                            st.success("Thank you for your feedback! 😊")
                    
                    with feedback_col2:
                        if st.button("👎 **Not Helpful**", use_container_width=True):
                            st.info("Thanks for the feedback. We'll keep improving! 🔧")
                    
                    with feedback_col3:
                        if st.button("🔄 **Try Again**", use_container_width=True):
                            st.rerun()
                
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.markdown("## ❌ **Error Occurred**")
                    
                    st.markdown("""
                    <div class="error-message">
                        <strong>Something went wrong while processing your request.</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("🔍 **Error Details**"):
                        st.code(str(e))
                    
                    st.markdown("### **💡 Troubleshooting Tips:**")
                    st.markdown("""
                    • **Check your document:** Make sure it's readable and not corrupted
                    • **Verify API key:** Ensure your Google API key is correctly configured
                    • **Try smaller files:** Large documents may cause processing issues
                    • **Simplify your question:** Try asking a more specific question
                    • **Refresh and retry:** Sometimes a simple refresh helps
                    """)

if __name__ == "__main__":
    main()