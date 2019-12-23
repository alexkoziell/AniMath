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
    triangle_vertices = [[width/5,height/5],
                         [2*width/5,height/5],
                         [3*width/10,4*height/10]]
    global my_triangle
    my_triangle = shape.Polygon(triangle_vertices, color=colors.WHITE)
    
    center = [width/2, 2*height/3]
    global my_circle
    my_circle = shape.Circle(center, color=colors.WHITE, radius=height/6)
    
    square_vertices = [[4*width/6,height/6],
                       [4*width/6+width/7,height/6],
                       [4*width/6+width/7,height/6+width/7],
                       [4*width/6,height/6+width/7]]
    global my_square
    my_square = shape.Polygon(square_vertices, color=colors.WHITE)

    # Animate them!
    animation.Morph(1, 3,   my_triangle, my_circle)
    animation.Morph(1.5, 3.5, my_square,  my_circle)

def drawScene(elapsedTime):
    my_triangle.draw()
    my_circle.draw()        
    my_square.draw()

    if elapsedTime > 4.0:
        pyglet.app.exit()
