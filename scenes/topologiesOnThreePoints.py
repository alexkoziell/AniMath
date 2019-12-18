import numpy as np
import pyglet

import sys
sys.path.append('..')
import animation
import colors
sys.path.append('../geometry')
import shape

def setupScene(width, height):
    
    global my_ellipse
    my_ellipse = shape.Ellipse([width/2, height/2], width/4, height/4, color=colors.WHITE)
    

def drawScene(elapsedTime):
    my_ellipse.draw()
