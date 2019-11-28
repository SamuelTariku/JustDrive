import pygame, sys
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

from importObj import *
pygame.init()
vp = (800, 600)
##hx = vp[0]/2
##hy = vp[1]/2
srf = pygame.display.set_mode(vp, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION, (-10, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (3, 3, 3, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)

obj = GameObject("Car.obj")

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = vp
gluPerspective(45.0, width/float(height), 1, 100)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5
rotate = move = False
game = True
while game:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glCallList(obj.gl_list)

    pygame.display.flip()
pygame.quit()
