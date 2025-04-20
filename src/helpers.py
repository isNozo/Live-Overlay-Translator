import win32gui
from ctypes import windll, byref, Structure, c_int, sizeof

class RECT(Structure):
    _fields_ = [
        ('left', c_int),
        ('top', c_int),
        ('right', c_int),
        ('bottom', c_int)
    ]

def get_window_titles():
    titles = []

    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                titles.append(title)

    win32gui.EnumWindows(enum_handler, None)
    return titles

def get_window_rect(title):
    try:
        hwnd = win32gui.FindWindow(None, title)
        if not hwnd:
            return None

        # Get the window rect
        rect = RECT()
        windll.dwmapi.DwmGetWindowAttribute(
            hwnd,
            9,  # DWMWA_EXTENDED_FRAME_BOUNDS
            byref(rect),
            sizeof(rect)
        )
        
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        return (rect.left, rect.top, width, height)
    except Exception:
        return None