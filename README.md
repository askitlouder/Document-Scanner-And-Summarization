# Document Scanner and Summarization System

A comprehensive document processing pipeline that extracts text from multiple file formats (PDFs, images) using OCR and generates intelligent summaries using Large Language Models (LLMs).

---

## 🎯 Overview

This system provides an end-to-end solution for:
1. **Document Input**: Accepts multiple file formats (PDF, PNG, JPG, JPEG, BMP, TIFF, WEBP)
2. **Text Extraction**: Uses intelligent extraction methods (native PDF extraction or OCR)
3. **Text Summarization**: Leverages Google Gemini LLM for generating concise summaries
4. **Output Management**: Saves extracted text and summaries to files

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure prerequisites** (see [Configuration](#configuration) section)

3. **Launch the web UI:**
   ```bash
   streamlit run app.py
   ```

4. **Upload files and click "Start Processing"** - That's it! 🎉

---

## ✨ Features

### Input Handling
- ✅ Supports multiple file formats (PDF, PNG, JPG, JPEG, BMP, TIFF, WEBP)
- ✅ Batch processing of multiple files
- ✅ Automatic folder scanning for supported files
- ✅ Mixed input types in a single run

### Text Extraction
- ✅ **Smart PDF Processing**: Attempts native text extraction first, falls back to OCR for scanned PDFs
- ✅ **Advanced OCR**: Tesseract-based OCR with configurable parameters
- ✅ **Image Preprocessing**: Optional enhancement (denoising, thresholding) for better OCR accuracy

### Summarization
- ✅ **LLM-Powered**: Uses Google Gemini 2.5 Flash model
- ✅ **Intelligent Chunking**: Automatically splits large documents for processing
- ✅ **Structured Output**: Generates bullet points and concise summaries

### Output Options
- ✅ Console display with formatted results
- ✅ Optional file saving for extracted text
- ✅ Optional file saving for summaries
- ✅ UTF-8 encoding support

---

## 🏗️ System Architecture

```
                    ┌──────────────────────────┐
                    │   USER INTERFACES        │
                    │                          │
         ┌──────────┴──────────┬───────────────┴──────────┐
         │                     │                          │
         ▼                     ▼                          ▼
┌─────────────────┐  ┌─────────────────┐     ┌──────────────────┐
│  STREAMLIT UI   │  │   CLI SCRIPT    │     │   API (Future)   │
│    (app.py)     │  │   (main.py)     │     │   Integration    │
│                 │  │                 │     │                  │
│ • File Upload   │  │ • Batch Process │     │ • REST API       │
│ • Progress Bar  │  │ • Automation    │     │ • Webhooks       │
│ • Results View  │  │ • Scripting     │     │                  │
└────────┬────────┘  └────────┬────────┘     └──────────────────┘
         │                    │
         └──────────┬─────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENT SCANNER PIPELINE                    │
│                    (document_scanner.py)                        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 1: File Path Resolution (get_file_paths)          │  │
│  │  • Expand directories to individual files               │  │
│  │  • Filter by supported extensions                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 2: Text Extraction (extract_text_from_files)      │  │
│  │                                                          │  │
│  │    ┌─────────────┐         ┌─────────────┐             │  │
│  │    │  PDF Files  │         │ Image Files │             │  │
│  │    └──────┬──────┘         └──────┬──────┘             │  │
│  │           │                       │                     │  │
│  │           ▼                       ▼                     │  │
│  │  ┌───────────────┐      ┌──────────────────┐           │  │
│  │  │ Check Text    │      │ Load Images      │           │  │
│  │  │ Extractable?  │      │ (io_utils.py)    │           │  │
│  │  └───┬───────┬───┘      └────────┬─────────┘           │  │
│  │      │       │                   │                     │  │
│  │  YES │       │ NO                │                     │  │
│  │      │       │                   │                     │  │
│  │      ▼       │                   ▼                     │  │
│  │  ┌─────────┐ │         ┌──────────────────┐           │  │
│  │  │ Native  │ │         │  Preprocessing   │           │  │
│  │  │ Extract │ │         │  (Optional)      │           │  │
│  │  │ (PyMuPDF)│ │        │ (preprocess.py)  │           │  │
│  │  └─────────┘ │         └────────┬─────────┘           │  │
│  │              │                   │                     │  │
│  │              └──────┬────────────┘                     │  │
│  │                     │                                  │  │
│  │                     ▼                                  │  │
│  │            ┌─────────────────┐                         │  │
│  │            │  OCR Processing │                         │  │
│  │            │  (Tesseract)    │                         │  │
│  │            │  (ocr.py)       │                         │  │
│  │            └─────────────────┘                         │  │
│  │                     │                                  │  │
│  │                     ▼                                  │  │
│  │            ┌─────────────────┐                         │  │
│  │            │ Concatenated    │                         │  │
│  │            │ Extracted Text  │                         │  │
│  │            └─────────────────┘                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 3: Summarization (summarizer.py)                  │  │
│  │                                                          │  │
│  │  • Text Chunking (3000 chars per chunk)                 │  │
│  │  • Per-chunk Summarization (Gemini API)                 │  │
│  │  • Final Summary Aggregation                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 4: Output Management                               │  │
│  │                                                          │  │
│  │  • Save extracted text (optional)                        │  │
│  │  • Save summary (optional)                               │  │
│  │  • Return results to main                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT DISPLAY                             │
│  • Console output with formatted sections                       │
│  • Extracted text preview (first 500 chars)                     │
│  • Complete summary display                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Module Documentation

### 1. `app.py` - Streamlit Web UI (NEW!)
**Purpose**: Interactive web-based user interface for document scanning and summarization

**Key Features**:
- 📁 **File Upload**: Drag-and-drop or browse multiple files
- ⚙️ **Settings Panel**: Configure preprocessing, model selection, and save options
- 🚀 **One-Click Processing**: Start entire pipeline with single button
- 📊 **Tabbed Results**: Organized display of extracted text and summary
- 📈 **Real-time Progress**: Visual feedback with progress bars and status messages
- 💾 **Download Options**: Export results as text files
- 📋 **Statistics Display**: Character count, word count, and page metrics
- ⚠️ **Error Handling**: User-friendly error messages with troubleshooting tips

#### UI Components:

**Main Header Section**:
- Application title and description
- Custom styled interface with modern design

**Sidebar (Settings Panel)**:
```python
# Configuration Options:
- Enable Image Preprocessing (checkbox)
  • Enables denoising and thresholding for better OCR
  
- Select LLM Model (dropdown)
  • gemini-2.5-flash (default)
  • gemini-1.5-flash
  • gemini-1.5-pro
  
- Save Options (checkboxes)
  • Save Extracted Text
  • Save Summary
  
- Information Sections
  • Supported Formats (expandable)
  • About (expandable)
```

**File Upload Area**:
- Multi-file uploader supporting all document formats
- Visual confirmation of uploaded files with size information
- Expandable list showing all uploaded file names

**Processing Button**:
- Large, centered "Start Processing" button
- Disabled state when no files uploaded
- Triggers complete pipeline execution

**Progress Indicators**:
```python
Step 1/3: Extracting text from documents... (33%)
Step 2/3: Processing with OCR and LLM... (66%)
Step 3/3: Finalizing results... (100%)
```

**Results Display (Tabbed Interface)**:

**Tab 1: 📝 Extracted Text**
- Character count metric
- Word count metric
- Page count metric
- Scrollable text area with full extracted content
- Download button for text file

**Tab 2: 📊 Summary**
- Formatted AI-generated summary display
- Summary character count
- Summary word count
- Download button for summary file

#### Technical Implementation:

**File Handling**:
```python
# Temporary file management
with tempfile.TemporaryDirectory() as temp_dir:
    # Save uploaded files to temp directory
    for uploaded_file in uploaded_files:
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    # Process files
    extracted_text, summary = scan_and_summarize(
        input_paths=temp_file_paths,
        use_preprocess=use_preprocess,
        model_name=model_name,
        save_text=save_text_path,
        save_summary=save_summary_path
    )
```

**State Management**:
- Uses Streamlit session state for configuration persistence
- Automatic cleanup of temporary files after processing
- Responsive UI updates based on user actions

**Error Handling**:
- Try-catch blocks for robust error management
- Detailed error messages in expandable sections
- Troubleshooting tips displayed on errors

**Custom Styling**:
- CSS injection for modern, professional appearance
- Color-coded status boxes (success, info, warning)
- Responsive layout with columns for better organization

#### User Workflow:

1. **Launch Application**: `streamlit run app.py`
2. **Configure Settings** (optional): Adjust preprocessing and model in sidebar
3. **Upload Files**: Click file uploader, select documents
4. **Review Uploaded Files**: Check file list in expandable section
5. **Start Processing**: Click "Start Processing" button
6. **Monitor Progress**: Watch real-time progress bar (3 steps)
7. **View Results**: Switch between "Extracted Text" and "Summary" tabs
8. **Download Results**: Use download buttons to save outputs
9. **Process More**: Click "Process Another Document" to restart

#### UI Sections:

**Getting Started Panel** (shown when no files uploaded):
- Upload instructions
- Key features showcase (3-column layout)
- Quick guide (expandable)
- Tips for best results
- Troubleshooting section

**Features Showcase**:
```
Column 1: Multi-Format Support
  • PDF documents
  • Image files (PNG, JPG, etc.)
  • Batch processing

Column 2: Smart Extraction
  • Native PDF text extraction
  • OCR for scanned documents
  • Image preprocessing

Column 3: AI Summarization
  • Google Gemini LLM
  • Bullet point summaries
  • Concise overviews
```

#### Page Configuration:
```python
st.set_page_config(
    page_title="Document Scanner & Summarizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Benefits of Streamlit UI**:
- ✅ No coding required for end users
- ✅ Visual feedback at every step
- ✅ Easy file management (no manual path configuration)
- ✅ Immediate result visualization
- ✅ Mobile-responsive design
- ✅ Shareable via network (can run on server)
- ✅ Professional appearance for demonstrations

**Performance Optimizations**:
- Temporary file cleanup
- Lazy loading of results
- Efficient state management
- Minimal re-rendering with Streamlit caching

---

### 2. `main.py` - CLI Entry Point
**Purpose**: Application entry point and user configuration

**Key Functions**:
- `main()`: Orchestrates the entire pipeline

**Configuration Options**:
- `input_paths`: List of file/folder paths to process
- `use_preprocess`: Enable/disable image preprocessing (Boolean)
- `model_name`: LLM model identifier (default: "gemini-2.5-flash")
- `save_text`: Filename to save extracted text (optional)
- `save_summary`: Filename to save summary (optional)

**Output**:
- Console display with extracted text preview
- Console display with full summary
- Optional file outputs

---

### 3. `document_scanner.py` - Core Pipeline
**Purpose**: Main orchestration and document processing logic

#### Functions:

**`get_file_paths(inputs: List[str]) -> List[str]`**
- Expands input paths to individual files
- Handles folder inputs by scanning for supported files
- Supported extensions: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.webp`
- Returns: List of absolute file paths

**`extract_text_from_files(file_paths: List[str], use_preprocess: bool) -> str`**
- Main text extraction router
- **PDF Processing**:
  - Checks if PDF has extractable text using `has_extractable_text()`
  - Uses native extraction if available (faster, more accurate)
  - Falls back to OCR for scanned/image-based PDFs
- **Image Processing**:
  - Loads images via `images_from_paths()`
  - Applies optional preprocessing
  - Performs OCR using Tesseract
- Returns: Concatenated text from all files

**`scan_and_summarize(input_paths, use_preprocess, model_name, save_text, save_summary) -> Tuple[str, str]`**
- Complete end-to-end pipeline
- Steps:
  1. Collect files from input paths
  2. Extract text from all files
  3. Generate summary using LLM
  4. Save outputs if requested
- Returns: (extracted_text, summary)

---

### 4. `io_utils.py` - Input/Output Utilities
**Purpose**: File loading and image conversion

#### Functions:

**`images_from_paths(paths: List[str], dpi: int = 300) -> List[Image.Image]`**
- Converts various input types to PIL images
- **Handles**:
  - **Folders**: Automatically loads all supported images
  - **PDFs**: Converts each page to an image (300 DPI default)
  - **Images**: Opens and converts to RGB format
- Uses `pdf2image` library for PDF conversion
- Returns: List of PIL Image objects ready for OCR

**Configuration**:
- `dpi`: Resolution for PDF-to-image conversion (higher = better quality, slower)
- Supported image formats: PNG, JPG, JPEG, BMP, TIFF, WEBP

---

### 5. `pdf_extractor.py` - PDF Text Extraction
**Purpose**: Native PDF text extraction using PyMuPDF

#### Functions:

**`extract_text_from_pdf(pdf_path: str) -> str`**
- Extracts native text layer from PDF
- Processes all pages sequentially
- Adds page markers for multi-page documents
- Returns: Formatted text with page separators

**`has_extractable_text(pdf_path: str, min_chars: int = 100) -> bool`**
- Checks if PDF contains meaningful extractable text
- Examines first 3 pages for efficiency
- Minimum character threshold: 100 (configurable)
- Returns: True if text extraction is viable

**Use Case**: 
- Digital PDFs with text layers → Fast native extraction
- Scanned PDFs without text → Triggers OCR fallback

---

### 6. `preprocess.py` - Image Preprocessing
**Purpose**: Enhance image quality for better OCR accuracy

#### Functions:

**`preprocess_for_ocr(pil_img: Image.Image, denoise=True, resize_max=2000) -> Image.Image`**

**Processing Steps**:
1. **Resize**: Scales down large images (max dimension: 2000px)
2. **Grayscale Conversion**: Converts to single-channel
3. **Denoising**: Applies Non-Local Means Denoising (optional)
   - Template window: 7x7
   - Search window: 21x21
   - Filter strength: 10
4. **Adaptive Thresholding**: Gaussian adaptive threshold
   - Block size: 15x15
   - C constant: 8
5. **Morphological Operations**: Opening operation to remove noise
   - Kernel: 1x1 rectangular

**Helper Functions**:
- `pil_to_cv2()`: PIL Image → OpenCV format
- `cv2_to_pil()`: OpenCV format → PIL Image

**When to Use**:
- Low-quality scans
- Images with noise or artifacts
- Uneven lighting conditions

---

### 7. `ocr.py` - OCR Processing
**Purpose**: Text extraction from images using Tesseract OCR.
- Download tesseract from above informations and installed it within or code directory within folder named as "model_binaries" or with any name.
Once installation gets completed then provide its path within a code module named as ocr.py 

#### Configuration:
```python
tesseract_cmd = r"F:\ASKITLOUD\OpenCVProjects\Document_Scanner_Summerisation\model_binaries\tesseract.exe"
```


#### Functions:

**`ocr_image_tesseract(pil_img: Image.Image, lang='eng', psm=3, oem=3) -> str`**
- Performs OCR on a single image
- **Parameters**:
  - `lang`: Language model (default: 'eng')
  - `psm`: Page Segmentation Mode (3 = fully automatic)
  - `oem`: OCR Engine Mode (3 = default)
- Returns: Extracted text string

**`ocr_images(images: List[Image.Image], preprocess_fn=None) -> str`**
- Batch OCR processing for multiple images
- Applies optional preprocessing function to each image
- Concatenates results with double newlines
- Returns: Combined text from all images

**Page Segmentation Modes (PSM)**:
- `0`: Orientation and script detection only
- `3`: Fully automatic page segmentation (default)
- `6`: Assume uniform block of text
- `11`: Sparse text. Find as much text as possible

---

### 8. `summarizer.py` - LLM Summarization
**Purpose**: Generate intelligent summaries using Google Gemini API

#### Configuration:
```python
DEFAULT_MODEL = "gemini-2.5-flash"
API_KEY = "API_KEY"  # Replace with your key
```

#### Functions:

**`make_client() -> genai.Client`**
- Creates Google Gemini API client
- Uses API key authentication
- Returns: Configured client instance

**`chunk_text(text: str, max_chars: int = 3000) -> List[str]`**
- Splits large text into manageable chunks
- Attempts smart splitting at:
  1. Double newlines (paragraph breaks)
  2. Sentence endings (`. `)
  3. Hard character limit (fallback)
- Returns: List of text chunks

**`summarize_with_gemini(text: str, model: str = DEFAULT_MODEL) -> str`**

**Two-Stage Summarization Process**:

**Stage 1: Per-Chunk Summarization**
- Each chunk is processed with prompt:
  ```
  Summarize into concise bullet points and 2-5 sentence summary.
  Output JSON with keys: 'summary' and 'bullets'.
  ```
- Handles chunks independently
- Generates structured intermediate summaries

**Stage 2: Final Aggregation**
- Combines all chunk summaries
- Generates final output with prompt:
  ```
  Combine into:
  1) 4-6 sentence concise summary
  2) Combined ordered list of key bullet points (max 12 bullets)
  ```
- Returns: Plain text final summary

---

## 🚀 Installation

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR**
   - Download from: https://github.com/tesseract-ocr/tesseract
   - Update path in `ocr.py` line 9
3. **Poppler** (for PDF to image conversion)
   - Windows: Download from https://github.com/oschwartz10612/poppler-windows
   - Add to system PATH
4. **Google Gemini API Key**
   - Get from: https://makersuite.google.com/app/apikey
   - Update in `summarizer.py` line 18

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies Breakdown:

**UI & Web Framework:**
- `streamlit>=1.28.0`: Interactive web UI framework (NEW!)

**Document Processing:**
- `opencv-python>=4.7.0`: Image processing and preprocessing
- `pillow`: Image loading and manipulation
- `pytesseract`: Tesseract OCR Python wrapper
- `pdf2image`: PDF to image conversion
- `PyMuPDF`: Native PDF text extraction

**AI & LLM:**
- `google-genai>=0.6.0`: Google Gemini API client

**Utilities:**
- `numpy`: Numerical operations for image processing
- `tqdm`: Progress bars (optional)
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests
- `langchain>=0.0.330`: LLM helpers and chunking (optional)

---

## ⚙️ Configuration

### 1. Update Tesseract Path
Edit `ocr.py` line 9:
```python
pytesseract.pytesseract.tesseract_cmd = r"YOUR_PATH\tesseract.exe"
```

### 2. Update Google Gemini API Key
Edit `summarizer.py` line 18:
```python
client = genai.Client(api_key="YOUR_API_KEY")
```

### 3. Configure Input and Options
Edit `main.py`:
```python
# Input files/folders
input_paths = [r"path/to/your/documents"]

# Processing options
use_preprocess = False  # True for better OCR on poor quality images
model_name = "gemini-2.5-flash"  # LLM model
save_text = "extracted_text.txt"  # or None to skip
save_summary = "summary.txt"  # or None to skip
```

---

## 📖 Usage

### Option 1: Web UI (Streamlit) - Recommended

Launch the interactive web interface:

```bash
streamlit run app.py
```

This will open a web browser with an intuitive interface where you can:
- 📁 Upload multiple files via drag-and-drop or file browser
- ⚙️ Configure preprocessing and model settings
- 🚀 Start processing with a single click
- 📊 View results in organized tabs
- ⬇️ Download extracted text and summaries

**Features of the Streamlit UI:**
- Beautiful, user-friendly interface
- Real-time progress indicators
- Statistics (character count, word count)
- Side-by-side comparison of extracted text and summary
- Download buttons for results
- Error handling with troubleshooting tips
- No coding required!

### Option 2: Command Line (Python Script)

For automated or batch processing:

```bash
python main.py
```

### Expected Output:

```
Processing: ['path/to/document.pdf']
Starting document scanner pipeline
Found 1 file(s) to process
Processing PDF: path/to/document.pdf
  -> Using native PDF text extraction
Extracted text length: 5432 chars
Generating summary with LLM
Text split into 2 chunks for summarization.
Summary generated length: 856 chars
Saved extracted text -> extracted_text.txt
Saved summary -> summary.txt

==================================================
EXTRACTED TEXT VIA OCR MODEL
==================================================
[First 500 characters of extracted text]...

==================================================
SUMMARY OF DOCUMENT CONTENT VIA LLMs
==================================================
[Complete summary with bullet points]
==================================================

Document scanning completed successfully
```

### Advanced Usage Examples

#### Example 1: Process Multiple Files
```python
input_paths = [
    r"F:\Documents\report1.pdf",
    r"F:\Documents\report2.pdf",
    r"F:\Images\scan.jpg"
]
```

#### Example 2: Process Entire Folder
```python
input_paths = [r"F:\Documents\Reports"]
# Automatically processes all supported files
```

#### Example 3: Enable Preprocessing for Low-Quality Scans
```python
use_preprocess = True  # Applies denoising and thresholding
```

#### Example 4: Custom Output Files
```python
save_text = "outputs/extracted_2024_11_08.txt"
save_summary = "outputs/summary_2024_11_08.txt"
```

---

## 🔄 Code Flow

### Detailed Execution Flow

```
1. USER RUNS main.py
   │
   ├─> Loads configuration (paths, options)
   │
   └─> Calls scan_and_summarize()
       │
       ├─> Step 1: FILE RESOLUTION (get_file_paths)
       │   ├─> Expands folders to file lists
       │   ├─> Filters by supported extensions
       │   └─> Returns list of absolute paths
       │
       ├─> Step 2: TEXT EXTRACTION (extract_text_from_files)
       │   │
       │   ├─> FOR EACH PDF:
       │   │   ├─> Check if text extractable (has_extractable_text)
       │   │   │   ├─> YES: Use PyMuPDF extraction (fast)
       │   │   │   └─> NO: Convert to images → Preprocess → OCR
       │   │   └─> Append to all_text
       │   │
       │   ├─> FOR IMAGE FILES:
       │   │   ├─> Load images (images_from_paths)
       │   │   ├─> Optional preprocessing (preprocess_for_ocr)
       │   │   ├─> Perform OCR (ocr_images)
       │   │   └─> Append to all_text
       │   │
       │   └─> Return concatenated text
       │
       ├─> Step 3: SUMMARIZATION (summarize_with_gemini)
       │   │
       │   ├─> Chunk text (3000 chars per chunk)
       │   │
       │   ├─> FOR EACH CHUNK:
       │   │   ├─> Send to Gemini API
       │   │   ├─> Get structured summary (JSON)
       │   │   └─> Store chunk summary
       │   │
       │   ├─> Combine chunk summaries
       │   │
       │   ├─> Send combined summaries to Gemini
       │   │
       │   └─> Return final aggregated summary
       │
       ├─> Step 4: OUTPUT MANAGEMENT
       │   ├─> Save extracted text to file (if requested)
       │   ├─> Save summary to file (if requested)
       │   └─> Return (extracted_text, summary)
       │
       └─> Display results in console
           ├─> Extracted text preview
           └─> Complete summary
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Tesseract Not Found
**Error**: `TesseractNotFoundError`

**Solution**:
- Install Tesseract OCR
- Update path in `ocr.py` line 9
- Verify installation: `tesseract --version`

#### 2. Poppler Not Found
**Error**: `Unable to get page count. Is poppler installed?`

**Solution**:
- Install Poppler utilities
- Add poppler `bin` folder to system PATH
- Restart terminal/IDE

#### 3. Google Gemini API Error
**Error**: `Failed creating genai client`

**Solution**:
- Verify API key is valid
- Check internet connection
- Ensure you have API quota remaining
- Verify API is enabled in Google Cloud Console

#### 4. Poor OCR Results
**Issue**: Garbled or incomplete text extraction

**Solution**:
- Enable preprocessing: `use_preprocess = True`
- Increase image resolution (DPI) in `io_utils.py`
- Verify image quality
- Try different Tesseract PSM modes in `ocr.py`

#### 5. Memory Issues with Large PDFs
**Issue**: System runs out of memory

**Solution**:
- Process files individually instead of batch
- Reduce PDF-to-image DPI (line 34 in `io_utils.py`)
- Close other applications

#### 6. Slow Processing
**Issue**: Takes too long to process documents

**Optimization**:
- Disable preprocessing if images are high quality
- Use native PDF extraction when possible
- Reduce image resolution
- Process fewer files per batch

---

## 📊 Performance Tips

### For Best OCR Results:
1. Use high-resolution scans (300 DPI minimum)
2. Ensure good lighting and contrast
3. Enable preprocessing for poor-quality images
4. Use native PDF extraction when available

### For Faster Processing:
1. Disable preprocessing for high-quality images
2. Reduce PDF-to-image DPI to 200 for drafts
3. Use batch processing for similar document types
4. Keep Tesseract language data minimal (only needed languages)

### For Better Summaries:
1. Ensure OCR text is clean and accurate
2. Adjust chunk size in `summarizer.py` based on document structure
3. Experiment with different Gemini models
4. Provide context-specific prompts if needed

---

## 📁 File Structure

```
codebase/
│
├── app.py                 # Streamlit web UI (NEW!)
├── main.py                # CLI entry point and configuration
├── document_scanner.py    # Core pipeline orchestration
├── io_utils.py            # File loading and image conversion
├── pdf_extractor.py       # Native PDF text extraction
├── preprocess.py          # Image preprocessing for OCR
├── ocr.py                 # Tesseract OCR integration
├── summarizer.py          # Google Gemini LLM summarization
├── requirements.txt       # Python dependencies
├── __init__.py            # Package initialization
└── README.md              # This documentation file
```

### File Descriptions

**User Interfaces:**
- `app.py` - Interactive Streamlit web application with file upload and result display
- `main.py` - Command-line interface for automated/batch processing

**Core Modules:**
- `document_scanner.py` - Pipeline orchestration and coordination
- `ocr.py` - Tesseract OCR text extraction
- `pdf_extractor.py` - Native PDF text extraction (PyMuPDF)
- `summarizer.py` - LLM-based summarization (Google Gemini)

**Utility Modules:**
- `io_utils.py` - File I/O and image loading
- `preprocess.py` - Image enhancement for better OCR

---

## 🎯 Supported File Formats

| Format | Extension | Extraction Method |
|--------|-----------|------------------|
| PDF (Digital) | `.pdf` | Native text extraction (PyMuPDF) |
| PDF (Scanned) | `.pdf` | OCR via Tesseract |
| PNG | `.png` | OCR via Tesseract |
| JPEG | `.jpg`, `.jpeg` | OCR via Tesseract |
| BMP | `.bmp` | OCR via Tesseract |
| TIFF | `.tiff` | OCR via Tesseract |
| WebP | `.webp` | OCR via Tesseract |

---

## 🌐 Advanced Streamlit Usage

### Running on Network (Remote Access)

To access the Streamlit UI from other devices on your network:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Then access from any device on the same network using:
```
http://YOUR_IP_ADDRESS:8501
```

### Deployment Options

**Local Development:**
```bash
streamlit run app.py
```

**Production/Server:**
```bash
streamlit run app.py --server.headless true --server.port 8501
```

**With Custom Configuration:**
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### Streamlit Features Utilized:

1. **File Uploader**: Multi-file drag-and-drop support
2. **Progress Bars**: Real-time processing feedback
3. **Tabs**: Organized result display
4. **Metrics**: Visual statistics (character count, word count)
5. **Download Buttons**: Export results directly from browser
6. **Expanders**: Collapsible information sections
7. **Sidebar**: Persistent configuration panel
8. **Custom CSS**: Professional styling and theming
9. **Error Handling**: User-friendly error messages

---

## 🔐 Security Notes

⚠️ **Important**: The API key is currently hardcoded in `summarizer.py`. For production use:
1. Use environment variables
2. Implement secure key management
3. Never commit API keys to version control

Example using environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
```

---

## 📝 Notes

- The system automatically detects the best extraction method for each file type
- Native PDF extraction is preferred for speed and accuracy
- OCR is used as a fallback for scanned documents and images
- Preprocessing should only be enabled for low-quality images to avoid unnecessary processing time
- The summarization uses a two-stage approach for handling long documents effectively
- All text processing uses UTF-8 encoding for international character support

---

## 🤝 Contributing

This is a working codebase. When making modifications:
1. Test with various document types and qualities
2. Verify OCR accuracy with sample documents
3. Check memory usage with large files
4. Validate API integration and error handling

---

## 📧 Support

For issues related to:
- **Streamlit**: https://docs.streamlit.io/
- **Tesseract**: https://github.com/tesseract-ocr/tesseract
- **Google Gemini API**: https://ai.google.dev/docs
- **PyMuPDF**: https://pymupdf.readthedocs.io/
- **OpenCV**: https://docs.opencv.org/

---

## 🎉 What's New

### Version 1.1 (Latest - November 8, 2024)
✨ **Major Addition: Streamlit Web UI**
- 🌐 New `app.py` - Interactive web-based interface
- 📁 Drag-and-drop file upload
- 📊 Real-time progress tracking with visual indicators
- 🎨 Professional UI with tabbed results display
- 📈 Statistics dashboard (character/word counts)
- ⬇️ One-click download for extracted text and summaries
- ⚙️ Configurable settings in sidebar (preprocessing, model selection)
- 📱 Mobile-responsive design
- ⚠️ Enhanced error handling with troubleshooting tips

**Documentation Improvements:**
- Complete module documentation for all 8 modules
- Detailed Streamlit UI component descriptions
- User workflow guides
- Advanced deployment options
- Updated system architecture diagram

### Version 1.0 (Initial Release)
- CLI interface via `main.py`
- Core document scanning pipeline
- OCR integration (Tesseract)
- LLM summarization (Google Gemini)
- Multi-format support (PDF, images)
- Image preprocessing capabilities

---

## 📦 Version Information

**Current Version**: 1.1  
**Release Date**: November 8, 2024  
**Status**: Production Ready ✅

**Available Interfaces:**
- 🌐 **Web UI** (Streamlit) - `streamlit run app.py` - Recommended for most users
- 💻 **CLI** (Python) - `python main.py` - For automation and scripting

**Supported Platforms:**
- Windows ✅
- Linux ✅
- macOS ✅

---



