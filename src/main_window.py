from PySide6.QtWidgets import QMainWindow, QComboBox, QPushButton, QWidget, QVBoxLayout
from helpers import get_window_titles
from overlay_window import OverlayWindow
from window_capture import CaptureThread
from text_recognition import TextRecognizer
from translator import Translator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sub_window = None
        self.selected_window = None
        self.ocr = TextRecognizer(lang='en')
        self.translator = Translator()

        self.setWindowTitle("Live Overlay Translator")

        # Get available window titles and list them in the combobox
        self.combobox = QComboBox()
        self.combobox.addItems(get_window_titles())
        self.combobox.currentTextChanged.connect(self.update_text)

        # Create buttons for opening and closing the sub window
        self.start_button = QPushButton("Start Capture")
        self.start_button.clicked.connect(self.open_sub_window)
        self.stop_button = QPushButton("Stop Capture")
        self.stop_button.clicked.connect(self.close_sub_window)

        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_text(self, text):
        self.selected_window = text

    def open_sub_window(self):
        if self.sub_window is None:
            self.sub_window = OverlayWindow(self.selected_window)
            self.sub_window.show()
            self.capture_thread = CaptureThread(self.selected_window, self.process_frame)
            self.capture_thread.start()

    def close_sub_window(self):
        if self.sub_window:
            self.sub_window.close()
            self.sub_window = None
            self.capture_thread.stop()

    def closeEvent(self, event):
        if self.sub_window is not None:
            self.sub_window.close()
        super().closeEvent(event)
    
    def process_frame(self, frame_buffer):
        """Process captured frame"""
        result = self.ocr.recognize_text(frame_buffer)
        
        if result is not None:
            boxes = [line[0] for line in result]
            # txts = [self.translator.translate_text(line[1][0]) for line in result]
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            self.sub_window.update_results(boxes, txts, scores)
