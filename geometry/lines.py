import numpy as np
import pyglet
import sys
sys.path.append('../')
import colors

class NumberLine():
    def __init__(self, offset=0, subdivisions=10, color=colors.WHITE):
        (width, height) = pyglet.canvas.get_display().get_windows()[0].get_size()
        self.endVertices = np.asarray([0,     height/2+offset,
                                       width, height/2+offset])
        self.color = color
        self.markerPositions = np.linspace(0, width, subdivisions)

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

