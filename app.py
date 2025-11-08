import streamlit as st
import tempfile
import os
from pathlib import Path
from src.document_scanner import scan_and_summarize
import time

# Page configuration
st.set_page_config(
    page_title="Document Scanner & Summarizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📄 Document Scanner & Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Extract text from documents and generate intelligent summaries using AI</div>', unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.markdown("---")
    
    # Preprocessing option
    use_preprocess = st.checkbox(
        "Enable Image Preprocessing",
        value=False,
        help="Enable denoising and thresholding for better OCR on low-quality images"
    )
    
    # Model selection
    model_options = [
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]
    model_name = st.selectbox(
        "Select LLM Model",
        options=model_options,
        index=0,
        help="Choose the Google Gemini model for summarization"
    )
    
    # Save options
    st.markdown("---")
    st.subheader("💾 Save Options")
    
    save_extracted = st.checkbox("Save Extracted Text", value=False)
    save_summary_option = st.checkbox("Save Summary", value=False)
    
    st.markdown("---")
    
    # Supported formats info
    with st.expander("📋 Supported Formats"):
        st.markdown("""
        **Supported File Types:**
        - PDF (`.pdf`)
        - PNG (`.png`)
        - JPEG (`.jpg`, `.jpeg`)
        - BMP (`.bmp`)
        - TIFF (`.tiff`)
        - WebP (`.webp`)
        
        **Processing Methods:**
        - Digital PDFs: Native text extraction
        - Scanned PDFs: OCR via Tesseract
        - Images: OCR via Tesseract
        """)
    
    # About section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Document Scanner & Summarizer**
        
        This application uses:
        - **Tesseract OCR** for text extraction
        - **PyMuPDF** for PDF processing
        - **Google Gemini** for AI summarization
        - **OpenCV** for image preprocessing
        
        Version 1.0
        """)

# Main content area
st.markdown("---")

# File uploader
st.subheader("📁 Upload Documents")
uploaded_files = st.file_uploader(
    "Choose files to process (PDF, Images)",
    type=["pdf", "png", "jpg", "jpeg", "bmp", "tiff", "webp"],
    accept_multiple_files=True,
    help="You can upload multiple files at once"
)

# Display uploaded files
if uploaded_files:
    st.markdown(f'<div class="info-box">✅ {len(uploaded_files)} file(s) uploaded successfully</div>', unsafe_allow_html=True)
    
    with st.expander("📋 View Uploaded Files"):
        for idx, file in enumerate(uploaded_files, 1):
            file_size = len(file.getvalue()) / 1024  # Size in KB
            st.write(f"{idx}. **{file.name}** ({file_size:.2f} KB)")

st.markdown("---")

# Process button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    process_button = st.button("🚀 Start Processing", disabled=not uploaded_files)

# Processing logic
if process_button and uploaded_files:
    # Create temporary directory for uploaded files
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            temp_dir = os.mkdir("output_dir") if not os.path.exists("output_dir") else "output_dir"
            # Save uploaded files to temporary directory
            temp_file_paths = []
            
            with st.spinner("📤 Uploading files..."):
                for uploaded_file in uploaded_files:
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    temp_file_paths.append(temp_file_path)
                time.sleep(0.5)  # Brief pause for user feedback
            
            st.success(f"✅ {len(temp_file_paths)} file(s) uploaded successfully")
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Text Extraction
            status_text.text("🔍 Step 1/3: Extracting text from documents...")
            progress_bar.progress(33)
            
            # Prepare output file paths if saving is enabled
            save_text_path = None
            save_summary_path = None
            
            if save_extracted:
                save_text_path = os.path.join(temp_dir,f"text_{int(time.time()*1000)}.txt")
            
            if save_summary_option:
                save_summary_path = os.path.join(temp_dir,f"summary_{int(time.time()*1000)}.txt")
            
            # Step 2: Processing
            status_text.text("🤖 Step 2/3: Processing with OCR and LLM...")
            progress_bar.progress(66)
            
            # Run the pipeline
            extracted_text, summary = scan_and_summarize(
                input_paths=temp_file_paths,
                use_preprocess=use_preprocess,
                model_name=model_name,
                save_text=save_text_path,
                save_summary=save_summary_path
            )
            
            # Step 3: Complete
            status_text.text("✨ Step 3/3: Finalizing results...")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display success message
            st.markdown('<div class="success-box">✅ Processing completed successfully!</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display results in tabs
            tab1, tab2 = st.tabs(["📝 Extracted Text", "📊 Summary"])
            
            with tab1:
                st.subheader("Extracted Text via OCR")
                
                if extracted_text and extracted_text.strip():
                    # Show character count
                    char_count = len(extracted_text)
                    word_count = len(extracted_text.split())
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Characters", f"{char_count:,}")
                    with col2:
                        st.metric("Words", f"{word_count:,}")
                    with col3:
                        st.metric("Pages", len(uploaded_files))
                    
                    st.markdown("---")
                    
                    # Display text in scrollable box
                    st.text_area(
                        "Full Extracted Text",
                        value=extracted_text,
                        height=400,
                        help="Scroll to view all extracted text"
                    )
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Extracted Text",
                        data=extracted_text,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("⚠️ No text could be extracted from the uploaded files.")
            
            with tab2:
                st.subheader("AI-Generated Summary")
                
                if summary and summary.strip():
                    # Display summary
                    st.markdown(summary)
                    
                    st.markdown("---")
                    
                    # Summary statistics
                    summary_char_count = len(summary)
                    summary_word_count = len(summary.split())
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Summary Characters", f"{summary_char_count:,}")
                    with col2:
                        st.metric("Summary Words", f"{summary_word_count:,}")
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("⚠️ No summary could be generated.")
            
            # Additional actions
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Process Another Document"):
                    st.rerun()
            
        except Exception as e:
            st.error(f"❌ **Error during processing:** {str(e)}")
            st.exception(e)
            
            # Show error details in expander
            with st.expander("🔍 View Error Details"):
                st.code(str(e))
                
            st.info("💡 **Troubleshooting Tips:**\n"
                   "- Ensure Tesseract is installed and path is configured\n"
                   "- Check that Poppler is installed for PDF processing\n"
                   "- Verify Google Gemini API key is valid\n"
                   "- Try enabling preprocessing for low-quality images\n"
                   "- Check file format is supported")

# Instructions section (shown when no files uploaded)
if not uploaded_files:
    st.markdown("---")
    st.info("👆 **Getting Started:** Upload one or more documents using the file uploader above, then click 'Start Processing'")
    
    # Features showcase
    st.subheader("✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📄 Multi-Format Support**
        - PDF documents
        - Image files (PNG, JPG, etc.)
        - Batch processing
        """)
    
    with col2:
        st.markdown("""
        **🔍 Smart Extraction**
        - Native PDF text extraction
        - OCR for scanned documents
        - Image preprocessing
        """)
    
    with col3:
        st.markdown("""
        **🤖 AI Summarization**
        - Google Gemini LLM
        - Bullet point summaries
        - Concise overviews
        """)
    
    st.markdown("---")
    
    # Quick guide
    with st.expander("📖 Quick Guide"):
        st.markdown("""
        ### How to Use:
        
        1. **Upload Files**: Click on the file uploader and select one or more documents
        2. **Configure Settings**: (Optional) Adjust preprocessing and model options in the sidebar
        3. **Start Processing**: Click the "Start Processing" button
        4. **View Results**: Check the extracted text and summary in the results tabs
        5. **Download**: Use download buttons to save results locally
        
        ### Tips for Best Results:
        
        - **For scanned documents**: Enable image preprocessing in settings
        - **For multiple pages**: Upload all pages as separate files or as a single PDF
        - **For better OCR**: Use high-resolution images (300 DPI or higher)
        - **For faster processing**: Disable preprocessing for high-quality images
        
        ### Troubleshooting:
        
        If you encounter errors:
        1. Check that all prerequisites are installed (Tesseract, Poppler)
        2. Verify file formats are supported
        3. Ensure API key is configured correctly
        4. Try processing fewer files at once
        """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; font-size: 0.9rem;">'
    '📄 Document Scanner & Summarizer | Developed BY ASKITLOUD'
    '</div>',
    unsafe_allow_html=True
)

