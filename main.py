
import pygame, sys
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import hud
import random
from InputBox import InputBox
from importObj import *
import numpy

#CAR NPC
class Car:
    def __init__(self, obj):
        self.obj = obj
        self.movements = [[-7,0,90], [-7, 2,180], [6, 2, 270], [6, 0, 360]]
        self.current = 0
        self.x, self.z = -1, 0
        self.direction = 90
        self.speed = 0.01
        self.turnSpeed = 5
    def update(self):
        check = True
        if(math.floor(self.x) != self.movements[self.current][0]):
            if(self.x > self.movements[self.current][0]):
                self.x -= self.speed
            else:
                self.x += self.speed

            check = False
        
        if(math.floor(self.z) != self.movements[self.current][1]):
            if(self.z > self.movements[self.current][1]):
                self.z -= self.speed
            else:
                self.z += self.speed

            check = False
        if(self.direction != self.movements[self.current][2]):
            if(self.direction > self.movements[self.current][2]):
                self.direction -= self.turnSpeed
            else:
                self.direction += self.turnSpeed
            check = False

        if(check):
            if(self.current + 1 < len(self.movements)):
                self.current += 1
            else:
                self.current = 0
        self.obj.draw((self.x, 0.05,self.z), (0, self.direction, 0), (0.5, 0.5, 0.5))
    
        

class Player:
    def __init__(self):
        self.speed = 3
        self.answers = 0
        self.direction = 1
        self.x, self.z = 0, 0
        self.angle = 0
        self.maxSpeed = 2

    def addAngle(self, a):
        if(self.angle + a > 360):
            self.angle = (self.angle + a) - 360
        elif(self.angle + a < 0):
            self.angle = 360 - (self.angle + a)
        else:
            self.angle += a
    

