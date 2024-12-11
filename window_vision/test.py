import pyautogui
import win32gui
import win32con

def find_window_by_title(partial_title):
    def callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd) and partial_title in win32gui.GetWindowText(hwnd):
            result.append(hwnd)
    result = []
    win32gui.EnumWindows(callback, result)
    return result[0] if result else None

def screenshot(window_title=None):
    if window_title:
        hwnd = find_window_by_title(window_title)
        if hwnd:
            # Restore and bring the window to the foreground
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)

            # Get the client area rectangle
            rect = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (rect[0], rect[1]))
            x1, y1 = win32gui.ClientToScreen(hwnd, (rect[2], rect[3]))
            width, height = x1 - x, y1 - y

            # Take a screenshot of the specified region
            im = pyautogui.screenshot(region=(x, y, width, height))
            return im
        else:
            print('Window not found!')
    else:
        # Fullscreen screenshot
        im = pyautogui.screenshot()
        return im


# Example usage
im = screenshot('Albion Online Client')  # Replace with the exact or partial window title
if im:
    im.show()
