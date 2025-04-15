from PySide6.QtCore import QThread
from windows_capture import WindowsCapture, Frame, InternalCaptureControl

class CaptureThread(QThread):
    def __init__(self, window_name, process_frame):
        super().__init__()
        self.capture = WindowsCapture(
            cursor_capture=False,
            draw_border=False,
            monitor_index=None,
            window_name=window_name,
        )

        @self.capture.event
        def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
            # print("Frame Arrived")
            frame.save_as_image("image.png")
            process_frame()

        @self.capture.event
        def on_closed():
            print("Capture Session Closed")

    def run(self):
        self.capture.start()

