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
    if not hwnd:
        return None

    # Get the size of the client area
    client_rect = list(win32gui.GetClientRect(hwnd))
    
    # Convert the top-left coordinates of the client area to screen coordinates
    left, top = win32gui.ClientToScreen(hwnd, (0, 0))
    # Convert the bottom-right coordinates of the client area to screen coordinates
    right, bottom = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))
    
    return (left, top, right - left, bottom - top)