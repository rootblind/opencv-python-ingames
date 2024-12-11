# credits for the code: https://www.youtube.com/@LearnCodeByGaming

import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
os.chdir(os.path.dirname(os.path.abspath(__file__)))


wincap = WindowCapture('Albion Online Client')

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()
    screenshot_bgr = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
    cv.imshow('Albion Online Client', screenshot_bgr)
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    if cv.waitKey(1) == ord(']'):  # Press `]` to exit
        cv.destroyAllWindows()
        break

print('Done.')
