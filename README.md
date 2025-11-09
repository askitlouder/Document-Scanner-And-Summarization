# Document Scanner and Summarization System

**Extract text from PDFs/images using OCR and generate AI-powered summaries with Google Gemini LLM**

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure (see Configuration section)
# 3. Launch Web UI (Recommended)
streamlit run app.py

# OR use CLI
python main.py
```

---

## ✨ Key Features

- **Multi-format Support**: PDF, PNG, JPG, JPEG, BMP, TIFF, WEBP
- **Smart Text Extraction**: Native PDF extraction → OCR fallback for scanned docs
- **AI Summarization**: Google Gemini 2.5 Flash with intelligent chunking
- **Two Interfaces**: 
  - 🌐 **Streamlit Web UI** - Drag-and-drop, real-time progress, visual results
  - 💻 **CLI** - Automation and batch processing
- **Image Preprocessing**: Optional denoising and thresholding for better OCR
- **Batch Processing**: Multiple files/folders in single run

---

## 📋 Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR** - [Download](https://github.com/tesseract-ocr/tesseract)
3. **Poppler** (PDF conversion) - [Windows Download](https://github.com/oschwartz10612/poppler-windows)
4. **Google Gemini API Key** - [Get Key](https://makersuite.google.com/app/apikey)

---

## ⚙️ Configuration

### 1. Set Tesseract Path
**File**: `src/ocr.py` (Line 9)
```python
pytesseract.pytesseract.tesseract_cmd = r"YOUR_PATH\tesseract.exe"
```

### 2. Set Gemini API Key
**File**: `src/summarizer.py` (Line 18)
```python
client = genai.Client(api_key="YOUR_API_KEY")
```

### 3. Add Poppler to PATH
- Extract Poppler and add `bin` folder to system PATH
- Restart terminal after adding

---

## 📖 Usage

### Web UI (Recommended)

```bash
streamlit run app.py
```

**Features**:
- 📁 Drag-and-drop file upload
- ⚙️ Configure preprocessing & model in sidebar
- 📊 View results in organized tabs (Extracted Text | Summary)
- 📈 Statistics: character count, word count, page count
- ⬇️ Download results as text files
- ⚠️ Error handling with troubleshooting tips

### Command Line

```bash
python main.py
```

**Configure in `main.py`**:
```python
input_paths = [r"path/to/documents"]  # Files or folders
use_preprocess = False  # True for low-quality images
model_name = "gemini-2.5-flash"
save_text = "extracted_text.txt"  # or None
save_summary = "summary.txt"  # or None
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│  Input: PDF/Images                          │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Step 1: File Resolution                    │
│  • Expand folders → individual files        │
│  • Filter by extensions                     │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Step 2: Text Extraction                    │
│  ┌────────────┐      ┌──────────────┐      │
│  │    PDF     │      │    Images    │      │
│  └─────┬──────┘      └──────┬───────┘      │
│        │                    │              │
│        ├─ Has text? YES → Native Extract   │
│        │                    │              │
│        └─ Has text? NO ──→ OCR             │
│                            ↑               │
│                    Optional Preprocessing  │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Step 3: AI Summarization                   │
│  • Chunk text (3000 chars)                  │
│  • Summarize chunks (Gemini API)            │
│  • Aggregate final summary                  │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Output: Extracted Text + Summary           │
│  • Console display                          │
│  • Optional file saving                     │
└─────────────────────────────────────────────┘
```

---

## 📚 Module Overview

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| **app.py** | Streamlit Web UI | File upload, progress tracking, result display |
| **main.py** | CLI Entry Point | Configuration, pipeline orchestration |
| **document_scanner.py** | Core Pipeline | `scan_and_summarize()`, `extract_text_from_files()` |
| **ocr.py** | OCR Processing | `ocr_images()` - Tesseract integration |
| **pdf_extractor.py** | PDF Text Extraction | `extract_text_from_pdf()`, `has_extractable_text()` |
| **preprocess.py** | Image Enhancement | `preprocess_for_ocr()` - denoising, thresholding |
| **io_utils.py** | File I/O | `images_from_paths()` - load images/PDFs |
| **summarizer.py** | LLM Summarization | `summarize_with_gemini()` - chunking & API calls |

### Module Details

**document_scanner.py** - Core Pipeline
- `get_file_paths(inputs)` → Expand folders, filter by extensions
- `extract_text_from_files(file_paths, use_preprocess)` → Extract text from PDFs/images
- `scan_and_summarize(...)` → Complete end-to-end pipeline

**ocr.py** - OCR Processing
- `ocr_image_tesseract(image, lang='eng', psm=3)` → Single image OCR
- `ocr_images(images, preprocess_fn)` → Batch OCR with optional preprocessing
- **Config**: Set `tesseract_cmd` path at line 9

**pdf_extractor.py** - PDF Handling
- `extract_text_from_pdf(pdf_path)` → Native text extraction (PyMuPDF)
- `has_extractable_text(pdf_path, min_chars=100)` → Check if PDF has text layer

**preprocess.py** - Image Enhancement
- `preprocess_for_ocr(image, denoise=True, resize_max=2000)` → Enhance for OCR
- **Pipeline**: Resize → Grayscale → Denoise → Adaptive Threshold → Morphology

**io_utils.py** - File Operations
- `images_from_paths(paths, dpi=300)` → Load images, convert PDFs to images

**summarizer.py** - AI Summarization
- `summarize_with_gemini(text, model)` → Two-stage summarization
  - Stage 1: Per-chunk summaries (JSON format)
  - Stage 2: Final aggregation (plain text)
- `chunk_text(text, max_chars=3000)` → Smart text splitting
- **Config**: Set `API_KEY` at line 18

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Tesseract Not Found** | Install Tesseract, update path in `ocr.py`, verify with `tesseract --version` |
| **Poppler Not Found** | Install Poppler, add `bin` folder to PATH, restart terminal |
| **Gemini API Error** | Verify API key, check internet, confirm API quota |
| **Poor OCR Results** | Enable preprocessing: `use_preprocess=True`, increase DPI in `io_utils.py` |
| **Memory Issues** | Reduce DPI (line 34 in `io_utils.py`), process files individually |
| **Slow Processing** | Disable preprocessing for high-quality images, reduce DPI |

---

## 📊 Performance Tips

### Best OCR Results
- Use 300 DPI minimum for scans
- Enable preprocessing for poor-quality images only
- Use native PDF extraction when possible

### Faster Processing
- Disable preprocessing for high-quality documents
- Reduce DPI to 200 for draft processing
- Process files in batches of similar types

### Better Summaries
- Ensure clean OCR text
- Adjust chunk size in `summarizer.py` (line 20-40)
- Try different Gemini models: `gemini-1.5-pro` for complex docs

---

## 📁 Project Structure

```
project/
├── app.py                 # Streamlit Web UI
├── main.py                # CLI Entry Point
├── requirements.txt       # Python Dependencies
├── src/
│   ├── document_scanner.py    # Core Pipeline
│   ├── ocr.py                 # Tesseract OCR
│   ├── pdf_extractor.py       # PDF Text Extraction
│   ├── preprocess.py          # Image Enhancement
│   ├── io_utils.py            # File I/O
│   └── summarizer.py          # Gemini LLM API
├── model_binaries/        # Tesseract Installation
└── output_dir/            # Saved Results
```

---

## 🎯 Supported Formats

| Format | Extension | Method |
|--------|-----------|--------|
| PDF (Digital) | `.pdf` | Native (PyMuPDF) |
| PDF (Scanned) | `.pdf` | OCR (Tesseract) |
| Images | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.webp` | OCR (Tesseract) |

