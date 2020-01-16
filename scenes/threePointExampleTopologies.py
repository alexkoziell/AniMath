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

    global redAB, redB
    redB  = shape.Circle(centerB, height/13, color=colors.RED)
    redAB = shape.Ellipse((centerA+centerB)/2, width/5, height/8, color=colors.RED)
    fadeinAB = animation.fadeIn(14, 16, redAB)
    fadeinB  = animation.fadeIn(24, 26, redB )


def drawScene(elapsedTime):
    X.draw() # entire set necessarily in the topology
    my_vertices.draw()
    
    dt = 1
    # example topologies
    if dt < elapsedTime < 2*dt:
        B.draw()
    if 2*dt < elapsedTime < 3*dt:
        AB.draw()
    if 3*dt < elapsedTime < 4*dt:
        A.draw()
        AB.draw()
    if 4*dt < elapsedTime < 5*dt:
        A.draw()
        BC.draw()
    if 5*dt < elapsedTime < 6*dt:
        A.draw()
        B.draw()
        AB.draw()
    if 6*dt < elapsedTime < 7*dt:
        B.draw()
        AB.draw()
        BC.draw()
    if 7*dt < elapsedTime < 8*dt:
        B.draw()
        C.draw()
        AB.draw()
        BC.draw()

    if 9*dt < elapsedTime < 19*dt:
        A.draw()
        B.draw()
        redAB.draw()
    if 19*dt < elapsedTime < 29*dt:
        AB.draw()
        BC.draw()
        redB.draw()


    if elapsedTime >= 30:
        pyglet.app.exit()