def text_objects(text, font, color=(255,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text(text, location, display, size):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, largeText, pygame.color.Color("green"))
    TextRect.center = location
    display.blit(TextSurf, TextRect)
def intro():
    gameD = pygame.display.set_mode((800, 600))
    
    text("JUST DRIVE 1", (400, 100), gameD, 50)
    text("DRIVING SIMULATOR", (400, 150), gameD, 20)
    text("Play City Drive Simulator -- Press 1", (400, 250), gameD, 20)
    text("Play Maze Game -- Press 2", (400, 300), gameD, 20)
    text("Exit -- Press 3", (400, 350), gameD, 20)
    level = 0
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 0
                if event.key == pygame.K_2:
                    level = 1
                if event.key == pygame.K_3 or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                wait = False
            
                    
                
        pygame.display.update()
    return level

def Riddle(gameD, vp):
    gameD = pygame.display.set_mode(vp)
    riddleImage = pygame.image.load("clown.jpeg")

    gameD.blit(riddleImage, (270, 50))


    Riddles = {"""Can you name three consecutive day
                s without using the words Monday Thursday Sunday""" : "Yesterday Today Tommorrow",
               "David's father has three sons: Snap, Crackle and _______" : "David",
               "What belongs to you, but other people use it more than you" : "Your name",
               """I speak without a mouth and hear without ears. I have no body, but i come alive with the wind
                What am i """ : "echo",
               """You measure my life in hours and i serve you by expiring, i'm quick when i am thin and slow
                when i am fat. The wind is my enemy""" : "Candle",
               """I have cities but no houses, i have mountains but no trees, i have water, but no fish. What am i""" : "map",
               """i come from a mine and get surrounded by wood always. What am i""" : "Pencil lead",
               "What disappers as soon as you say its name" : "Silence",
               "I have keys, but no lock and space but no rooms. You can enter but you cant leave. What am i" : "Keyboard",
               "What comes once a minute, twice in a moment but never in a thousand years" : "m",
               "The more you take, the more you leave behind. What am i" : "Footsteps",
               "What can be swallowed but swallow you also?" : "Pride",
               """I can fly but have no wings, i can cry but
                i have no eyes. Whereever i go darkness follows me. What am i""" : "Cloud",
               "What are the two things you can never eat for breakfast" : "Lunch and Dinner",
               """Open me, you can't see me without a mirror. Close me and you can't see me at all. What am i""" : "Eyes",
               "What has a Heart but no other organs" : "cards",
               "When i point up its bright. When i point down its dark. What am i" : "light switch",
               "Two bodies have i, though both joined in one. The more still i stand, the quicker i run. What am i" : "hourglass",
               """Some will use me, while others will not. Some have remembered, others have forgotten.
                For profit or gain, i'm used expertly. I can't be picked off the ground or tossed into the sea.
                Only gained from patience and time, can you unravel my rhyme. what am i""" : "knowledge"
               }

    Riddle = random.choice(list(Riddles.keys()))
    
    answer = False
    inputbox = InputBox(100, 400, 500, 30)
    
    level = 0
    wait = True
    clock = pygame.time.Clock()
    while wait:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            rCheck = inputbox.handle_event(event)
            if(rCheck[0]):
                a = rCheck[1].lower()
                if(a == Riddles[Riddle].lower()):
                    answer = True
                    riddleImage = pygame.image.load("riddleCorrect.png")
                else:
                    riddleImage = pygame.image.load("riddleWrong.png")
                wait = False
        gameD.fill((0,0,0))
        gameD.blit(riddleImage, (270, 50))
        text(Riddle, (400, 350), gameD, 10)
        inputbox.update()
        inputbox.draw(gameD)
        inputbox.active = True          
                
        pygame.display.update()

    gameD = pygame.display.set_mode(vp, OPENGL | DOUBLEBUF)
    light()
    setupDisplay(vp)
    return answer


def light():
    glLightfv(GL_LIGHT0, GL_POSITION, (-10, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    
    
def setupDisplay(vp):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = vp
    gluPerspective(45.0, width/float(height), 1, 200.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    
    glTranslate(0, -1.5, 0)
    #glRotate(10, 1, 0, 0)
    glScale(15, 10, 15)
    view_mat = numpy.matrix(numpy.identity(4), 'float32', False)
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)

    return view_mat

def displayHUD(playerHud, vp):
    w, h = playerHud.get_size()

    texture = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    image = pygame.image.tostring(playerHud, "RGBA", 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    
    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor3f(1, 1, 1)
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glTranslate(-1, -1.1, 0)
    glScale((2 / w) + 0.0001, 2 / h, 1)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glDisable(GL_LIGHTING)
    glBegin(GL_QUADS)
    x0, y0 = -15, 14
    w, h = playerHud.get_size()
    for dx, dy in [(0,0), (0, 1), (1, 1), (1, 0)]:
        glVertex(x0 + dx * w, y0 + dy * h, 0)
        glTexCoord(dy, 1 - dx)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glDisable(GL_BLEND)
    glDeleteTextures([texture])

    light()
    



def main():
    #Initialize pygame and setup variables
    global Running
    pygame.init()
    vp = (800, 600)
    
    #SOUNDS
    carStartSound = pygame.mixer.Sound("carStart2.wav")
    carHornSound = pygame.mixer.Sound("carHorn.wav")
    carRunSound = pygame.mixer.Sound("carRun5.wav")
    currentMeter = 0
    soundChanges = [0.1, 0.2, 0.4, 0.6, 0.9, 1.3, 1.5, 1.8, 2]
    carAccelerateSound = pygame.mixer.Sound("carRun4.wav")
    
    notMax = True
    
    startSound = False
    
    Tracks = {"main" : "mainTrack.wav", "maze" : "mazeTrack.wav"}
    pygame.mixer.music.load(Tracks["main"])
    pygame.mixer.music.play(-1)
    
    level = intro()

    if(level == 1):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(Tracks["maze"])
        pygame.mixer.music.play(-1)
    
    srf = pygame.display.set_mode(vp, OPENGL | DOUBLEBUF)

    #LIGHTING AND SHADE
    light()

    #OBJECTS
    levels = ["city.obj", "maze.obj"]
    obj = GameObject(levels[level])
    gameobjects = []
    car = None
    if(level == 0):
        car = Car(GameObject("Car.obj"))
        gameobjects.append(car.obj)
        HUDsurface = pygame.Surface(vp)
        playerHud = hud.HUD(HUDsurface, vp[0], vp[1])
        
        
    
    view_mat = setupDisplay(vp)
    if(not Running):
        Running = True
        accelerate = False
        brake = False
        display = False
        isRiddle = False
        horn = False
        player = Player()
        speed = 0
        turning = 0
        game = True
        clock = pygame.time.Clock()
        RiddlePoints = [(84, -29), (48, 56), (-39, -66),
                        (15, 115), (-85,106), (823, -65),
                        (923, 177), (1117, 219), (1044, -98),
                        (868, -57)]
        riddleOut = True
        while game:
            clock.tick(30)
            for e in pygame.event.get():
                if e.type == QUIT:
                    game = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_a:
                        turning = 1
                        
                    elif e.key == pygame.K_d:
                        turning = -1
                    elif e.key == pygame.K_w:
                        accelerate = True
                    elif e.key == pygame.K_s:
                        brake = True
                    elif e.key == pygame.K_j:
                        display = True
                    elif e.key == pygame.K_h:
                        horn = True
                    elif e.key == pygame.K_ESCAPE:
                        game = False
                    
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_w:
                        accelerate = False
                    elif e.key == pygame.K_s:
                        brake = False
                    elif e.key == pygame.K_a or e.key == pygame.K_d:
                        turning = 0
                    elif e.key == pygame.K_j:
                        display = False
                    elif e.key == pygame.K_h:
                        horn = False
            #game logic 
            if(accelerate):
                if(speed < 0.08):
                    if(not startSound):
                        pygame.mixer.Sound.play(carStartSound)
                        startSound = True
                        
                elif(speed > soundChanges[currentMeter] and notMax):
                    pygame.mixer.Sound.play(carAccelerateSound)
                    if(currentMeter+1 == len(soundChanges)):
                        notMax = False
                    else:
                        currentMeter+=1
                else:
                    startSound = False
                    if(notMax):
                        current = 0
                        while (speed > soundChanges[current]):
                            current += 1
                        currentMeter = current
                    else:
                        if(speed < soundChanges[len(soundChanges)-1]):
                            notMax = True
                speed += 0.001
                speed = min(player.maxSpeed, speed)
            else:
                speed -= 0.001
                speed = max(speed, 0)

            if(brake):
                speed -= 0.02
                speed = max(speed, 0)

            if(turning == 1):
                turn = -1
            elif(turning == -1):
                turn = 1
            else:
                turn = 0

            if(level == 1):
                for i in RiddlePoints:
                    if(i[0] - 10 < player.x < i[0] + 10 and i[1] - 10 < player.z < i[1] + 10):
                        if(riddleOut):
                            isRiddle = True
                            riddleOut = False

                            RiddlePoints.remove(i)

                        speed -= 1
                    else:
                        riddleOut = True
                        
                        
                        
            if(len(RiddlePoints) == 0):
                view_mat = numpy.matrix(numpy.identity(4), 'float32', False)
                glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
                RiddlePoints = [(84, -29), (48, 56), (-39, -66),
                        (15, 115), (-85,106), (823, -65),
                        (923, 177), (1117, 219), (1044, -98),
                        (868, -57)]
                
            if(horn):
                pygame.mixer.Sound.play(carHornSound)
                
            if(isRiddle):
                answer = Riddle(srf, vp)
                isRiddle = False
                obj = GameObject(levels[level])

                if(answer):
                    player.answers += 1
            
            if(display):
                print()
                print(player.x, player.z)
    ##        if(player.x > 118 and player.x):
    ##            print("test x")
    ##            speed = -speed
    ##            turn = -turn
            #player.setSpeed(speed)


            
            
            glPushMatrix()
            
            glLoadIdentity()
            glTranslate(0, 0, speed)
            player.z += speed*math.cos(math.radians(player.angle))
            player.x += speed*math.sin(math.radians(player.angle))
            glRotate(turn, 0, 1, 0)
            player.addAngle(turn)
            glMultMatrixf(view_mat)
            
            glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            
            
            glCallList(obj.gl_list)
            
##            for gameobject in gameobjects:
##                glCallList(gameobject.gl_list)

            if(level == 0):
                if(car != None):
                    car.update()
                playerHud.speed = math.floor(speed * 100)
                playerHud.wheelAngle(-(turn * 10))
                playerHud.update()
                playerHud.render()
                displayHUD(HUDsurface, vp)
            
            glPopMatrix()
            

            
            
            pygame.display.flip()
            #pygame.quit()
            #break

        pygame.quit()

            


    

    
   
    


if __name__ == '__main__':
    global Running
    Running = False
    main()
