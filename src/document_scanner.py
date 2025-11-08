from typing import List, Optional, Tuple
from pathlib import Path

from src.io_utils import images_from_paths
from src.pdf_extractor import extract_text_from_pdf, has_extractable_text
from src.preprocess import preprocess_for_ocr
from src.ocr import ocr_images
from src.summarizer import summarize_with_gemini




def get_file_paths(inputs: List[str]) -> List[str]:
    """
    Expand input paths to individual files.
    Handles folders by collecting all supported files inside.
    """
    SUPPORTED_EXTS = (".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")
    files = []
    
    for inp in inputs:
        path = Path(inp)
        if path.is_dir():
            for file in sorted(path.iterdir()):
                if file.suffix.lower() in SUPPORTED_EXTS:
                    files.append(str(file))
        elif path.is_file():
            if path.suffix.lower() in SUPPORTED_EXTS:
                files.append(str(path))
    
    return files


def extract_text_from_files(file_paths: List[str], use_preprocess: bool = True) -> str:
    """
    Extract text from a list of files (PDFs and images).
    For PDFs: tries native text extraction first, falls back to OCR if needed.
    For images: uses OCR with optional preprocessing.
    """
    all_text = []
    
    pdf_files = [f for f in file_paths if f.lower().endswith('.pdf')]
    image_files = [f for f in file_paths if not f.lower().endswith('.pdf')]
    
    # Handle PDFs
    for pdf_path in pdf_files:
        print(f"Processing PDF: {pdf_path}")
        
        # Try native text extraction first
        if has_extractable_text(pdf_path):
            print("  -> Using native PDF text extraction")
            text = extract_text_from_pdf(pdf_path)
            if text.strip():
                all_text.append(text)
        else:
            # Fall back to OCR
            print("  -> PDF has no extractable text, using OCR")
            images = images_from_paths([pdf_path])
            preprocess_fn = preprocess_for_ocr if use_preprocess else None
            text = ocr_images(images, preprocess_fn=preprocess_fn)
            if text.strip():
                all_text.append(text)
    
    # Handle images
    if image_files:
        print(f"Processing {len(image_files)} image(s) with OCR")
        images = images_from_paths(image_files)
        preprocess_fn = preprocess_for_ocr if use_preprocess else None
        text = ocr_images(images, preprocess_fn=preprocess_fn)
        if text.strip():
            all_text.append(text)
    
    return "\n\n".join(all_text)


def scan_and_summarize(
    input_paths: List[str],
    use_preprocess: bool = True,
    model_name: Optional[str] = None,
    save_text: Optional[str] = None,
    save_summary: Optional[str] = None
) -> Tuple[str, str]:
    """
    Complete document scanner pipeline:
    1. Collect all files from input paths
    2. Extract text (using best method for each file type)
    3. Summarize with LLM
    4. Optionally save outputs
    
    Returns: (extracted_text, summary)
    """
    print("Starting document scanner pipeline")
    
    # Expand paths to files
    files = get_file_paths(input_paths)
    print(f"Found {len(files)} file(s) to process")
    
    if not files:
        print("No files found to process")
        return "", ""
    
    # Extract text from file via OCR Model
    extracted_text = extract_text_from_files(files, use_preprocess=use_preprocess)
    print(f"Extracted text length: {len(extracted_text)} chars")
    
    if not extracted_text.strip():
        print("No text extracted from files")
        return "", ""
    
    # Summarize
    print("Generating summary with LLM")
    summary = summarize_with_gemini(extracted_text, model=model_name)
    print(f"Summary generated length: {len(summary)} chars")
    
    # Save outputs if requested
    if save_text:
        Path(save_text).write_text(extracted_text, encoding='utf-8')
        print(f"Saved extracted text -> {save_text}")
    
    if save_summary:
        Path(save_summary).write_text(summary, encoding='utf-8')
        print(f"Saved summary -> {save_summary}")
    
    return extracted_text, summary

