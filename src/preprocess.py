import cv2
import numpy as np
from PIL import Image

def pil_to_cv2(pil_img: Image.Image):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv_img):
    from PIL import Image
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cv_img)

def preprocess_for_ocr(pil_img: Image.Image, denoise=True, resize_max=2000):
    """
    Preprocess image for better OCR:
     - convert to grayscale
     - optional denoise
     - adaptive thresholding
     - resize if large
    Returns a PIL image ready for pytesseract.
    """
    img = pil_to_cv2(pil_img)
    h, w = img.shape[:2]
    scale = 1.0
    if max(h, w) > resize_max:
        scale = resize_max / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if denoise:
        gray = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)

    # Apply adaptive threshold - helps for scanned docs
    th = cv2.adaptiveThreshold(gray, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 15, 8)

    # Optional morphological ops to close small gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)

    return cv2_to_pil(th)
