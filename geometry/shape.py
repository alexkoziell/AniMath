import numpy as np
import pyglet

import sys
sys.path.append('../')
import colors

class Shape():

    """ RENDERING """
    def draw(self):
        # uses pyglet to render a GL_LINE_LOOP through the vertices

        try:
            int_vertices = self.vertices.astype(int)
            gl_vertices = tuple(int_vertices.flatten().tolist())
            n_vertices = int(len(gl_vertices)/2)

            polygon_vertices = pyglet.graphics.vertex_list(
            n_vertices,
            ('v2i', gl_vertices),
            ('c3B', self.color*n_vertices)
            )
            polygon_vertices.draw(pyglet.gl.GL_LINE_LOOP)
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


class Polygon(Shape):

    def __init__(self, vertices, color=colors.WHITE):
        # vertices are a numpy array where each row is the coordinates of one vertex
        self.vertices = vertices
        # average coordinate gives center
        self.center = np.average(vertices, axis=0)

        self.color = color

class Circle(Shape):

    def __init__(self, center, radius, color=colors.WHITE, n_vertices=100):
        self.center = center

        # n_vertices determines the number of lines used to render the circle
        self.vertices = np.asarray([], dtype=np.float64)
        for angle in np.linspace(0, 2*np.pi, n_vertices):
            point = center + radius*np.asarray([np.cos(angle), np.sin(angle)])
            self.vertices = np.append(self.vertices, point)
        self.vertices = self.vertices.reshape(n_vertices, 2)

        self.color = color
