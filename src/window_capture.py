from PySide6.QtCore import QThread
from windows_capture import WindowsCapture, Frame, InternalCaptureControl

class CaptureThread(QThread):
    def __init__(self, window_name, process_frame):
        super().__init__()
        self.running = False

        self.capture = WindowsCapture(
            cursor_capture=False,
            draw_border=False,
            monitor_index=None,
            window_name=window_name,
        )

        @self.capture.event
        def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
            # print(f"Frame Arrived: {QThread.currentThread()}")
            frame.save_as_image("image.png")
            process_frame()

            if not self.running:
                capture_control.stop()

        @self.capture.event
        def on_closed():
            print("Capture Session Closed")
        
        print(f"Capture Thread Initialized: {QThread.currentThread()}")

    def run(self):
        print(f"Starting Capture: {QThread.currentThread()}")
        self.running = True
        self.capture.start()
    
    def stop(self):
        print(f"Stopping Capture: {QThread.currentThread()}")
        self.running = False
