# Autor: Ivan Olmos Pineda


import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


import numpy as np
from typing import Tuple


class CuboA:

    def __init__(self) -> None:
        self.points = np.array(
            [
                [-3.0, -3.0, 3.0],
                [3.0, -3.0, 3.0],
                [3.0, -3.0, -3.0],
                [-3.0, -3.0, -3.0],
                [-3.0, 3.0, 3.0],
                [3.0, 3.0, 3.0],
                [3.0, 3.0, -3.0],
                [-3.0, 3.0, -3.0],
            ]
        )
        self.faces = np.array(
            [
                [0, 1, 2, 3],
                [4, 5, 6, 7],
                [0, 1, 5, 4],
                [1, 2, 6, 5],
                [2, 3, 7, 6],
                [3, 0, 4, 7],
            ]
        )

        self.edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]

    def drawFaces(self) -> None:
        glBegin(GL_QUADS)
        for face in self.faces:
            for vertex in face:
                glVertex3fv(self.points[vertex])
        glEnd()

    def drawEdges(self) -> None:
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.points[vertex])
        glEnd()

    def draw(
        self, position: Tuple[int, int, int], scale: Tuple[int, int, int] = (1, 1, 1)
    ) -> None:
        glPushMatrix()
        glTranslatef(position[0] + 0.5, position[1] + 0.5, position[2] + 0.5)
        glScalef(scale[0], scale[1], scale[2])
        glColor3f(1.0, 0.0, 1.0)
        self.drawFaces()
        glColor3f(0.0, 0.0, 1.0)
        self.drawEdges()
        glPopMatrix()
