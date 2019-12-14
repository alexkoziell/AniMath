import numpy as np
import pyglet
import pyglet.gl.gl as pygl

import argparse
import subprocess as sp

import sys
sys.path.append('geometry')
import shape

""" PARAMETERS """
isRecording = False
outfile = None
width, height = 1080, 720

""" SOME SHAPES... """
vertices = np.array([[200,200],[300,300],[400,200]])
my_triangle = shape.Polygon(vertices)

center = np.asarray([500, 500])
my_circle = shape.Circle(center, radius=100)

""" PYGLET """
def setupPyglet():
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
        if isRecording:
            pipe.stdin.write(buffer)

    def rotate_triangle(dt):
        my_triangle.rotate(0.02)

    pyglet.clock.schedule_interval(rotate_triangle, 1/24.0)
    pyglet.clock.schedule_interval(write_to_video, 1/24.0)


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
    print(outfile)

    if outfile is not None:
        isRecording = setupFFMPEG(width, height, outfile)
    else:
        askToContinue()

    setupPyglet()
    pyglet.app.run()