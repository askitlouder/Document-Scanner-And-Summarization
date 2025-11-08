# import os
# from typing import List
# from pdf2image import convert_from_path
# from PIL import Image

# def images_from_paths(paths: List[str], dpi: int = 300) -> List[Image.Image]:
#     """
#     Accepts a list of file paths (images or PDFs).
#     Returns a list of PIL Image objects for OCR.
#     """
#     imgs = []
#     for p in paths:
#         p = os.path.abspath(p)
#         if p.lower().endswith('.pdf'):
#             # Convert each PDF page to an image
#             pages = convert_from_path(p, dpi=dpi)  # requires poppler on system
#             imgs.extend(pages)
#         else:
#             imgs.append(Image.open(p).convert('RGB'))
#     return imgs

import os
import logging
from typing import List
from pdf2image import convert_from_path
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")


def images_from_paths(paths: List[str], dpi: int = 300) -> List[Image.Image]:
    """
    Accepts file or folder paths.
    - If folder: auto-loads all images inside it.
    - If PDF: convert pages to images (for OCR fallback).
    - Else: open image file.
    Returns list of PIL images.
    """
    imgs = []

    for p in paths:
        p = os.path.abspath(p)

        if os.path.isdir(p):
            # Folder input - load all images
            for file in sorted(os.listdir(p)):
                full_path = os.path.join(p, file)
                if file.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS):
                    try:
                        imgs.append(Image.open(full_path).convert("RGB"))
                    except Exception as e:
                        logger.warning(f"Failed to open image {full_path}: {e}")
        else:
            # PDF support - convert to images
            if p.lower().endswith(".pdf"):
                try:
                    pages = convert_from_path(p, dpi=dpi)
                    imgs.extend(pages)
                except Exception as e:
                    logger.error(f"Failed to convert PDF {p} to images: {e}")
            else:
                # Regular image file
                try:
                    imgs.append(Image.open(p).convert("RGB"))
                except Exception as e:
                    logger.warning(f"Failed to open image {p}: {e}")

    return imgs
