import numpy as np
import pyglet

import sys
sys.path.append('../')
import colors

class Geometry():
    """ Base class for objects defined by sets of vertices. """

    def __init__(self, vertices, color=colors.WHITE):
        # vertices are a numpy array where each row is the coordinates of one vertex
        self.vertices = np.asarray(vertices, dtype=np.float64)
        self.color = color
    
    """ RENDERING """
    def draw(self, drawType):
        # uses pyglet to render a GL_LINE_LOOP through the vertices

        try:
            int_vertices = self.vertices.astype(int)
            gl_vertices = tuple(int_vertices.flatten().tolist())
            n_vertices = int(len(gl_vertices)/2)

            vertex_list = pyglet.graphics.vertex_list(
            n_vertices,
            ('v2i', gl_vertices),
            ('c3B', self.color*n_vertices)
            )
            vertex_list.draw(drawType)
        except:
            pass

    """ TRANFORMATIONS """
    def translate(self, vector):
        # numpy adds vector to each row in vertices when used as follows
        self.vertices += vector
        self.center += vector

    def rotate(self, angle):
        # translate vertices to center
        self.vertices = self.vertices - self.center

        # rotate
        rotation = Polygon.rotationMatrix(angle)
        self.vertices = np.transpose(self.vertices)
        self.vertices = rotation@self.vertices
        self.vertices = np.transpose(self.vertices)

        # return to original position
        self.vertices = self.vertices + self.center

    def scale(self, scale, x=True, y=True, z=True):
        # translate vertices to center
        self.vertices = self.vertices - self.center

        #rescale
        self.vertices *= scale

        # return to original position
        self.vertices = self.vertices + self.center

    @staticmethod
    def rotationMatrix(angle):
        return np.array([[np.cos(angle), -np.sin(angle)],
                           [np.sin(angle), np.cos(angle)]])


class Points(Geometry):
    """ Simple set of points. """
    def draw(self):
        super().draw(pyglet.gl.GL_POINTS)

class Shape(Geometry):
    """ Base class for shapes. """
    def draw(self, filled=False):
        super().draw(pyglet.gl.GL_POLYGON if filled else pyglet.gl.GL_LINE_LOOP)

class Polygon(Shape):
    def __init__(self, vertices, color=colors.WHITE):
        super().__init__(vertices, color)
        # average coordinate gives center
        self.center = np.average(vertices, axis=0)

class Ellipse(Shape):

    def __init__(self, center, major, minor, n_vertices=100, color=colors.WHITE):
        self.center = np.asarray(center, dtype=np.float64)

        # n_vertices determines the number of lines used to render the ellipse
        self.vertices = np.empty((n_vertices, 2), dtype=np.float64)
        for row, angle in enumerate(np.linspace(0, 2*np.pi, n_vertices)):
            point = center + np.asarray([major*np.cos(angle), minor*np.sin(angle)])
            self.vertices[row] = point

        self.color = color

class Circle(Ellipse):
    """ Subclass of ellipse. """
    def __init__(self, center, radius, color=colors.WHITE, n_vertices=100):
        super().__init__(center, radius, radius, color=color, n_vertices=n_vertices)
