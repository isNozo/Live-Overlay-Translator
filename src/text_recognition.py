from paddleocr import PaddleOCR
from ppocr.utils.logging import get_logger
import logging

class TextRecognizer:
    def __init__(self, lang='en'):
        self.ocr = PaddleOCR(lang=lang, use_angle_cls=True)
        logger = get_logger()
        logger.setLevel(logging.ERROR)


    def recognize_text(self, image_path):
        try:
            results = self.ocr.ocr(image_path, rec=True)  # Enable text recognition
            if not results or not results[0]:
                return None
            return results[0]
        except Exception as e:
            print(f"Failed to process image: {e}")
            return None