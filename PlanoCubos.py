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
UP_X = 0
UP_Y = 1
UP_Z = 0
DOOR_PROPORTION: float = 1522 / 2130
pygame.init()

textures = []


def Axis(warehouse_dimensions: Tuple[int, int, int]):
    max_dimension = max(warehouse_dimensions)
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(-max_dimension, 0.0, 0.0)
    glVertex3f(max_dimension, 0.0, 0.0)
    glEnd()
    # Y axis in green
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, -max_dimension, 0.0)
    glVertex3f(0.0, max_dimension, 0.0)
    glEnd()
    # Z axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, -max_dimension)
    glVertex3f(0.0, 0.0, max_dimension)
    glEnd()
    glLineWidth(1.0)


def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data
    )
    glGenerateMipmap(GL_TEXTURE_2D)


def Init(
    warehouse_dimensions: Tuple[int, int, int],
    storage_zone_dimensions: Tuple[int, int, int],
):
    # Configuración inicial de la cámara
    eye_x = warehouse_dimensions[0] * 1.25
    eye_y = (warehouse_dimensions[0] + warehouse_dimensions[2]) * 0.5
    eye_z = warehouse_dimensions[2] * 1.25
    center_x = warehouse_dimensions[0] / 2
    center_y = 0
    center_z = warehouse_dimensions[2] / 2
    distance_to_origin = ((eye_x) ** 2 + (eye_y) ** 2 + (eye_z) ** 2) ** 0.5

    # Configuración de la ventana de Pygame y OpenGL
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Evidencia 1. Actividad Integradora - Equipo Colonists")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, distance_to_origin * 1.1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye_x, eye_y, eye_z, center_x, center_y, center_z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    Texturas("wall_texture.png")
    Texturas("door_texture.png")


def PlanoTexturizadoXY(width, height):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(0, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(0, height, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(width, height, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(width, 0, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def PlanoTexturizadoYZ(depth, height):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(0, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(0, height, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(0, height, depth)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(0, 0, depth)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def PuertaTexturizadaXY(door_width, door_height, wall_width):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glColor3f(1.0, 1.0, 1.0)
    x_start = (wall_width - door_width) / 2
    x_end = x_start + door_width
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(x_start, 0, 0.01)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(x_start, door_height, 0.01)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(x_end, door_height, 0.01)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(x_end, 0, 0.01)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def display(
    warehouse_dimensions: Tuple[int, int, int],
    storage_zone_dimensions: Tuple[int, int, int],
):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis(warehouse_dimensions)
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
    storage_zone_start_x: int = (
        warehouse_dimensions[0] - storage_zone_dimensions[0]
    ) // 2
    storage_zone_start_y: float = 0.01
    storage_zone_start_z: int = (
        warehouse_dimensions[2] - storage_zone_dimensions[2]
    ) // 2
    storage_zone_end_x: int = storage_zone_start_x + storage_zone_dimensions[0]
    _: int = storage_zone_start_y + storage_zone_dimensions[1]
    storage_zone_end_z: int = storage_zone_start_z + storage_zone_dimensions[2]
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3d(storage_zone_start_x, storage_zone_start_y, storage_zone_start_z)
    glVertex3d(storage_zone_start_x, storage_zone_start_y, storage_zone_end_z)
    glVertex3d(storage_zone_end_x, storage_zone_start_y, storage_zone_end_z)
    glVertex3d(storage_zone_end_x, storage_zone_start_y, storage_zone_start_z)
    glEnd()
    door_width = warehouse_dimensions[0] / 3
    door_height = door_width * DOOR_PROPORTION
    walls_height = max(
        (warehouse_dimensions[0] + warehouse_dimensions[2]) / 2, 1.5 * door_height
    )
    PlanoTexturizadoXY(warehouse_dimensions[0], walls_height)
    PlanoTexturizadoYZ(warehouse_dimensions[2], walls_height)
    PuertaTexturizadaXY(
        warehouse_dimensions[0] / 3, door_height, warehouse_dimensions[0]
    )
