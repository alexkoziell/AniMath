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

    global definition1, definition2a, definition2b
    definition1 = image.Image('image/topology1.png',  width/12, 10*height/12, 1, 8)
    definition2a = image.Image('image/topology2c.png', width/12, 10*height/12, 10, 22)
    definition2b = image.Image('image/topology2d.png', 5*width/12, 8*height/12, 12, 22)
    
    fadeInX   = animation.fadeIn(3, 5, X)
    fadeOutX  = animation.fadeOut(5, 6, X)

    fadeinA, fadeOutA = animation.fadeIn(12, 14, A), animation.fadeOut(22,24, A)
    fadeinB, fadeOutB = animation.fadeIn(12.5, 14, B), animation.fadeOut(22,24, B)

    fadeinAB, fadeOutAB = animation.fadeIn(16, 18, AB), animation.fadeOut(22,24, AB)

def drawScene(elapsedTime):
    for shape in [X, A, B, AB]: #C, AB, BC]:
        shape.draw()

    definition1.sprite.draw()
    definition2a.sprite.draw()
    definition2b.sprite.draw()

    if elapsedTime < 7 or elapsedTime > 8.5:
        my_vertices.draw()
