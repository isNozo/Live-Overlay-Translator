import win32gui

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
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        if rect:
            left, top, right, bottom = rect
            return (left, top, right - left, bottom - top)
    return None