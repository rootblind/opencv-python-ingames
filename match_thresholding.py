import cv2 as cv
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

bob_image = cv.imread('./img/bob_placed_1.JPG', cv.IMREAD_REDUCED_COLOR_2)
lake_screenshot = cv.imread('./img/lake_bob_placed_1.JPG', cv.IMREAD_REDUCED_COLOR_2)

result = cv.matchTemplate(lake_screenshot, bob_image, cv.TM_SQDIFF_NORMED)

threshold = 0.17
locations = np.where(result <= threshold)

locations = list(zip(*locations[::-1]))

rectangles = []
for loc in locations:
    rect = [int(loc[0]), int(loc[1]), bob_image.shape[1], bob_image.shape[0]]
    rectangles.append(rect)
    rectangles.append(rect)


rectangles, wrights = cv.groupRectangles(rectangles, 1, 0.5)

print(rectangles)

if len(rectangles):
    print('Found object')

    object_w = bob_image.shape[1]
    object_h = bob_image.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    for (x, y, w, h) in rectangles:
        top_left = (x, y)
        bottom_right = (x + w, y + h)

        cv.rectangle(lake_screenshot, top_left, bottom_right, line_color, line_type)

    cv.imshow('Matches', lake_screenshot)
    cv.waitKey()
    cv.imwrite('result_match_threshold.JPG', lake_screenshot)
else:
    print('Object not found!')