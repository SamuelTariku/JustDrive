import pygame
from OpenGL.GL import *

def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if(line.startswith("#")): continue
        values = line.split()
        if(not values): continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise(ValueError, "file doesn't startwith newmtl stmt")
        elif values[0] == 'map_Kd':
            mtl[values[0]] = values[1]
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, image)
        elif values[0] == 'map_Ka':
            pass
        elif values[0] in ('refl', 'map_refl'):
            pass
        else:
            mtl[values[0]] = list(map(float, values[1:]))
    return contents
            
                                     

class GameObject:
    def __init__(self, filename, swap=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces =[]
        self.mtl = None
        material = None

        size = 0
        split = filename.split('/')
        
        for line in open(filename, 'r'):
            size += 1
            if line.startswith('#'):continue
            values = line.split()
            if not values: continue #if line is empty
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if(swap):
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if(swap):
                    v = v[0], v[2], v[1]
                self.normals.append(v)

            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                if(len(split) > 1):
                    self.mtl = MTL(split[0] + '/' + values[1])
                else:
                    self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords= []
                norms = []

                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if(len(w) >= 2 and len(w[1]) > 0):
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if(len(w) >= 3 and len(w[2]) > 0):
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)

                self.faces.append((face, norms, texcoords, material))
        print("Size, ", size)
            
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        nofaces = 0
        for face in self.faces:
            vertices, normals, texture_coords, material = face
            nofaces += 1
            mtl = self.mtl[material]

            if('texture_Kd' in mtl):
                #if texture map -- use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                glColor(mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if(normals[i] > 0):
                    glNormal3fv(self.normals[normals[i] - 1])
                if(texture_coords[i] > 0):
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        print("Face, ", nofaces)
        glDisable(GL_TEXTURE_2D)
        glEndList()
    def draw(self, trans=(0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        glTranslatef(trans[0], trans[1], trans[2])
        glRotate(rotate[0], 1, 0, 0)
        glRotate(rotate[1], 0, 1, 0)
        glRotate(rotate[2], 0, 0, 1)
        glScalef(scale[0], scale[1], scale[2])
        glCallList(self.gl_list)
        
    
    
