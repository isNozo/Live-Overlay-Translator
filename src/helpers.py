import win32gui

def select_window():
    """Display window list and let user select one"""
    window_names = get_window_names()
    print("\nAvailable windows:")
    for i, name in enumerate(window_names):
        if name:  # Only show windows with names
            print(f"{i}: {name}")
    
    while True:
        try:
            selection = int(input("\nEnter the number of the window to capture: "))
            if 0 <= selection < len(window_names):
                return window_names[selection]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def get_window_names():
    """Retrieve a list of currently open window names."""
    def enum_window_callback(hwnd, window_names):
        if win32gui.IsWindowVisible(hwnd):
            window_names.append(win32gui.GetWindowText(hwnd))

    window_names = []
    win32gui.EnumWindows(enum_window_callback, window_names)
    return window_names


def calculate_coordinates(window_name):
    """Calculate the coordinates of the specified window."""
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return {
            'left': rect[0],
            'top': rect[1],
            'width': rect[2] - rect[0],
            'height': rect[3] - rect[1]
        }
    else:
        raise ValueError("Window not found.")
