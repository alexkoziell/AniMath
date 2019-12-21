import numpy as np
import pyglet

import sys
sys.path.append('..')
import animation
import colors
sys.path.append('../geometry')
import shape

def setupScene(width, height):

    centerA = np.array([width/4,   height/2])
    centerB = np.array([width/2,   height/2])
    centerC = np.array([3*width/4, height/2])
    
    global X, A, B, C, AB, BC
    X  = shape.Ellipse(centerB, width/3, height/5, color=colors.WHITE)
    
    A  = shape.Circle(centerA, height/13)
    B  = shape.Circle(centerB, height/13)
    C  = shape.Circle(centerC, height/13)

    AB = shape.Ellipse((centerA+centerB)/2, width/5, height/8, color=colors.WHITE)
    BC = shape.Ellipse((centerB+centerC)/2, width/5, height/8, color=colors.WHITE)

    global my_vertices
    my_vertices = shape.Points([centerA,
                                centerB,
                                centerC])
    
    fadeInX   = animation.fadeIn(1.0, 2.0, X)
    fadeOutAB = animation.fadeOut(3, 5, AB)

def drawScene(elapsedTime):
    for shape in [X, A, B, C, AB, BC]:
        shape.draw()

    print(colors.WHITE)
    my_vertices.draw()
