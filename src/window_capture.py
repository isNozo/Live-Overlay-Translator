from windows_capture import WindowsCapture, Frame, InternalCaptureControl

def start_capture(window_name):
    """Start capturing the specified window."""
    capture = WindowsCapture(
        cursor_capture=False,
        draw_border=False,
        monitor_index=None,
        window_name=window_name,
    )

    @capture.event
    def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
        frame.save_as_image("./image.png")
        capture_control.stop()

    @capture.event
    def on_closed():
        print("Capture Session Closed")

    capture.start_free_threaded()
    return capture
