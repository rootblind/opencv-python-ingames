import cv2 as cv
import numpy as np
import random

def random_coords(top_left, bottom_right):
    x1, y1 = top_left
    x2, y2 = bottom_right

    random_x = int(random.uniform(x1, x2))
    random_y = int(random.uniform(y1, y2))

    return random_x, random_y

class Vision:
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        # Load the image we're trying to match
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        self.method = method

    def find(self, haystack_img, threshold=0.5, debug_mode=None):
        # Run the OpenCV matchTemplate function
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the positions of matches that exceed the threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Group overlapping rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        points = []
        if len(rectangles):
            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:
                point_x, point_y = random_coords((x, y), (x + w, y + h))
                points.append((point_x, point_y))

                if debug_mode == 'rectangles':
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    cv.rectangle(haystack_img, top_left, bottom_right, (0, 255, 0), 2)
                elif debug_mode == 'points':
                    cv.drawMarker(haystack_img, (point_x, point_y), (255, 0, 255), cv.MARKER_CROSS, 40, 2)

        if debug_mode:
            cv.imshow('Matches', haystack_img)

        return points
