import torch # Note: This is a workaround for the issue with paddleocr https://github.com/PaddlePaddle/PaddleOCR/issues/14979
from paddleocr import PaddleOCR
from ppocr.utils.logging import get_logger
import logging
import re

class TextRecognizer:
    def __init__(self, lang='en'):
        self.ocr = PaddleOCR(lang=lang, drop_score=0.9, use_angle_cls=False, det_limit_side_len=1980)
        logger = get_logger()
        logger.setLevel(logging.ERROR)

    def is_valid_text(self, text):
        # Check if the text contains only numbers and symbols
        only_numbers_symbols = re.match(r'^[\d\W]+$', text) is not None
        return not only_numbers_symbols

    def recognize_text(self, frame_buffer):
        try:
            results = self.ocr.ocr(frame_buffer, rec=True, cls=False)  # Enable text recognition
            if not results or not results[0]:
                return None
            
            # Filter out results that contain only numbers and symbols
            filtered_results = [
                result for result in results[0]
                if self.is_valid_text(result[1][0])
            ]
            
            return filtered_results if filtered_results else None
        except Exception as e:
            print(f"Failed to process image: {e}")
            return None