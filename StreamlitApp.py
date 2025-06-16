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
    /* Main container styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Custom header styling */
    .custom-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .custom-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .custom-header p {
        color: #e8f4fd;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    
    /* Upload section styling */
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Question input styling */
    .question-section {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Answer section styling */
    .answer-section {
        background: #e8f5e8;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin-top: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: #e3f2fd;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #2a5298;
    }
    
    /* Info boxes */
    .info-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create a professional sidebar with information and settings"""
    with st.sidebar:
        st.markdown("### 📋 Application Info")
        st.markdown("""
        **Document QA System**
        
        This application allows you to:
        - 📄 Upload PDF or text documents
        - 🤖 Ask questions about the content
        - 🔍 Get AI-powered answers
        
        **Supported Formats:**
        - PDF files (.pdf)
        - Text files (.txt)
        """)
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        # Add some configuration options
        max_tokens = st.slider("Max Response Length", 100, 1000, 500)
        confidence_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.7)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Upload clear, well-formatted documents
        - Ask specific questions for better results
        - Try different phrasings if needed
        """)
        
        return max_tokens, confidence_threshold

def display_header():
    """Display the custom header"""
    st.markdown("""
    <div class="custom-header">
        <h1>🤖 Document QA Assistant</h1>
        <p>Upload your documents and get instant AI-powered answers</p>
    </div>
    """, unsafe_allow_html=True)

def display_upload_section():
    """Display the file upload section"""
    st.markdown("""
    <div class="upload-section">
        <h3>📁 Upload Your Document</h3>
        <p>Select a PDF or text file to analyze</p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.file_uploader(
        "Choose a file",
        type=["pdf", "txt"],
        help="Upload PDF or text files up to 200MB",
        key="document_uploader"
    )

def display_question_section():
    """Display the question input section"""
    st.markdown("""
    <div class="question-section">
        <h3>❓ Ask Your Question</h3>
        <p>Enter your question about the uploaded document</p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.text_area(
        "Your Question:",
        placeholder="e.g., What are the main topics discussed in this document?",
        height=100,
        help="Be specific for better results",
        key="question_input"
    )

def display_processing_status(step, total_steps):
    """Display processing progress"""
    progress = step / total_steps
    st.progress(progress)
    
    status_messages = [
        "🔄 Loading document...",
        "🧠 Initializing AI model...",
        "📊 Creating embeddings...",
        "🔍 Processing your question...",
        "✅ Generating response..."
    ]
    
    if step <= len(status_messages):
        st.info(status_messages[step - 1])

def display_answer(response):
    """Display the answer in a styled format"""
    st.markdown("""
    <div class="answer-section">
        <h3>💡 Answer</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the response
    st.markdown(f"**Response:** {response.response}")
    
    # Add confidence indicator if available
    if hasattr(response, 'metadata') and 'confidence' in response.metadata:
        confidence = response.metadata['confidence']
        st.progress(confidence)
        st.caption(f"Confidence: {confidence:.1%}")
    
    # Add source information if available
    if hasattr(response, 'source_nodes') and response.source_nodes:
        with st.expander("📚 Sources"):
            for i, node in enumerate(response.source_nodes):
                st.markdown(f"**Source {i+1}:**")
                st.text(node.text[:200] + "..." if len(node.text) > 200 else node.text)

def show_error_message(error):
    """Display error message in a user-friendly way"""
    st.error("❌ Something went wrong!")
    
    with st.expander("Error Details"):
        st.code(str(error))
    
    st.markdown("""
    **Possible solutions:**
    - Check if your document is readable
    - Ensure your API key is configured correctly
    - Try with a smaller document
    - Refresh the page and try again
    """)

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
    max_tokens, confidence_threshold = create_sidebar()
    
    # Main content
    display_header()
    
    # Check API key
    if not GOOGLE_API_KEY:
        st.error("⚠️ Google API key not found. Please configure your .env file.")
        st.stop()
    
    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload section
        doc = display_upload_section()
        
        # Question section
        user_question = display_question_section()
        
        # Submit button
        submit_button = st.button("🚀 Process Document & Answer Question")
        
    with col2:
        # Display document info if uploaded
        if doc is not None:
            st.success("✅ Document uploaded successfully!")
            st.info(f"**Filename:** {doc.name}")
            st.info(f"**Size:** {doc.size} bytes")
            st.info(f"**Type:** {doc.type}")
    
    # Process when button is clicked
    if submit_button:
        if doc is None:
            st.warning("⚠️ Please upload a document first.")
        elif not user_question.strip():
            st.warning("⚠️ Please enter a question.")
        else:
            try:
                # Show processing steps
                progress_container = st.container()
                with progress_container:
                    st.markdown("### 🔄 Processing...")
                    
                    # Step 1: Load data
                    display_processing_status(1, 5)
                    documents = load_data(doc)
                    time.sleep(0.5)  # Small delay for UX
                    
                    # Step 2: Load model
                    display_processing_status(2, 5)
                    model = load_model()
                    time.sleep(0.5)
                    
                    # Step 3: Create embeddings
                    display_processing_status(3, 5)
                    query_engine = gemini_embedding(model, documents)
                    time.sleep(0.5)
                    
                    # Step 4: Process question
                    display_processing_status(4, 5)
                    time.sleep(0.5)
                    
                    # Step 5: Generate response
                    display_processing_status(5, 5)
                    response = query_engine.query(user_question)
                
                # Clear progress and show results
                progress_container.empty()
                
                # Display answer
                display_answer(response)
                
                # Add feedback section
                st.markdown("---")
                st.markdown("### 📝 Feedback")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Helpful"):
                        st.success("Thank you for your feedback!")
                with col2:
                    if st.button("👎 Not Helpful"):
                        st.info("We'll work on improving our responses!")
                        
            except Exception as e:
                show_error_message(e)

if __name__ == "__main__":
    main()