---

## 📦 Dependencies

```bash
# Install all at once
pip install -r requirements.txt
```

**Key Libraries**:
- `streamlit>=1.28.0` - Web UI framework
- `opencv-python>=4.7.0` - Image processing
- `pytesseract` - OCR wrapper
- `pdf2image` - PDF conversion
- `PyMuPDF` - PDF text extraction
- `google-genai>=0.6.0` - Gemini API
- `pillow`, `numpy` - Image manipulation

---

## 🌐 Advanced Streamlit Usage

### Run on Network
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
Access from other devices: `http://YOUR_IP:8501`

### Production Deployment
```bash
streamlit run app.py --server.headless true --server.port 8501
```

---

## 🔐 Security Best Practices

⚠️ **Never commit API keys to version control**

**Recommended**: Use environment variables
```python
# summarizer.py
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
```

---

## 💡 Usage Examples

### Example 1: Single File
```python
input_paths = [r"F:\Documents\report.pdf"]
```

### Example 2: Multiple Files
```python
input_paths = [
    r"F:\Documents\report1.pdf",
    r"F:\Images\scan.jpg",
    r"F:\Documents\invoice.png"
]
```

### Example 3: Entire Folder
```python
input_paths = [r"F:\Documents\Reports"]  # Auto-processes all supported files
```

### Example 4: Low-Quality Scans
```python
use_preprocess = True  # Applies denoising & thresholding
```

---

## 📝 Key Notes

- System auto-detects best extraction method per file type
- Native PDF extraction is always preferred (faster, more accurate)
- OCR is fallback for scanned documents/images
- Two-stage summarization handles long documents efficiently
- UTF-8 encoding supports international characters

---

## 📧 Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Google Gemini API](https://ai.google.dev/docs)
- [PyMuPDF Docs](https://pymupdf.readthedocs.io/)

---

## 🎉 Version History

### v1.1 (Current - Nov 8, 2024)
✨ **New Streamlit Web UI**
- Interactive web interface with drag-and-drop
- Real-time progress tracking
- Tabbed results display
- Statistics dashboard
- Download functionality

### v1.0 (Initial Release)
- CLI interface
- Core OCR & summarization pipeline
- Multi-format support

---

**Status**: Production Ready ✅  
**Platforms**: Windows | Linux | macOS  
**License**: See LICENSE file

---

*Built with Tesseract OCR, Google Gemini, and Streamlit*
