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

for _ in range(0, FPS*seconds):
    my_canvas.draw(my_triangle)
    frame = my_canvas.image
    
    # my_triangle.translate(np.array([25,25]))
    my_triangle.rotate(np.pi/12)
    my_canvas.image = np.array(my_canvas.background)

    video.write(frame)

video.release()