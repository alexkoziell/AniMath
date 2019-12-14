import numpy as np
from shape import Shape

def superImpose(shape1: Shape, shape2: Shape):
    """ Superimposes shape1 onto shape 2, without rotation or scaling. """
    shape1.translate(shape2.center-shape1.center)

def shapeInterpolation(shape1: Shape, shape2: Shape):
    """ Transforms shape1 into shape2. """

def addVertices(shape: Shape, N: int):
    """ Adds evenly distributed vertices along the edges of the shape. """
    numSides = int(shape.vertices.size/2)
    
    sides = np.asarray([]) # vectors for each edge of the original shape
    perimeter = 0
    for i in range(numSides):
        edgeVector = shape.vertices[(i+1)%numSides]-shape.vertices[i]
        perimeter += np.linalg.norm(edgeVector)
        sides = np.append(sides, edgeVector)
    sides = sides.reshape(numSides, 2)

    
    if N == 1:
        newVertex = shape.vertices[0] + sides[0]/2 # add to first side
        shape.vertices = np.insert(shape.vertices, 1, newVertex, axis=0)

    elif N == 2:
        newVertex = shape.vertices[0] + sides[0]/2 # add to first and last sides
        shape.vertices = np.insert(shape.vertices, 1, newVertex, axis=0)
        newVertex = shape.vertices[-1] + sides[-1]/2
        shape.vertices = np.append(shape.vertices, newVertex)

    elif N == numSides: #simple case: half way between each side
        for n in range(N):
            newVertex = shape.vertices[2*n] + sides[n]/2
            shape.vertices = np.insert(shape.vertices, 2*n+1, newVertex, axis=0)

    else:
        spacing = (N-2)*perimeter/N
        distances = np.linspace(perimeter/N, (N-1)*perimeter/N, N) # divide perimeter evenly
        old_vertices = np.asarray(shape.vertices)
        for n, distance in enumerate(distances):
            travelled = 0 # travel along perimeter
            for sideNum, side in enumerate(sides):
                hadTravelled = travelled
                travelled += np.linalg.norm(side)
                if distance < travelled: # if we are on the right edge
                    alongEdgeByFraction = (distance-hadTravelled)/np.linalg.norm(side)
                    newVertex = old_vertices[sideNum] + sides[sideNum]*alongEdgeByFraction
                    shape.vertices = np.insert(shape.vertices, sideNum+n+1, newVertex, axis=0)
                    break
    
    shape.vertices = shape.vertices.reshape(numSides+N, 2)