import numpy as np
import pyglet

import sys
sys.path.append('..')
import animation
import colors
sys.path.append('../geometry')
import shape

def setupScene(width, height):
    
    global X, AB, BC
    X  = shape.Ellipse([width/2, height/2], width/3, height/5, color=colors.WHITE)
    AB = shape.Ellipse([3*width/8, height/2], width/5, height/8, color=colors.WHITE)
    BC = shape.Ellipse([5*width/8, height/2], width/5, height/8, color=colors.WHITE)

    global my_vertices
    my_vertices = shape.Points([[width/4,   height/2],
                                [width/2,   height/2],
                                [3*width/4, height/2]])
    

def drawScene(elapsedTime):
    X.draw()
    AB.draw()
    BC.draw()
    my_vertices.draw()
