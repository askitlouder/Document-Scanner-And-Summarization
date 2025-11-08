import pytesseract
from PIL import Image
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pytesseract.pytesseract.tesseract_cmd = r"F:\ASKITLOUD\OpenCVProjects\Document_Scanner_Summerisation\model_binaries\tesseract.exe"


def ocr_image_tesseract(pil_img: Image.Image, lang='eng', psm=3, oem=3) -> str:
    """
    Runs pytesseract OCR and returns extracted text.
    psm: page segmentation mode (3 = fully automatic)
    oem: OCR engine mode
    """
    custom_config = f'--oem {oem} --psm {psm}'
    try:
        text = pytesseract.image_to_string(pil_img, lang=lang, config=custom_config)
    except Exception as e:
        logger.exception("Tesseract failed:", exc_info=e)
        text = ""
    return text

def ocr_images(images: List[Image.Image], preprocess_fn=None) -> str:
    """
    Takes a list of PIL images, optionally preprocesses them, and returns concatenated text.
    """
    texts = []
    for i, im in enumerate(images):
        if preprocess_fn:
            im_proc = preprocess_fn(im)
        else:
            im_proc = im
        txt = ocr_image_tesseract(im_proc)
        texts.append(txt)
    return "\n\n".join(texts)
