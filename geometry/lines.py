import numpy as np
import pyglet
import sys
sys.path.append('../')
sys.path.append('../image')
import animation
import colors
import image
import interpolate

class NumberLine():
    def __init__(self, offset=0, subdivisions=11, start=-5, end=5, color=colors.WHITE):
        
        # for plotting intervals
        self.start = start
        self.end = end

        (width, height) = pyglet.canvas.get_display().get_windows()[0].get_size()
        self.endVertices = np.asarray([0,     height/2+offset,
                                       width, height/2+offset])
        self.color = color
        self.markerPositions = np.linspace(0, width, subdivisions)
        labelNumbers = np.linspace(start, end, subdivisions)
        self.labels = []
        for idx, labelNumber in enumerate(labelNumbers):
            label = pyglet.text.Label('%.2f' % labelNumber,
                                      font_name='Times New Roman',
                                      font_size=28,
                                      color = self.color,
                                      x=self.markerPositions[idx]-30, y=height/2+offset-50)
            self.labels.append(label)

    def draw(self):
        int_vertices = tuple(self.endVertices.astype(int))
        int_colors = tuple(map(int, self.color))*2

        try:
            pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINES,
            ('v2i', int_vertices),
            ('c4B', int_colors)
            )
        except Exception as exception:
            print(exception)
            pass

        for xPosition in self.markerPositions:
            self.vertLine([xPosition, self.endVertices[1]], 30)
        for label in self.labels:
            label.draw()

    def vertLine(self, position, height):
        int_vertices = (int(position[0]), int(position[1]+height/2),
                        int(position[0]), int(position[1]-height/2))
        int_colors = tuple(map(int, self.color))*2

        try:
            pyglet.graphics.draw(
            2,
            pyglet.gl.GL_LINES,
            ('v2i', int_vertices),
            ('c4B', int_colors)
            )
        except Exception as exception:
            print(exception)
            pass

class Interval():

    def __init__(self, endPoints: list, parentLine: NumberLine, aOpen: bool, bOpen: bool, color=colors.WHITE):
        self.parentLine = parentLine
        self.bOpen = bOpen
        
        # interval a to b
        a = endPoints[0]
        b = endPoints[1]

        lineWidth   = parentLine.end - parentLine.start
        screenWidth = parentLine.endVertices[2]
        self.resolution  = screenWidth/lineWidth

        vertPosition = parentLine.endVertices[3]-42
        aPosition, bPosition = (a-parentLine.start)*self.resolution, (b-parentLine.start)*self.resolution
        # fine adjustment for aesthetic
        aPosition -= 3
        bPosition -= 27 if bOpen else 15

        self.aBracket = image.Image('image/brackets/leftOpenBracket.png' if aOpen else 'image/brackets/leftClosedBracket.png', x=aPosition, y=vertPosition)
        self.bBracket = image.Image('image/brackets/rightOpenBracket.png' if bOpen else 'image/brackets/rightClosedBracket.png', x=bPosition, y=vertPosition)
        
        self.color = color[:3]
        self.aBracket.sprite.color = self.bBracket.sprite.color = self.color
        self.aBracket.sprite.scale_x = self.bBracket.sprite.scale_x = 1.5

    def resize(self, endPoints: list, startTime, endTime):
        aStart = np.asarray([self.aBracket.sprite.position[0], self.aBracket.sprite.position[1]])
        bStart = np.asarray([self.bBracket.sprite.position[0], self.bBracket.sprite.position[1]])

        aEnd, bEnd = (endPoints[0]-self.parentLine.start)*self.resolution,\
                     (endPoints[1]-self.parentLine.start)*self.resolution
        aEnd -= 3
        bEnd -= 27 if self.bOpen else 15

        aTrajectory = interpolate.linearInterpolation(aStart, np.asarray([aEnd, aStart[1]]))
        bTrajectory = interpolate.linearInterpolation(bStart, np.asarray([bEnd, bStart[1]]))

        for (sprite, trajectory) in [(self.aBracket.sprite, aTrajectory), (self.bBracket.sprite, bTrajectory)]:
            animation.moveSprite(startTime, endTime, sprite, trajectory)

        
