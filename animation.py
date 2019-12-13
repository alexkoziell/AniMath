import numpy as np
import pyglet
import pyglet.gl.gl as pygl

import subprocess as sp

import sys
sys.path.append('geometry')
import shape

width  = 1080
height = 720

FPS = 24
seconds = 5

FFMPEG_BIN = 'ffmpeg'

FFMPEG_BIN = 'ffmpeg'
command = [ FFMPEG_BIN,
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', '%dx%d' %(width, height), # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '24', # frames per second
        '-i', '-', # The imput comes from a pipe
        '-vf', 'transpose=cclock_flip,transpose=cclock', # flips openGl output the right way up
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'mpeg4',
        'output_videos/rotating_triangle.mp4' ]

pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE)

vertices = np.array([[200,200],
                     [300,300],
                     [400,200]])
my_triangle = shape.Polygon(vertices)

center = np.asarray([500, 500])
radius = 200
my_circle = shape.Circle(center, radius)

window = pyglet.window.Window(width=width, height=height)

@window.event
def on_draw():
    window.clear()
    # simple frontend, see Polygon class for backend
    my_triangle.draw()
    my_circle.draw()

def write_to_video(dt):
    buffer = ( pygl.GLubyte * (3*window.width*window.height) )(0)
    pygl.glReadPixels(0, 0, width, height, pygl.GL_RGB, 
                         pygl.GL_UNSIGNED_BYTE, buffer)
    pipe.stdin.write(buffer)

def rotate_triangle(dt):
    my_triangle.rotate(0.02)

pyglet.clock.schedule_interval(rotate_triangle, 1/24.0)
pyglet.clock.schedule_interval(write_to_video, 1/24.0)

if __name__ == "__main__":
    pyglet.app.run()