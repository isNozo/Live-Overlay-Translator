from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6 import QtGui, QtCore
from helpers import get_window_rect

class OverlayWindow(QWidget):
    def __init__(self, target_title):
        super().__init__()
        self.target_title = target_title
        self.results = []
        
        # Set a frameless, always-on-top transparent window
        self.setWindowFlags(
            Qt.Window | 
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        # Resize the overlay window to match the target window
        rect = get_window_rect(self.target_title)
        if rect:
            self.setGeometry(*rect)
        else:
            # Default size if the target window is not found
            self.setGeometry(100, 100, 400, 300)

        # Set a timer to update the position of the overlay window
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)

        # Note: The label is not used for displaying text, but is required to create the QWidget
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        self.setLayout(layout)

    def update_position(self):
        rect = get_window_rect(self.target_title)
        if rect:
            self.setGeometry(*rect)

    def update_results(self, boxes, txts, scores):
        """Update the text to be displayed"""
        self.results = list(zip(boxes, txts, scores))
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Draw a border around the overlay window
        pen = QtGui.QPen(QtGui.QColor("#00AAFF"), 2)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        # Set pen for drawing text and boxes
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0, 200), 2)
        painter.setPen(pen)

        # Set font
        font = QtGui.QFont("Arial", 10)
        painter.setFont(font)

        for box, txt, score in self.results:
            # Draw bounding box
            polygon = QtGui.QPolygonF([QtCore.QPointF(float(x), float(y)) for x, y in box])
            painter.drawPolygon(polygon)

            # Draw text and confidence score
            text = f"{txt} ({score:.2f})"
            text_position = QtCore.QPointF(float(box[0][0]), float(box[0][1] - 10))
            painter.drawText(text_position, text)
