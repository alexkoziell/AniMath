import numpy as np
import pyglet
import pyglet.gl.gl as pygl

import argparse
import subprocess as sp

import sys
sys.path.append('geometry')
import animation
import colors
import interpolate, shape
sys.path.append('image')
import image

""" PARAMETERS """
isRecording = False
outfile = None
width, height = 1080, 720

""" ANIMATION """
def setupAnimation():
    # Some shapes
    triangle_vertices = np.array([[200,200],[400,200],[300,341]], dtype=np.float64)
    # triangle_color
    global my_triangle
    my_triangle = shape.Polygon(triangle_vertices, color=colors.RED)

    center = np.asarray([500, 500], dtype=np.float64)
    global my_circle
    my_circle = shape.Circle(center, color=colors.GREEN, radius=100)

    square_vertices = np.array([[665,195],[805,195],[805,335],[665,335]], dtype=np.float64)
    global my_square
    my_square = shape.Polygon(square_vertices, color=colors.BLUE)

    # Animate them!
    animation.Morph(1, 4,   my_triangle, my_circle)
    animation.Morph(4, 6.5, my_circle,  my_square)

    # Some text
    global continuity
    continuity = image.Image('image/continuity.png', x=50, y=height-150, start=1, end=6.5)

""" PYGLET """
def setupPyglet():
    window = pyglet.window.Window(width=width, height=height)
    pygl.glClearColor(0.05, 0.04, 0.04, 1)
    pygl.glLineWidth(3)
    pygl.glEnable(pygl.GL_BLEND)
    pygl.glBlendFunc(pygl.GL_SRC_ALPHA, pygl.GL_ONE_MINUS_SRC_ALPHA)

    clock = pyglet.clock.Clock()

    def on_draw(dt):
        window.clear()
        my_triangle.draw()
        my_square.draw()        
        my_circle.draw()
        continuity.sprite.draw()

    def write_to_video(dt):
        buffer = ( pygl.GLubyte * (3*window.width*window.height) )(0)
        pygl.glReadPixels(0, 0, width, height, pygl.GL_RGB, 
                            pygl.GL_UNSIGNED_BYTE, buffer)
        pipe.stdin.write(buffer)
    
    if isRecording:
        pyglet.clock.schedule_interval(write_to_video, 1/24.0)

    pyglet.clock.schedule_interval(on_draw, 1/24) # to sync animation with video



""" SETUP """
parser = argparse.ArgumentParser(description="Create a Math Animation.")
parser.add_argument('-o', '--outfile', type=str )

def setupFFMPEG(width, height, fileName):
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
            'output_videos/%s.mp4' % fileName ]

    global pipe 
    pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE)
    print("Animation is recording.")

    return True

def askToContinue():
    shouldContinue = str(input("Animation is not recording, continue? (y/n) "))
    if shouldContinue.lower() == 'y':
        pass
    elif shouldContinue.lower() == 'n':
        sys.exit("Animation aborted.")
    else:
        askToContinue()



if __name__ == "__main__":
    args = parser.parse_args()
    outfile = args.outfile

    if outfile is not None:
        isRecording = setupFFMPEG(width, height, outfile)
    else:
        askToContinue()

    setupPyglet()
    setupAnimation()
    pyglet.app.run()