import numpy as np
import pyglet

import sys
sys.path.append('..')
import animation
import colors
sys.path.append('../geometry')
import lines

def setupScene(width, height):
    global myNumberLine
    myNumberLine = lines.NumberLine()

def drawScene(elapsedTime):
    myNumberLine.draw()
