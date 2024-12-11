# credits for the code https://www.youtube.com/@LearnCodeByGaming

import cv2 as cv
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision  # Import Vision class

# Initialize the WindowCapture class
wincap = WindowCapture('Albion Online Client')

# Initialize the Vision class with the needle image and desired matching method
vision = Vision('./img/fishing_minigame_small.JPG', method=cv.TM_CCOEFF_NORMED)

loop_time = time()
while True:
    # Get an updated screenshot from the game window
    screenshot = wincap.get_screenshot()
    #screenshot = cv.resize(screenshot, (screenshot.shape[1] // 2, screenshot.shape[0] // 2))
    # Convert the screenshot to BGR for OpenCV processing
    screenshot_bgr = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    # Find the template (needle) in the screenshot using the Vision class
    points = vision.find(screenshot_bgr, threshold=0.7, debug_mode='rectangles')

    # Display FPS for debugging
    print('FPS: {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # Exit the loop when the user presses the `]` key
    if cv.waitKey(1) == ord(']'):
        cv.destroyAllWindows()
        break

print('Done.')
