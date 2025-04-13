from PySide6 import QtWidgets, QtGui, QtCore

class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, coordinates):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.Window | 
            QtCore.Qt.FramelessWindowHint | 
            QtCore.Qt.WindowStaysOnTopHint | 
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)

        self.setGeometry(
            coordinates['left'],
            coordinates['top'],
            coordinates['width'],
            coordinates['height']
        )
        
        # Create system tray icon
        self.tray_icon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(QtGui.QPixmap(32, 32))  # Placeholder icon
        )
        self.tray_icon.show()
        
        # Create tray menu
        tray_menu = QtWidgets.QMenu()
        quit_action = tray_menu.addAction("Exit")
        quit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        
        self.results = []

    def update_results(self, boxes, txts, scores):
        """Update the text to be displayed"""
        self.results = list(zip(boxes, txts, scores))
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Set semi-transparent green pen
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
