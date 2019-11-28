import pygame

class HUD:
    def __init__(self, gameDisplay, width, height):
        self.gameDisplay = gameDisplay

        #Car Dashboard setup
        self.x, self.y = 0, 0
        self.dash = pygame.image.load('dashTrans.png')

        #Accelerometer setup
        self.speed = 0
        self.speedFont = pygame.font.Font('freesansbold.ttf', 40)
        self.speedSurf = None
        self.speedRect = None
        self.speedColor = pygame.color.Color("red")
        self.speedx, self.speedy = 450, 400
        
        self.wx, self.wy = 270, 300
        self.wheelx, self.wheely = 0, 0
        self.wheelRotateAngle = 0
        self.wheel = pygame.image.load('wheelTrans.png')
        self.wheel = pygame.transform.scale(self.wheel, (400, 400))

        self.RotWheel = None
        

    def render(self):
        
        self.gameDisplay.blit(self.dash, (self.x, self.y))
        self.gameDisplay.blit(self.speedSurf, self.speedRect)
        #pygame.draw.rect(self.gameDisplay, pygame.color.Color('red'), self.RotWheel.get_rect())
        self.gameDisplay.blit(self.RotWheel, (self.wheelx, self.wheely))
    def update(self):
        
        self.RotWheel = pygame.transform.rotate(self.wheel, self.wheelRotateAngle)
        rect = self.RotWheel.get_rect().center
        self.wheelx = self.wx - (rect[0] - 200)
        self.wheely = self.wy - (rect[1] - 200)

        self.speedSurf = self.speedFont.render(str(self.speed), True, self.speedColor)
        self.speedRect = self.speedSurf.get_rect()
        self.speedRect.x, self.speedRect.y = self.speedx, self.speedy
        if(self.wheelRotateAngle != 0):
            if(self.wheelRotateAngle < 0):
                self.wheelAngle(1)
            else:
                self.wheelAngle(-1)
        
        
        
    def wheelAngle(self, add):
        self.wheelRotateAngle += add
        self.wheelRotateAngle = min(self.wheelRotateAngle, 50)
        self.wheelRotateAngle = max(self.wheelRotateAngle, -50)

    def wheelRot(self, angle):
        if(85 <= angle < 314):
            self.wheelRotateAngle = 314
        elif(85 > angle > 49):
            self.wheelRotateAngle = 49
        else:
            self.wheelRotateAngle = angle
            
        
        
    def speedup(self):
        self.speed += 1
    def slowdown(self):
        if(self.speed > 0):
            self.speed -= 1
def main():
    pygame.init()
    width, height = 850, 650
    gameD = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    run = True
    hud = HUD(gameD, width, height)
    angle = 0
    accelerate = False
    while run:
        clock.tick(30)
        
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    angle = 10
                elif event.key == pygame.K_a:
                    angle = -10
                elif event.key == pygame.K_w:
                    accelerate = True
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    angle = 0
                elif event.key == pygame.K_w:
                    accelerate = False
                


        if(accelerate):
            hud.speedup()
        else:
            hud.slowdown()
        
        hud.wheelAngle(angle)
        hud.update()
        gameD.fill((10,100,100))
        hud.render()
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
        
    

        
        
