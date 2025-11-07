from PySide6.QtWidgets import (QMainWindow, QComboBox, QPushButton, QWidget, 
                             QVBoxLayout, QHBoxLayout, QStyle)
from PySide6.QtCore import QSize
import logging

class MainWindow(QMainWindow):
    def __init__(self, get_window_titles):
        super().__init__()        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.get_window_titles = get_window_titles

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
        self.stop_button = QPushButton("Stop Capture")
        
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.logger.debug("initialized")

    def update_text(self, text):
        self.logger.debug("selected window changed to: %s", text)
        self.selected_window = text

    def add_start_listener(self, listener):
        self.start_button.clicked.connect(listener)
    
    def add_stop_listener(self, listener):
        self.stop_button.clicked.connect(listener)

    def closeEvent(self, event):
        self.logger.debug("closing")
        self.stop_button.click()
        super().closeEvent(event)

    def refresh_window_list(self):
        """Refresh the window titles in the combobox"""
        current = self.combobox.currentText()
        window_titles = self.get_window_titles()
        
        self.combobox.clear()
        self.combobox.addItems(window_titles)
        
        # Try to restore the previous selection if it still exists
        index = self.combobox.findText(current)
        if index >= 0:
            self.combobox.setCurrentIndex(index)
        else:
            # If previous selection is gone, select the first item
            self.selected_window = window_titles[0] if window_titles else None
