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
    X  = shape.Ellipse(centerB, width/3, height/5, color=colors.BLUE)
    
    A  = shape.Circle(centerA, height/13)
    B  = shape.Circle(centerB, height/13)
    C  = shape.Circle(centerC, height/13)

    AB = shape.Ellipse((centerA+centerB)/2, width/5, height/8, color=colors.GREEN)
    BC = shape.Ellipse((centerB+centerC)/2, width/5, height/8, color=colors.WHITE)

    global my_vertices
    my_vertices = shape.Points([centerA,
                                centerB,
                                centerC])

    global definition1, definition2a, definition2b, definition3a, definition3b
    definition1 = image.Image('image/topology1.png',  width/12, 10*height/12, 1, 10)
    definition2a = image.Image('image/topology2c.png', width/12, 10*height/12+50, 12, 24)
    definition2b = image.Image('image/topology2d.png', 5*width/12-150, 8*height/12+15, 16, 24)
    definition3a = image.Image('image/topology3a.png', width/12, 10*height/12+50, 25, 37)
    definition3b = image.Image('image/topology3b.png', 5*width/12-150, 8*height/12, 29, 37)
    definition3b.sprite.update(scale=0.9)
    
    fadeInX   = animation.fadeIn(3, 5, X)
    fadeOutX  = animation.fadeOut(5, 6, X)

    # Arbitrary union
    fadeinA, fadeOutA = animation.fadeIn(12, 14, A), animation.fadeOut(22,24, A)
    fadeinB, fadeOutB = animation.fadeIn(12.5, 14, B), animation.fadeOut(22,24, B)
    fadeinAB, fadeOutAB = animation.fadeIn(17, 19, AB), animation.fadeOut(22,24, AB)

    # Finite intersection
    fadeinAB_2, fadeOutAB_2 = animation.fadeIn(24, 26, AB), animation.fadeOut(35,37, AB)
    fadeinBC, fadeOutBC = animation.fadeIn(25, 27, BC), animation.fadeOut(35,37, BC)
    fadeinB_2, fadeOutB_2 = animation.fadeIn(30, 32, B), animation.fadeOut(35,37, B)

def drawScene(elapsedTime):
    for shape in [X, A, B, AB, BC]:
        shape.draw()

    if 24 < elapsedTime < 25:
        AB.color = colors.WHITE
        B.color  = colors.RED

    definition1.sprite.draw()
    definition2a.sprite.draw()
    definition2b.sprite.draw()
    definition3a.sprite.draw()
    definition3b.sprite.draw()

    if elapsedTime < 7 or elapsedTime > 8.5:
        my_vertices.draw()

    if elapsedTime >= 40:
        pyglet.app.exit()
