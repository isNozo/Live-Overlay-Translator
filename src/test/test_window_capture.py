"""
Usage:
$ cd Live-Overlay-Translator
$ pip install Pyside6 pywin32 windows_capture
$ python -m src.test.test_window_capture
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget
from ..window_capture import CaptureThread
from ..helpers import get_window_titles

def process_frame(frame_buffer):
    # Do nothing for testing
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create empty window (Main thread)
    window = QWidget()
    window.show()

    # List available window titles
    window_titles = get_window_titles()
    print("Available window titles:")
    for i, title in enumerate(window_titles):
        print(f"{i}: {title}")
    
    # Select a window to capture
    selected_index = int(input("Enter the number of the window to capture: "))
    selected_window = window_titles[selected_index]

    # Start capture thread
    capture_thread = CaptureThread(selected_window, process_frame)
    capture_thread.start()

    sys.exit(app.exec())