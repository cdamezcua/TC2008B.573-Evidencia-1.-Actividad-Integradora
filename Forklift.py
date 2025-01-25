# Autor: Ivan Olmos Pineda

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
from typing import Tuple

import CuboA


class Forklift:

    def drawOrtoedro(self, x1, y1, z1, dx, dy, dz):
        x2 = x1 + dx
        y2 = y1 + dy
        z2 = z1 + dz
        vertices = [
            (x1, y1, z1),
            (x1, y2, z1),
            (x2, y2, z1),
            (x2, y1, z1),
            (x1, y1, z2),
            (x1, y2, z2),
            (x2, y2, z2),
            (x2, y1, z2),
        ]
        faces = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (1, 2, 6, 5),
            (0, 3, 7, 4),
        ]
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

    def drawForkliftsCar(self, fork_height: float = 0):
        glColor3f(0.0, 0.0, 0.0)
        self.drawOrtoedro(-3, 0, -1, 1, 2, 2)
        self.drawOrtoedro(2, 0, -1, 1, 2, 2)
        self.drawOrtoedro(-3, 0, -5, 1, 2, 2)
        self.drawOrtoedro(2, 0, -5, 1, 2, 2)
        glColor3f(1.0, 1.0, 0.0)
        self.drawOrtoedro(-3, 1, -7, 6, 1, 2)
        self.drawOrtoedro(-2, 1, -5, 4, 1, 2)
        self.drawOrtoedro(-3, 1, -3, 6, 1, 2)
        self.drawOrtoedro(-2, 1, -1, 4, 1, 2)
        self.drawOrtoedro(-3, 1, 1, 1, 1, 1)
        self.drawOrtoedro(2, 1, 1, 1, 1, 1)
        self.drawOrtoedro(-3, 2, -5, 6, 1, 7)
        self.drawOrtoedro(-3, 2, -6, 6, 3, 1)
        self.drawOrtoedro(-3, 2, -7, 1, 3, 1)
        self.drawOrtoedro(2, 2, -7, 1, 3, 1)
        self.drawOrtoedro(-2, 4, -7, 4, 1, 1)
        glColor3f(0.7, 0.7, 0.7)
        self.drawOrtoedro(-2, 1, 1, 4, 1, 1)
        self.drawOrtoedro(-2, 1, 2, 1, max(8, fork_height + 2), 1)
        self.drawOrtoedro(1, 1, 2, 1, max(8, fork_height + 2), 1)
        self.drawOrtoedro(-2, max(8, fork_height + 2), 1, 4, 1, 1)
        glColor3f(1.0, 1.0, 1.0)
        self.drawOrtoedro(-2, 2, -7, 1, 1, 1)
        self.drawOrtoedro(-1, 3, -7, 1, 1, 1)
        self.drawOrtoedro(0, 2, -7, 1, 1, 1)
        self.drawOrtoedro(1, 3, -7, 1, 1, 1)
        glColor3f(1.0, 0.0, 0.0)
        self.drawOrtoedro(-2, 3, -7, 1, 1, 1)
        self.drawOrtoedro(-1, 2, -7, 1, 1, 1)
        self.drawOrtoedro(0, 3, -7, 1, 1, 1)
        self.drawOrtoedro(1, 2, -7, 1, 1, 1)
        self.drawOrtoedro(-1, 8, -4, 2, 1, 2)
        glColor3f(0.3, 0.3, 0.3)
        self.drawOrtoedro(-2, 3, -5, 4, 5, 1)
        self.drawOrtoedro(-2, 3, -4, 1, 1, 4)
        self.drawOrtoedro(1, 3, -4, 1, 1, 4)
        self.drawOrtoedro(-2, 3, 0, 4, 1, 1)
        self.drawOrtoedro(-2, 4, 0, 1, 2, 1)
        self.drawOrtoedro(-2, 5, -1, 1, 2, 1)
        self.drawOrtoedro(1, 4, 0, 1, 2, 1)
        self.drawOrtoedro(1, 5, -1, 1, 2, 1)
        self.drawOrtoedro(-2, 6, -2, 4, 1, 1)
        self.drawOrtoedro(-2, 7, -4, 4, 1, 3)
        glColor3f(0.5, 0.3, 0.1)
        self.drawOrtoedro(-1, 3, -4, 2, 1, 2)
        self.drawOrtoedro(-1, 4, -4, 2, 1, 1)

    def drawForkliftsFork(self):
        glColor3f(0.3, 0.3, 0.3)
        self.drawOrtoedro(-3, 0, 2, 1, 3, 1)
        self.drawOrtoedro(-1, 0, 2, 1, 3, 1)
        self.drawOrtoedro(0, 0, 2, 1, 3, 1)
        self.drawOrtoedro(2, 0, 2, 1, 3, 1)
        self.drawOrtoedro(-3, 0, 3, 2, 1, 6)
        self.drawOrtoedro(-1, 0, 3, 2, 1, 2)
        self.drawOrtoedro(1, 0, 3, 2, 1, 6)

    def drawForklift(self, fork_height: float = 0):
        self.drawForkliftsCar(fork_height)
        glPushMatrix()
        glTranslatef(0.0, fork_height, 0.0)
        self.drawForkliftsFork()
        glPopMatrix()

    def draw(
        self,
        position: Tuple[float, float, float] = (0, 0, 0),
        direction: Tuple[float, float, float] = (1, 0, 0),
        fork_height: float = 0,
        is_loaded: bool = False,
    ):
        glPushMatrix()
        glTranslatef(position[0] + 0.5, position[1], position[2] + 0.5)
        glRotatef(math.degrees(math.atan2(direction[0], direction[2])), 0, 1, 0)
        glScaled(1 / 6, 1 / 6, 1 / 6)
        if is_loaded:
            glColor3f(0.0, 0.0, 1.0)
            glPushMatrix()
            glTranslatef(0.0, fork_height, 0.0)
            CuboA.CuboA().draw((0, 4, 6))
            glPopMatrix()
        self.drawForklift(fork_height)
        glPopMatrix()
