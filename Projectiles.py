import pygame
import math

pygame.mixer.init()
explosion_sound = pygame.mixer.Sound('explosion.wav')
explosion_sound.set_volume(.01)

class Grenade(pygame.sprite.Sprite):
    changeX=0
    changeY=0
    grenadeX=0
    grenadeY=0
    xCounter=0
    yCounter=0
    explode=30

    def __init__(self, startX, startY, x, y):
        pygame.sprite.Sprite.__init__(self)
        angle = math.atan2(y, x)  # find angle of shot
        self.changeX = (int(50 * math.cos(angle)))  # x change amount
        self.changeY = (int(-50 * math.sin(angle)))  # Y change amount
        if self.changeX==0:
            self.changeX+=1
        if self.changeY == 0:
            self.changeY+=1
        self.image = pygame.image.load("grenade.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.grenadeX = startX - (self.rect[0]*1.0 / 2.0) #-half of grenade size
        self.grenadeY = startY - (self.rect[1]*1.0 / 2.0)
        self.xCounter=x/self.changeX
        self.yCounter=-y/self.changeY


    def update(self, cameraX, cameraY, screen,explosions):
        #print self.xCounter, self.yCounter
        if self.explode==30:
            if self.xCounter>0:
                self.rect.x = self.grenadeX + cameraX
                self.grenadeX += self.changeX
                self.xCounter+= -1
            else:
                self.rect.x = self.grenadeX + cameraX
            if self.yCounter>0:
                self.rect.y = self.grenadeY + cameraY
                self.grenadeY += self.changeY
                self.yCounter+= -1
            else:
                self.rect.y = self.grenadeY + cameraY

            if self.xCounter<=0 and self.yCounter<=0:
                self.explode += -1
        else:
            if self.explode>0:
                self.rect.x = self.grenadeX + cameraX
                self.rect.y = self.grenadeY + cameraY
                self.explode += -1
            else:
                explosion=grenadeDetonate(self.grenadeX,self.grenadeY)
                explosions.add(explosion)
                self.kill()


class grenadeDetonate(pygame.sprite.Sprite):
    explosionX=0
    explosionY=0
    counter=1
    def __init__(self,startX,startY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("explosion.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.explosionX = startX - (self.rect.size[0] / 2) #-half of explosion size
        self.explosionY = startY - (self.rect.size[1] / 2)
        explosion_sound.play()

    def update(self, cameraX, cameraY):
        #times before kill
        if self.counter>0:
            self.rect.x=self.explosionX+cameraX
            self.rect.y = self.explosionY + cameraY
            self.counter+= -1
        else:
            self.kill()


class stunGrenade(pygame.sprite.Sprite):
    changeX=0
    changeY=0
    grenadeX=0
    grenadeY=0
    xCounter=0
    yCounter=0
    explode=30

    def __init__(self, startX, startY, x, y):
        pygame.sprite.Sprite.__init__(self)
        angle = math.atan2(y, x)  # find angle of shot
        self.changeX = (int(50 * math.cos(angle)))  # x change amount
        self.changeY = (int(-50 * math.sin(angle)))  # Y change amount
        if self.changeX==0:
            self.changeX+=1
        if self.changeY == 0:
            self.changeY+=1
        self.image = pygame.image.load("stungrenade.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.grenadeX = startX - (self.rect[0]*1.0 / 2.0) #-half of grenade size
        self.grenadeY = startY - (self.rect[1]*1.0 / 2.0)
        self.xCounter=x/self.changeX
        self.yCounter=-y/self.changeY


    def update(self, cameraX, cameraY, screen,explosions):
        if self.explode==30:
            if self.xCounter>0:
                self.rect.x = self.grenadeX + cameraX
                self.grenadeX += self.changeX
                self.xCounter+= -1
            else:
                self.rect.x = self.grenadeX + cameraX
            if self.yCounter>0:
                self.rect.y = self.grenadeY + cameraY
                self.grenadeY += self.changeY
                self.yCounter+= -1
            else:
                self.rect.y = self.grenadeY + cameraY
            if self.xCounter<=0 and self.yCounter<=0:
                self.explode += -1
        else:
            if self.explode>0:
                self.rect.x = self.grenadeX + cameraX
                self.rect.y = self.grenadeY + cameraY
                self.explode += -1
            else:
                explosion=stunDetonate(self.grenadeX,self.grenadeY)
                explosions.add(explosion)
                self.kill()


class stunDetonate(pygame.sprite.Sprite):
    explosionX=0
    explosionY=0
    counter=1
    def __init__(self,startX,startY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("stunexplosion.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.explosionX = startX - (self.rect.size[0] / 2) #-half of explosion size
        self.explosionY = startY - (self.rect.size[1] / 2)
        explosion_sound.play()

    def update(self, cameraX, cameraY):
        #times before kill
        if self.counter>0:
            self.rect.x=self.explosionX+cameraX
            self.rect.y = self.explosionY + cameraY
            self.counter+= -1
        else:
            self.kill()