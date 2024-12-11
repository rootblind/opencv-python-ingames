import cv2 as cv
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision  # Import Vision class

# Initialize the WindowCapture class
wincap = WindowCapture('Albion Online Client')

# Initialize the Vision class with the needle image and desired matching method
vision = Vision('./img/fishing_minigame_small.JPG', method=cv.TM_CCOEFF_NORMED)

vision.init_control_gui()

loop_time = time()
while True:
    # Get an updated screenshot from the game window
    screenshot = wincap.get_screenshot()
    #screenshot = cv.resize(screenshot, (screenshot.shape[1] // 2, screenshot.shape[0] // 2))
    # Convert the screenshot to BGR for OpenCV processing
    screenshot_bgr = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    # obj detection
    #rectangles = vision.find(screenshot_bgr, threshold=0.7)

    #output_image = vision.draw_rectangles(screenshot_bgr, rectangles)

    output_image = vision.apply_hsv_filter(screenshot_bgr)
    cv.imshow('Matches', output_image)

    # Display FPS for debugging
    print('FPS: {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # Exit the loop when the user presses the `]` key
    if cv.waitKey(1) == ord(']'):
        cv.destroyAllWindows()
        break

print('Done.')
