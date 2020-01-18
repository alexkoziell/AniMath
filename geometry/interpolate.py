from copy import deepcopy
import numpy as np
import scipy.optimize

from shape import Shape
import munkres

def linearInterpolation(srcPos, dstPos):
    return dstPos-srcPos

def centerInterpolation(shape1: Shape, shape2: Shape, alpha=1):
    """ Superimposes shape1 onto shape 2, without rotation or scaling. """
    return shape2.center-shape1.center

def shapeInterpolation(shape1: Shape, shape2: Shape):
    """ Transforms shape1 into shape2. """
    
    # add vertices to either shape if necessary
    numToAdd = int((shape1.vertices.size - shape2.vertices.size)/2)
    if numToAdd > 0:
        addVertices(shape2, numToAdd)
    elif numToAdd < 0:
        addVertices(shape1, abs(numToAdd))

    assert shape1.vertices.size == shape2.vertices.size
    N = int(shape1.vertices.size/2)

    # copy shape1 to calculate vertex paths. We can then make a gradual transformation
    # in a separate function
    shape1Copy = deepcopy(shape1)
    shape1Copy.translate(centerInterpolation(shape1, shape2))

    # match them between shapes
    # compute pair-wise distance matrix
    pairWiseDist = np.empty((N,N))
    for n in range(N):
        for m in range(N):
            # rows for shape 1 vertex
            pairWiseDist[n,m] = np.linalg.norm(shape1Copy.vertices[n] - shape2.vertices[m])

    # Munkres (Hungarian) Algorithm
    sourceIndices, destIndices = scipy.optimize.linear_sum_assignment(pairWiseDist)

    # interpolate shape1 vertices to shape 2 vertices
    paths = np.empty((N,2))
    for srcIdx, vertex in enumerate(shape1.vertices):
        # adjacent vertices mapped adjacently to the destination vertices
        destIdx = int(destIndices[0] + srcIdx) % len(destIndices) # destIndices[srcIdx]
        paths[srcIdx] = shape2.vertices[destIdx] - shape1Copy.vertices[srcIdx]

    return paths

def interpolateVertices(vertices, paths, alpha=1):
    vertices += alpha*paths

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

    if N <= 0:
        return
    
    elif N == 1:
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

def spriteInterpolation(sprite, trajectory, alpha=1):
    (x, y) = sprite.position
    x += trajectory[0]*alpha
    y += trajectory[1]*alpha
    sprite.update(x=x, y=y)