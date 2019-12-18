import numpy as np
import pyglet

import sys
sys.path.append('..')
import animation
import colors
sys.path.append('../geometry')
import shape

def setupScene(width, height):
    # Some shapes
    triangle_vertices = [[width/3,height/3],
                         [2*width/3,height/3],
                         [width/2,2*height/3]]
    global my_triangle
    my_triangle = shape.Polygon(triangle_vertices)
    my_triangle.translate(np.asarray([0, 100]))

    center = [width/2, 5*height/7]
    global my_circle
    my_circle = shape.Circle(my_triangle.center, radius=height/5-10)

    square_vertices = [[4*width/7,height/5],
                       [4*width/7+width/6,height/5],
                       [4*width/7+width/6,height/5+width/6],
                       [4*width/7,height/5+width/6]]
    global my_square
    my_square = shape.Polygon(square_vertices)
    my_square.translate(my_triangle.center-my_square.center)
    my_square.scale(1.3)

    # Animate them!
    animation.Morph(1, 3,   my_square, my_circle)
    animation.Morph(3.1, 4.5, my_circle,  my_triangle)

def drawScene(elapsedTime):
    if elapsedTime < 3:
        my_square.draw()
    elif 3 < elapsedTime < 4.6:
        my_circle.draw()        
    else:
        my_triangle.draw()
    
    if elapsedTime > 6.0:
        pyglet.app.exit()
