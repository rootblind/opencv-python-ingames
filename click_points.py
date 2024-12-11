import cv2 as cv
import numpy as np
import os
import random

# generating random points on the detected objects

def random_coords(top_left, bottom_right):
    x1, y1 = top_left
    x2, y2 = bottom_right

    random_x = int(random.uniform(x1, x2))
    random_y = int(random.uniform(y1, y2))

    return random_x, random_y

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def click_points_finder(lake_img_path, bob_img_path, threshold = 0.5, debug_mode=None):
    bob_image = cv.imread(bob_img_path, cv.IMREAD_REDUCED_COLOR_2)
    lake_screenshot = cv.imread(lake_img_path, cv.IMREAD_REDUCED_COLOR_2)

    object_w = bob_image.shape[1]
    object_h = bob_image.shape[0]

    method = cv.TM_CCOEFF_NORMED

    result = cv.matchTemplate(lake_screenshot, bob_image, method)

    locations = np.where(result >= threshold)

    locations = list(zip(*locations[::-1]))

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), object_w, object_h]
        rectangles.append(rect)
        rectangles.append(rect)


    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

    points = []

    if len(rectangles):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (x, y, w, h) in rectangles:
            click_point_x, click_point_y = random_coords((x, y), (x + w, y + h))
            points.append((click_point_x, click_point_y))
            if debug_mode == 'rectangles':
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                cv.rectangle(lake_screenshot, top_left, bottom_right, color=line_color, lineType=line_type, thickness=2)
            elif debug_mode == 'points':
                cv.drawMarker(lake_screenshot, (click_point_x, click_point_y), color=marker_color, markerType=marker_type, markerSize=40, thickness=2)

            
        if debug_mode:
            cv.imshow('Matches', lake_screenshot)
            cv.waitKey()
            #cv.imwrite('result_click_points.JPG', lake_screenshot)
    return points


points = click_points_finder('./img/lake_bob_placed_1.JPG', './img/bob_placed_1.JPG', debug_mode='points')

print(points)

points = click_points_finder('./img/lake_bob_placed_1.JPG', './img/bob_placed_1.JPG', threshold=0.7, debug_mode='rectangles')

print(points)

print('Done!')
    