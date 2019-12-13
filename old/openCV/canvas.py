import cv2
import numpy as np

import polygon

class Canvas():
    BG_COLOR = "BLACK"

    def __init__(self, width, height):
        self.background = np.zeros((height, width, 3), dtype=np.uint8)
        self.image = np.zeros((height, width, 3), dtype=np.uint8)

    def draw(self, polygon: polygon.Polygon, filled=False, color=(0,255,255)):
        cv2.polylines(self.image, np.int32([polygon.vertices]), filled, color)

