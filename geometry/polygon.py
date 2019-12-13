import numpy as np
import pyglet

class Polygon():

    def __init__(self, vertices):
        # vertices are a numpy array where each row is the coordinates of one vertex
        self.vertices = vertices
        # average coordinate gives center
        self.center = np.average(vertices, axis=0)

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


    """ RENDERING """
    def draw(self):
        # uses pyglet to render a GL_LINE_LOOP through the vertices
        
        gl_vertices = tuple(self.vertices.flatten().tolist())
        n_vertices = int(len(gl_vertices)/2)

        polygon_vertices = pyglet.graphics.vertex_list(
        3,
        ('v2i', gl_vertices)
        )
        polygon_vertices.draw(pyglet.gl.GL_LINE_LOOP)