import pyglet

import sys
sys.path.append('geometry')
from geometry.shape import Shape
from geometry import interpolate

class Animation():
    def __init__(self, start, end):
        self.start = start
        self.end   = end
        self.duration = end-start
        self.toCompletion = 1.0 # fraction left to completion
        pyglet.clock.schedule_once(self.begin, start)
        pyglet.clock.schedule_once(self.stop, end)

    def animateFunc(self, dt):
        pass

    def begin(self, dt):
        pyglet.clock.schedule_interval(self.animateFunc, 1/24)

    def stop(self, dt):
        pyglet.clock.unschedule(self.animateFunc)
        
class Morph(Animation):
    def __init__(self, start, end, srcShape: Shape, dstShape: Shape):
        super().__init__(start, end)
        self.srcShape = srcShape
        self.dstShape = dstShape
        self.vertexPaths = interpolate.shapeInterpolation(srcShape, dstShape)\
                         + interpolate.centerInterpolation(srcShape, dstShape)
        self.alpha = 1/(24*self.duration)

    def animateFunc(self, dt):
        interpolate.interpolateVertices(self.srcShape.vertices, self.vertexPaths, self.alpha)
        self.toCompletion -= self.alpha

    def stop(self, dt):
        self.srcShape.vertices = self.dstShape.vertices
        super().stop(dt)

    
