from copy import deepcopy
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
        self.alpha = 1/(24*self.duration)
        pyglet.clock.schedule_once(self.begin, start)
        pyglet.clock.schedule_once(self.stop, end)

    def animateFunc(self, dt):
        self.toCompletion -= self.alpha

    def begin(self, dt):
        pyglet.clock.schedule_interval(self.animateFunc, 1/24)

    def stop(self, dt):
        pyglet.clock.unschedule(self.animateFunc)
        
class Morph(Animation):
    def __init__(self, start, end, srcShape: Shape, dstShape: Shape, keepObjectInstance=True):
        super().__init__(start, end)
        self.srcShape = srcShape
        self.dstShape = dstShape
        self.vertexPaths = interpolate.shapeInterpolation(srcShape, dstShape)\
                         + interpolate.centerInterpolation(srcShape, dstShape)
        
        self.keepObjectInstance = keepObjectInstance

    def animateFunc(self, dt):
        interpolate.interpolateVertices(self.srcShape.vertices, self.vertexPaths, self.alpha)
        super().animateFunc(dt)

    def stop(self, dt):
        if not self.keepObjectInstance:
            self.srcShape.vertices = None
            self.srcShape.center   = None
            self.srcShape.color    = None
        else:
            self.srcShape.vertices = self.dstShape.vertices
            self.srcShape.center   = self.dstShape.center
            self.srcShape.color    = self.dstShape.color

        super().stop(dt)
class fadeIn(Animation):
    def __init__(self, start, end, shape: Shape):
        super().__init__(start, end)
        self.shape = shape
        self.shape.color = deepcopy(self.shape.color)
        self.shape.color[3] = 0
    
    def animateFunc(self, dt):
        self.shape.color[3] += 255*self.alpha
        super().animateFunc(dt)

    def stop(self, dt):
        self.shape.color[3] = 255
        super().stop(dt)

class fadeOut(Animation):
    def __init__(self, start, end, shape: Shape):
        super().__init__(start, end)
        self.shape = shape
        self.shape.color = deepcopy(self.shape.color)
        self.startTransparency = 255
    
    def animateFunc(self, dt):
        self.shape.color[3] -= self.startTransparency*self.alpha
        super().animateFunc(dt)

    def stop(self, dt):
        self.shape.color[3] = 0
        super().stop(dt)

class moveSprite(Animation):
    def __init__(self, start, end, sprite, trajectory):
        super().__init__(start, end)
        self.sprite = sprite
        self.trajectory = trajectory
        self.endPos = (sprite.position[0]+trajectory[0], sprite.position[1]+trajectory[1])

    def animateFunc(self, dt):
        interpolate.spriteInterpolation(self.sprite, self.trajectory, self.alpha)
        super().animateFunc(dt)

    def stop(self, dt):
        self.sprite.update(x=self.endPos[0], y=self.endPos[1])
        super().stop(dt)