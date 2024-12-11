import cv2 as cv
import numpy as np

# loading two images
# bob_image contains a fishing bob and lake_screenshot contains an in-game screenshot of a lake and a bob floating
# this script detects the bob_image inside lake_screenshot


bob_image = cv.imread('./img/bob_pop_5.JPG', cv.IMREAD_REDUCED_COLOR_2)
lake_screenshot = cv.imread('./img/lake_bob_pop_1.JPG', cv.IMREAD_REDUCED_COLOR_2)

result = cv.matchTemplate(lake_screenshot, bob_image, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % str(max_val))

threshold = 0.85

if max_val >= threshold:
    print('found')
    top_left = max_loc
    bottom_right = (top_left[0] + bob_image.shape[1], top_left[1] + bob_image.shape[0])
    cv.rectangle(lake_screenshot, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    cv.imshow('Result', lake_screenshot)
    cv.waitKey()
    cv.imwrite('result_objesct_detection.JPG', lake_screenshot)
else:
    print('not found')