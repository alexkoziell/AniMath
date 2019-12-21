import numpy as np
import pyglet

import sys
sys.path.append('..')
import animation
import colors
sys.path.append('../geometry')
import shape
sys.path.append('../image')
import image

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

    global definition1
    definition1 = image.Image('image/topology1.png', width/12, 10*height/12, 1, 7)
    
    fadeInX   = animation.fadeIn(6, 10, X)
    # fadeOutAB = animation.fadeOut(3, 5, AB)

def drawScene(elapsedTime):
    for shape in [X,]:#A, B, C, AB, BC]:
        shape.draw()

    definition1.sprite.draw()
    if elapsedTime < 3 or elapsedTime > 5:
        my_vertices.draw()
