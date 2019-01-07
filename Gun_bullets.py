import pygame
import math

pygame.mixer.init()
gun_shot_sound = pygame.mixer.Sound('gunAudio.wav')
gun_shot_sound.set_volume(.01)


class Gun_1_bullet(pygame.sprite.Sprite):
    bullet_change_x = 0
    bullet_change_y = 0
    bullet_x_per_frame = 0
    bullet_y_per_frame = 0
    bulletX = 0
    bulletY = 0
    # how many pixel to move per frame
    bullet_speed = 150
    # 14 being size of bullet
    continuous = bullet_speed / 14
    kill_me = False

    def __init__(self, startX, startY, x, y):
        pygame.sprite.Sprite.__init__(self)
        angle = math.atan2(y, x)  # find angle of shot
        self.bullet_change_x = math.cos(angle)
        self.bullet_change_y = -math.sin(angle)
        self.bullet_x_per_frame = int(self.bullet_speed * self.bullet_change_x)  # x change amount
        self.bullet_y_per_frame = int(self.bullet_speed * self.bullet_change_y)  # Y change amount

        self.image = pygame.image.load("bullet.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.bulletX = startX - (self.rect[0] / 2)
        self.bulletY = startY - (self.rect[1] / 2)
        gun_shot_sound.play()

    def update(self, cameraX, cameraY, zombie_group):
        if not self.kill_me:
            for i in range(int(
                    self.continuous)):  # checks to see if bullet is touching zombie (bullet movement / bullet size) times
                self.rect.x = self.bulletX + cameraX
                self.rect.y = self.bulletY + cameraY
                self.bulletX += (14 * self.bullet_change_x)
                self.bulletY += (14 * self.bullet_change_y)
                for zombie in zombie_group:
                    if self.bullet_touching_zombie(zombie):
                        return
        else:
            self.kill()
        # kill bullet off screen
        if self.rect.x > 1000 or self.rect.x < -1000 or self.rect.y > 1000 or self.rect.y < -1000:
            self.kill_me = True

    def bullet_touching_zombie(self, zombie):
        if pygame.sprite.collide_rect(zombie, self):
            if zombie.remove_health(20):
                zombie.kill()
            self.kill_me = True
            return True

class Gun_2_bullet(pygame.sprite.Sprite):
    bullet_change_x=0
    bullet_change_y=0
    bullet_x_per_frame=0
    bullet_y_per_frame=0
    bulletX=0
    bulletY=0
    #how many pixel to move per frame
    bullet_speed=150
    #14 being size of bullet
    continuous=bullet_speed/14
    kill_me=False
    
    def __init__(self,startX,startY,x,y):
        pygame.sprite.Sprite.__init__(self)
        angle = math.atan2(y, x)  # find angle of shot
        self.bullet_change_x=math.cos(angle)
        self.bullet_change_y=-math.sin(angle)
        self.bullet_x_per_frame = int(self.bullet_speed * self.bullet_change_x)  # x change amount
        self.bullet_y_per_frame = int(self.bullet_speed * self.bullet_change_y)  # Y change amount

        self.image = pygame.image.load("bullet.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.bulletX = startX - (self.rect[0] / 2)
        self.bulletY = startY - (self.rect[1] / 2)
        gun_shot_sound.play()

    def update(self,cameraX,cameraY,zombie_group):
        if not self.kill_me:
            for i in range(int(self.continuous)):   #checks to see if bullet is touching zombie (bullet movement / bullet size) times
                self.rect.x=self.bulletX+cameraX
                self.rect.y=self.bulletY+cameraY
                self.bulletX += (14 * self.bullet_change_x)
                self.bulletY += (14 * self.bullet_change_y)
                for zombie in zombie_group:
                    if self.bullet_touching_zombie(zombie):
                        return
        else:
            self.kill()
        #kill bullet off screen
        if self.rect.x>1000 or self.rect.x<-1000 or self.rect.y>1000 or self.rect.y<-1000:
            self.kill_me=True

    def bullet_touching_zombie(self,zombie):
        if pygame.sprite.collide_rect(zombie, self):
            if zombie.remove_health(20):
                zombie.kill()
            self.kill_me=True
            return True

