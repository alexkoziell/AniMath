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
    my_triangle = shape.Polygon(triangle_vertices, color=colors.RED)
    
    center = [width/2, 2*height/3]
    global my_circle
    my_circle = shape.Circle(center, color=colors.GREEN, radius=height/5)
    
    square_vertices = [[3*width/5,height/5],
                       [3*width/5+width/5,height/5],
                       [3*width/5+width/5,height/5+width/5],
                       [3*width/5,height/5+width/5]]
    global my_square
    my_square = shape.Polygon(square_vertices, color=colors.BLUE)

    # Animate them!
    animation.Morph(1, 3,   my_triangle, my_circle)
    animation.Morph(3, 4.5, my_circle,  my_square)

def drawScene(elapsedTime):
    if elapsedTime <= 3:
        my_triangle.draw()
    if 3 <= elapsedTime <= 4.5:
        my_circle.draw()        
    if elapsedTime >=4.5:
        my_square.draw()
    
    if elapsedTime > 8.0:
        pyglet.app.exit()
