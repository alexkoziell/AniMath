import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

import canvas
import polygon

width  = 1280
height = 720

FPS = 24
seconds = 5

fourcc = VideoWriter_fourcc(*'MP42')
video  = VideoWriter('./triangle.avi', fourcc, float(FPS), (width, height))

my_canvas = canvas.Canvas(width, height)

vertices = np.array([[200,200],
                     [300,300],
                     [400,200],
                     [200,200]])
my_triangle = polygon.Polygon(vertices)

for frameNum in range(0, FPS*seconds):
    # draw the triangle
    my_canvas.draw(my_triangle)
    image = my_canvas.image
    
    # transform the triangle object
    if frameNum < FPS*seconds/3:
        my_triangle.translate(np.array([2,2]))
    elif frameNum < FPS*seconds*2/3:
        my_triangle.rotate(np.pi/12)
    else:
        my_triangle.scale(0.9)

    # blank canvas to redraw the triangle in its new state
    my_canvas.image = np.array(my_canvas.background)

    video.write(image)

video.release()