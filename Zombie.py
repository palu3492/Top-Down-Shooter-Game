import pygame
import random
import math

class Zombie(pygame.sprite.Sprite):
    zombieX = zombieY = 0
    type = "MOVE"
    current_idle, current_move, current_attack = 0,0,0
    zombie_speed=6
    stun_timer=0
    zombie_attack_timer=0

    player = ("zombie_" + type + "/skeleton-" + type + "_" + str(0) + ".png")
    zombie_health = 100.00

    def __init__(self, window_size, cash):
        self.player_cash=cash
        pygame.sprite.Sprite.__init__(self)
        self.window_size=window_size
        self.image = pygame.image.load("zombie_idle/skeleton-idle_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(120.5), int(111)))
        self.rect = self.image.get_rect()
        self.spawn_zombie() #calls function that controls Zombie Spawning

    #Spawns zombies out side of screen size
    def spawn_zombie(self):
        selection = random.randint(1,4)
        if selection == 1:
            self.zombieY = -1
            self.zombieX = random.randint(1, 192) *10
        elif selection == 2:
            self.zombieY = 1081
            self.zombieX = random.randint(1, 192) *10
        elif selection == 3:
            self.zombieY = random.randint(1, 108) *10
            self.zombieX = -1
        elif selection == 4:
            self.zombieY = random.randint(1, 108) *10
            self.zombieX= 1921

    def update_anim(self, type):
        if type == "Null":
            pass
        else:
            self.type = type

        if self.type == "IDLE":
            if self.current_idle < 16:
                self.current_idle+=1
            else:
                self.current_idle = 0
            self.player = ("zombie_" + type + "/skeleton-" + type + "_" + str(self.current_idle) + ".png")
        elif type == "MOVE":
            if self.current_move < 16:
                self.current_move += 1
            else:
                self.current_move = 0
            self.player = ("zombie_" + type + "/skeleton-" + type + "_" + str(self.current_move) + ".png")
        elif type == "ATTACK":
            if self.current_attack < 8:
                self.current_attack += 1
            else:
                self.current_attack = 0
            self.player = ("zombie_" + type + "/skeleton-" + type + "_" + str(self.current_attack) + ".png")

        self.image = pygame.image.load(self.player).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_rect().size[0] * .5),int(self.image.get_rect().size[1] * .5)))

    def get_posistion(self):
        return (self.zombieX, self.zombieY)

    def set_posistion(self, X, Y):
        self.zombieY = Y
        self.zombieX = X

    def reset_posistion(self):
        self.spawn_zombie()

    def move_posistion(self, cameraX,cameraY):
        self.rect.x = self.zombieX+cameraX
        self.rect.y = self.zombieY+cameraY

    def moveZombieTowardMid(self, cameraX,cameraY):
        zombie_pos = self.rect.x, self.rect.y
        distanceFromCenterX=(self.window_size[0]/2.0)-zombie_pos[0]-120
        distanceFromCenterY =(self.window_size[1]/2.0)-zombie_pos[1]-110
        angle=math.atan2(distanceFromCenterX,distanceFromCenterY) #find angle of zombie toward center
        moveX=(self.zombie_speed*math.sin(angle))  #x change amount
        moveY=(self.zombie_speed*math.cos(angle)) #Y change amount
        self.zombieX+=moveX
        self.zombieY+=moveY
        self.move_posistion(cameraX,cameraY)

    def health_bar(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (244, 66, 66), (self.rect.x + 75, self.rect.y, self.zombie_health * 1.2, 22))
        pygame.draw.rect(gameDisplay, (96, 96, 96), (self.rect.x + 75, self.rect.y, 100 * 1.2, 22), 4)

    def remove_health(self, damage):
        if self.zombie_health > 0:
            self.zombie_health -= damage
        if self.zombie_health <= 0:
            self.player_cash.increase_cash(50)
            return True
        else:
            return False

    def add_health(self, repair):
        self.zombie_health += repair

    def remove_speed(self, stun_amount):
        self.zombie_speed = stun_amount
        self.stun_timer=200

    def zombie_speed_timer(self):
        if self.stun_timer>0:
            self.stun_timer-=1
        else:
            self.zombie_speed=6

    def is_zombie_attacking(human, zombie):
        pygame.sprite.collide_rect_ratio(.5)
        if pygame.sprite.collide_rect(human, zombie):
            # zombie.update_anim("ATTACK")
            if human.remove_health(.75):  # if return True (player is dead) then change to idle and kill player
                # zombie.update_anim("IDLE")
                human.kill()




