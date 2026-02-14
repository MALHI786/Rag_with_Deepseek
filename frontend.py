import streamlit as st
from datetime import datetime
import io
import os
from dotenv import load_dotenv
from rag_pipeline import RAGApplication

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot with DeepSeek",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    
    /* Chat message styling */
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .bot-message {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
    }
    
    /* Upload section styling */
    .upload-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #ccc;
        margin-bottom: 1rem;
    }
    
    /* Success message */
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    /* Warning message */
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 20px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_uploaded' not in st.session_state:
    st.session_state.pdf_uploaded = False
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = None
if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = None
if 'rag_app' not in st.session_state:
    st.session_state.rag_app = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False

# Sidebar for PDF upload
with st.sidebar:
    st.title("📚 Document Upload")
    st.markdown("---")
    
    # Upload section with custom styling
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### Upload Your PDF")
    st.markdown("Upload a PDF document to start chatting (max 100MB)")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        accept_multiple_files=False,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle file upload
    if uploaded_file is not None:
        # Check file size (100MB = 104857600 bytes)
        file_size = uploaded_file.size
        max_size = 100 * 1024 * 1024  # 100MB in bytes
        
        if file_size > max_size:
            st.error(f"❌ File size ({file_size / (1024*1024):.2f}MB) exceeds the 100MB limit!")
            st.session_state.pdf_uploaded = False
            st.session_state.pdf_name = None
            st.session_state.pdf_content = None
        else:
            # Store PDF information
            st.session_state.pdf_uploaded = True
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.pdf_content = uploaded_file.read()
            
            # Display success message
            st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")
            st.info(f"📄 Size: {file_size / (1024*1024):.2f}MB")
            
            # Process PDF button
            if not st.session_state.pdf_processed:
                if st.button("🚀 Process PDF", use_container_width=True, type="primary"):
                    st.session_state.processing = True
                    st.rerun()
            
            # Clear chat button
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
            
            # Remove PDF button
            if st.button("❌ Remove PDF", use_container_width=True):
                st.session_state.pdf_uploaded = False
                st.session_state.pdf_name = None
                st.session_state.pdf_content = None
                st.session_state.chat_history = []
                st.session_state.rag_app = None
                st.session_state.pdf_processed = False
                st.rerun()
    else:
        if st.session_state.pdf_uploaded:
            # PDF was uploaded before but now removed
            st.session_state.pdf_uploaded = False
            st.session_state.pdf_name = None
            st.session_state.pdf_content = None
            st.session_state.chat_history = []
            st.session_state.rag_app = None
            st.session_state.pdf_processed = False
    
    # Display upload status
    st.markdown("---")
    st.markdown("### 📊 Status")
    if st.session_state.pdf_processed:
        st.markdown(f"""
        <div class="success-box">
            <strong>✓ Ready to Chat</strong><br>
            Document: {st.session_state.pdf_name}<br>
            Status: Processed & Indexed
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.pdf_uploaded:
        st.markdown(f"""
        <div class="warning-box">
            <strong>⚠️ PDF Uploaded</strong><br>
            Click "Process PDF" to enable chatting
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ No Document Loaded</strong><br>
            Please upload a PDF to start chatting
        </div>
        """, unsafe_allow_html=True)
    
    # Info section
    st.markdown("---")
    st.markdown("### ℹ️ Instructions")
    st.markdown("""
    1. Upload a PDF document (max 100MB)
    2. Wait for processing confirmation
    3. Start asking questions about your document
    4. Get AI-powered answers
    """)

# Process PDF if needed
if st.session_state.processing:
    with st.spinner("🔄 Processing PDF... This may take a minute..."):
        try:
            # Get Groq API key
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                st.error("❌ GROQ_API_KEY not found. Please set it in .env file")
                st.session_state.processing = False
                st.stop()
            
            # Initialize RAG application
            ollama_model = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")
            groq_model = os.getenv("GROQ_MODEL", "deepseek-r1-distill-llama-70b")
            
            st.session_state.rag_app = RAGApplication(
                groq_api_key=groq_api_key,
                ollama_model=ollama_model,
                groq_model=groq_model
            )
            
            # Process the PDF
            result = st.session_state.rag_app.process_pdf(
                st.session_state.pdf_content,
                st.session_state.pdf_name
            )
            
            st.session_state.pdf_processed = True
            st.session_state.processing = False
            
            st.success(f"✅ PDF processed successfully! {result['num_chunks']} chunks created.")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
            st.session_state.processing = False
            st.session_state.rag_app = None

# Main chat interface
st.title("💬 RAG Chatbot with DeepSeek")
st.markdown("Ask questions about your uploaded document and get intelligent answers!")
st.markdown("---")

# Display chat history
chat_container = st.container()
with chat_container:
    if len(st.session_state.chat_history) == 0:
        st.info("👋 Welcome! Upload a PDF document in the sidebar to start chatting.")
    else:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="user-message">
                    <strong>🧑 You:</strong><br>
                    {message['content']}
                    <div style="text-align: right; font-size: 0.8em; color: #666; margin-top: 0.5rem;">
                        {message['timestamp']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <strong>🤖 Assistant:</strong><br>
                    {message['content']}
                    <div style="text-align: right; font-size: 0.8em; color: #666; margin-top: 0.5rem;">
                        {message['timestamp']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Chat input section
st.markdown("---")

# Create input form
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Your question:",
            placeholder="Type your question here..." if st.session_state.pdf_processed else "Please upload and process a PDF first...",
            disabled=not st.session_state.pdf_processed,
            label_visibility="collapsed"
        )
    
    with col2:
        submit_button = st.form_submit_button(
            "Send 📤",
            use_container_width=True,
            disabled=not st.session_state.pdf_processed
        )

# Handle message submission
if submit_button and user_input:
    if st.session_state.pdf_processed and st.session_state.rag_app:
        # Get current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add user message to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        
        # Get answer from RAG pipeline
        with st.spinner("🤔 Thinking..."):
            try:
                bot_response = st.session_state.rag_app.ask_question(user_input)
                # Add debug info about retrieval
                with st.expander("🔍 Debug: Retrieved Context", expanded=False):
                    st.info(f"Retrieved 8 chunks from the document for analysis")
            except Exception as e:
                bot_response = f"❌ Error generating response: {str(e)}"
        
        # Add bot response to chat history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': bot_response,
            'timestamp': timestamp
        })
        
        # Rerun to update the chat display
        st.rerun()
    else:
        st.error("⚠️ Please upload and process a PDF document first!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p>Powered by DeepSeek AI | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
