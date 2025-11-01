from paddleocr import TextRecognition
import time
import cv2

if __name__ == "__main__":
    ocr = TextRecognition(
        model_name="PP-OCRv5_mobile_rec",
        )
    
    # load image.png as ndarray (BGR) for PaddleOCR
    image = cv2.imread("./image.png", cv2.IMREAD_COLOR)

    start_time = time.time()
    result = ocr.predict(image)
    end_time = time.time()
    
    for res in result:
        res.print()
        res.save_to_img("output")
        res.save_to_json("output")

    print(f"OCR Time: {(end_time - start_time)*1000:.2f} ms")
