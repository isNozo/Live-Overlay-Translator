from PySide6.QtWidgets import (QMainWindow, QComboBox, QPushButton, QWidget, 
                             QVBoxLayout, QHBoxLayout, QStyle)
from PySide6.QtCore import QSize
from helpers import get_window_titles
from overlay_window import OverlayWindow
from window_capture import CaptureThread
from text_recognition import TextRecognizer
from translator import Translator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sub_window = None
        self.ocr = TextRecognizer(lang='en')
        self.translator = Translator()

        self.setWindowTitle("Live Overlay Translator")

        # Create combo box and refresh button layout
        combo_layout = QHBoxLayout()
        
        # Get available window titles and list them in the combobox
        window_titles = get_window_titles()
        self.selected_window = window_titles[0] if window_titles else None
        self.combobox = QComboBox()
        self.combobox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.combobox.setMinimumContentsLength(28)
        self.combobox.addItems(window_titles)
        self.combobox.currentTextChanged.connect(self.update_text)
        
        # Create refresh button
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.refresh_button.setFixedSize(QSize(24, 24))
        self.refresh_button.clicked.connect(self.refresh_window_list)
        
        # Add widgets to horizontal layout
        combo_layout.addWidget(self.combobox)
        combo_layout.addWidget(self.refresh_button)
        
        # Create main layout
        layout = QVBoxLayout()
        layout.addLayout(combo_layout)
        
        # Create buttons for opening and closing the sub window
        self.start_button = QPushButton("Start Capture")
        self.start_button.clicked.connect(self.open_sub_window)
        self.stop_button = QPushButton("Stop Capture")
        self.stop_button.clicked.connect(self.close_sub_window)
        
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

    def refresh_window_list(self):
        """Refresh the window titles in the combobox"""
        current = self.combobox.currentText()
        window_titles = get_window_titles()
        
        self.combobox.clear()
        self.combobox.addItems(window_titles)
        
        # Try to restore the previous selection if it still exists
        index = self.combobox.findText(current)
        if index >= 0:
            self.combobox.setCurrentIndex(index)
        else:
            # If previous selection is gone, select the first item
            self.selected_window = window_titles[0] if window_titles else None
