import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import subprocess as sp

import canvas
import polygon

width  = 1080
height = 720

FPS = 24
seconds = 5

FFMPEG_BIN = 'ffmpeg'

command = [ FFMPEG_BIN,
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', '1080x720', # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '24', # frames per second
        '-i', '-', # The imput comes from a pipe
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'mpeg4',
        'my_output_videofile.mp4' ]

pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE)

# fourcc = VideoWriter_fourcc(*'mp4v')
# video  = VideoWriter('./triangle.mp4', fourcc, float(FPS), (width, height))

my_canvas = canvas.Canvas(width, height)

vertices = np.array([[200,200],
                     [300,300],
                     [400,200],
                     [200,200]])
my_triangle = polygon.Polygon(vertices)

for frameNum in range(0, FPS*seconds):
    # blank canvas to redraw the triangle in its new state
    my_canvas.image = np.array(my_canvas.background)

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

    pipe.stdin.write( image.tostring() )
    #video.write(image)

#video.release()