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
sys.path.append('scenes')
import topologiesOnThreePoints as totp

""" PARAMETERS """
isRecording = False
outfile = None
width, height = 1920, 1080
elapsedTime = 0

""" ANIMATION """
def setupAnimation():
    totp.setupScene(width, height)

""" PYGLET """
def setupPyglet():
    window = pyglet.window.Window(width=width, height=height)
    pygl.glClearColor(0.05, 0.04, 0.04, 1)
    pygl.glPointSize(10)
    pygl.glLineWidth(5)
    pygl.glEnable(pygl.GL_BLEND)
    pygl.glBlendFunc(pygl.GL_SRC_ALPHA, pygl.GL_ONE_MINUS_SRC_ALPHA)

    def on_draw(dt):
        window.clear()

        global elapsedTime
        totp.drawScene(elapsedTime)
        if isRecording:
            write_to_video()

        elapsedTime += dt

    def write_to_video():
        buffer = ( pygl.GLubyte * (3*window.width*window.height) )(0)
        pygl.glReadPixels(0, 0, width, height, pygl.GL_RGB, 
                            pygl.GL_UNSIGNED_BYTE, buffer)
        pipe.stdin.write(buffer)

    pyglet.clock.schedule_interval(on_draw, 1/24) # to sync animation with video


""" ARGPARSE AND RECORDING """
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
            '-i', '-', # The input comes from a pipe
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


""" RUN """
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