import sys
from PySide6 import QtWidgets, QtCore
from helpers import select_window, calculate_coordinates
from window_capture import CaptureThread
from overlay_window import OverlayWindow
from text_recognition import TextRecognizer
from translator import Translator

class TranslationOverlay:
    def __init__(self):
        self.window_name = select_window()
        self.coordinates = calculate_coordinates(self.window_name)
        self.capture_thread = CaptureThread(self.window_name, self.process_frame)
        self.app = QtWidgets.QApplication(sys.argv)
        self.overlay = OverlayWindow(self.coordinates)
        self.ocr = TextRecognizer(lang='en')
        self.translator = Translator()
        self.running = True

    def process_frame(self):
        """Process captured frame"""
        result = self.ocr.recognize_text("./image.png")
        
        if result is not None:
            boxes = [line[0] for line in result]
            txts = [self.translator.translate_text(line[1][0]) for line in result]
            scores = [line[1][1] for line in result]
            self.overlay.update_results(boxes, txts, scores)

    def quit_application(self):
        """Clean up and quit application"""
        self.running = False
        self.capture.release()
        self.app.quit()

    def run(self):
        """Main application loop"""
        self.overlay.show()

        # start capture thread
        self.capture_thread.start()
        
        # Start event loop
        self.app.exec()

def main():
    overlay = TranslationOverlay()
    overlay.run()

if __name__ == "__main__":
    main()