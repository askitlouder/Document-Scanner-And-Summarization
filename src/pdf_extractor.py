from typing import Optional
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF (fitz).
    Returns concatenated text from all pages.
    """
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{text}")
        
        doc.close()
        return "\n\n".join(text_parts)
    
    except Exception as e:
        print(f"Failed to extract text from PDF: {pdf_path}", exc_info=e)
        return ""


def has_extractable_text(pdf_path: str, min_chars: int = 100) -> bool:
    """
    Check if PDF contains extractable text.
    Returns True if text extraction yields meaningful content.
    """
    try:
        doc = fitz.open(pdf_path)
        total_text = ""
        
        # Check first few pages
        pages_to_check = min(3, len(doc))
        for page_num in range(pages_to_check):
            page = doc[page_num]
            total_text += page.get_text()
            if len(total_text) > min_chars:
                doc.close()
                return True
        
        doc.close()
        return len(total_text.strip()) > min_chars
    
    except Exception as e:
        print(f"Failed to check PDF text: {pdf_path}", exc_info=e)
        return False

