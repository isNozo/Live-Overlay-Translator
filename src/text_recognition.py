from paddleocr import PaddleOCR
import re

class TextRecognizer:
    def __init__(self, lang='en'):
        self.ocr = PaddleOCR(
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="PP-OCRv5_mobile_rec",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            )

    def is_valid_text(self, text):
        # Check if the text contains only numbers and symbols
        only_numbers_symbols = re.match(r'^[\d\W]+$', text) is not None
        return not only_numbers_symbols

    def recognize_text(self, frame_buffer):
        try:
            result = self.ocr.predict(frame_buffer)
            return result
        except Exception as e:
            print(f"Failed to process image: {e}")
            return None