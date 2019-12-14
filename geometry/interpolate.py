import numpy as np
from shape import Shape

def superImpose(shape1: Shape, shape2: Shape):
    """ Superimposes shape1 onto shape 2, without rotation or scaling. """
    shape1.translate(shape2.center-shape1.center)

def shapeInterpolation(shape1: Shape, shape2: Shape):
    """ Transforms shape1 into shape2. """