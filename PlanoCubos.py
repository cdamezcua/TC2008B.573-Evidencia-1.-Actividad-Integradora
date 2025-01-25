# Autor: Ivan Olmos Pineda
# Curso: Multiagentes - Graficas Computacionales

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from typing import Tuple

# Se carga el archivo de la clase Cubo
import sys

sys.path.append("..")
from CuboA import CuboA
from Forklift import Forklift

screen_width = 800
screen_height = 800
# vc para el obser.
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 900.0
# Variables para definir la posicion del observador
# gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 40.0
EYE_Y = 20.0
EYE_Z = 40.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X = 0
UP_Y = 1
UP_Z = 0
# Variables para dibujar los ejes del sistema
X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500
# Dimension del plano
DimBoard = 200
zone_size = 50  # Tamaño de la zona verde

pygame.init()


def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()
    # Y axis in green
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()
    # Z axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()
    glLineWidth(1.0)


def Init():
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


def display(
    warehouse_dimensions: Tuple[int, int, int],
    storage_zone_dimensions: Tuple[int, int, int],
):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()

    # We draw the warehouse (base plane)
    for x in range(warehouse_dimensions[0]):
        for z in range(warehouse_dimensions[2]):
            is_magenta = (x + z) % 2 == 0
            glColor3f(1.0, 1.0, 1.0) if is_magenta else glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_QUADS)
            glVertex3d(x, 0, z)
            glVertex3d(x, 0, z + 1)
            glVertex3d(x + 1, 0, z + 1)
            glVertex3d(x + 1, 0, z)
            glEnd()

    # We draw the storage zone
    storage_zone_start_x: int = (
        warehouse_dimensions[0] - storage_zone_dimensions[0]
    ) // 2
    storage_zone_start_y: float = 0.01
    storage_zone_start_z: int = (
        warehouse_dimensions[2] - storage_zone_dimensions[2]
    ) // 2
    storage_zone_end_x: int = storage_zone_start_x + storage_zone_dimensions[0]
    storage_zone_end_y: int = storage_zone_start_y + storage_zone_dimensions[1]
    storage_zone_end_z: int = storage_zone_start_z + storage_zone_dimensions[2]
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3d(storage_zone_start_x, storage_zone_start_y, storage_zone_start_z)
    glVertex3d(storage_zone_start_x, storage_zone_start_y, storage_zone_end_z)
    glVertex3d(storage_zone_end_x, storage_zone_start_y, storage_zone_end_z)
    glVertex3d(storage_zone_end_x, storage_zone_start_y, storage_zone_start_z)
    glEnd()
