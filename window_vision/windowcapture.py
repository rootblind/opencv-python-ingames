import numpy as np
import pyautogui
import win32gui, win32ui, win32con

def find_window_by_title(partial_title):
    def callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd) and partial_title in win32gui.GetWindowText(hwnd):
            result.append(hwnd)
    result = []
    win32gui.EnumWindows(callback, result)
    return result[0] if result else None

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = find_window_by_title(window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwnd)
        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        # Use pyautogui for window screenshot based on hwnd
        rect = win32gui.GetClientRect(self.hwnd)
        x, y = win32gui.ClientToScreen(self.hwnd, (rect[0], rect[1]))
        x1, y1 = win32gui.ClientToScreen(self.hwnd, (rect[2], rect[3]))
        width, height = x1 - x, y1 - y

        # Take a screenshot of the specified region
        im = pyautogui.screenshot(region=(x, y, width, height))

        # Convert the image to a numpy array (similar to previous method)
        img = np.array(im)
        img = img[..., :3]  # Drop the alpha channel if it exists

        return img

    # find the name of the window you're interested in.
    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
