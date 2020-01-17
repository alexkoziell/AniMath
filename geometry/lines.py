import numpy as np
import pyglet
import sys
sys.path.append('../')
sys.path.append('../image')
import colors
import image

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
            print(idx, labelNumber)
            label = pyglet.text.Label('%.2f' % labelNumber,
                                      font_name='Times New Roman',
                                      font_size=28,
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

    def __init__(self, endPoints: list, parentLine: NumberLine, aOpen: bool, bOpen: bool):
        # interval a to b
        a = endPoints[0]
        b = endPoints[1]

        lineWidth   = parentLine.end - parentLine.start
        screenWidth = parentLine.endVertices[2]
        resolution  = screenWidth/lineWidth

        vertPosition = parentLine.endVertices[3]-40
        aPosition, bPosition = (a-parentLine.start)*resolution, (b-parentLine.start)*resolution
        bPosition -= 20 if bOpen else 13

        self.aBracket = image.Image('image/leftOpenBracket.png' if aOpen else 'image/leftClosedBracket.png', x=aPosition, y=vertPosition)
        self.bBracket = image.Image('image/rightOpenBracket.png' if bOpen else 'image/rightClosedBracket.png', x=bPosition, y=vertPosition)
        
        
