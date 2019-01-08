import pygame

width = 1920
height = 50

BLACK = (0,0,0)
WHITE = (255,255,255)

human_X = 0
human_Y = 0

class RadarScrn:

    def __init__(self):
        pass

    def draw(self, screen, X, Y):
        pygame.draw.rect(screen, (200, 200, 200), (10, 10, 100, 100))
        pygame.draw.line(screen, (0, 0, 0), (10, 60), (110,60))
        pygame.draw.line(screen, (0, 0, 0), (60, 10), (60, 110))
        pygame.draw.rect(screen, (60, 255, 60), (10+int(X/50), 10+int(Y/50), 5, 5))

    def update_zom(self, screen, zombie):
        X,Y = zombie.get_posistion()
        pygame.draw.rect(screen, (255, 60, 60), (10+int(X/50), 10+int(Y/50), 5, 5))

class HealthBar:
    lives = 0
    def __init__(self, window_size):
        self.window_size=window_size

    def draw(self, screen, health_update):
        #pygame.draw.rect(screen, (200, 200, 200), (self.window_size[0]-200, self.window_size[1]-100, 200, 100))
        health_value = str(health_update)
        health_text = pygame.font.Font(None, 55)
        screen.blit(health_text.render(health_value, True, (255, 255, 255)), (70, self.window_size[1]-77))
        pygame.draw.rect(screen, (66, 255, 66), (480, 10, health_update * 2.2, 22))
        pygame.draw.rect(screen, (96, 96, 96), (480, 10, 100 * 2.2, 22), 4)

class HUD:
    def __init__(self, window):
        self.images= [pygame.image.load("Assets/HUD/blHUD.png"), (40, window[1] - 76)],[pygame.image.load("Assets/HUD/brHUD.png"),
                                (window[0] - 263, window[1] - 162)],[pygame.image.load("Assets/HUD/tmHUD.png"), ((window[0] / 2.0) - 225, 0)]


    def update(self, screen, window):
        for image in self.images:
            screen.blit(image[0],image[1])

class gun_data:
    clip_size = 60
    ammo_amount = 120
    reload_time=60
    def __init__(self,window):
        self.window=window
        self.gun_type = pygame.image.load("Assets/HUD/gunShotty.png")

    def shooting_bullet(self):
        if self.clip_size >1:
            self.clip_size-=1
        elif self.clip_size ==1:
            self.clip_size-=1
            if self.ammo_amount > 0:
                return self.reload_ammo()
        else:
            return "no ammo"

    def reload_ammo(self):
        #if clip is empty and ammo has at least 60 bullets
        if self.ammo_amount >= 60 and self.clip_size==0:
            self.ammo_amount -= 60
            self.clip_size = 60
        #if clip is empty and ammo does not have 60 bullets in it
        elif self.ammo_amount<60 and self.clip_size==0:
            self.clip_size=self.ammo_amount
            self.ammo_amount=0
        #if clip has bullets in it and ammo has enough to fill it
        elif self.clip_size!=0 and self.ammo_amount>=60-self.clip_size:
            self.ammo_amount-= 60-self.clip_size
            self.clip_size=60
        #if clip has bullets in it and ammo cant fill it
        elif self.clip_size!=0 and self.ammo_amount<60-self.clip_size:
            self.clip_size+=self.ammo_amount
            self.ammo_amount=0
        return "reload"

    def manual_reload(self):
        if self.ammo_amount>0:
            return self.reload_ammo()
        elif self.clip_size==0:
            return "no ammo"

    def reloading(self,screen):
        if self.reload_time>0:
            self.reload_time-=1
            self.update(screen)
            return "reload"
        else:
            #return nothing so it knows that its not still "reloading"
            self.reload_time=60
            return

    def update(self,screen):
        screen.blit(pygame.font.Font(None, 55).render(str(self.clip_size), True, (255, 255, 255)), (self.window[0] - 250, self.window[1] - 105))
        screen.blit(pygame.font.Font(None, 44).render(str(self.ammo_amount), True, (255, 255, 255)),(self.window[0] - 170, self.window[1] - 102))
        screen.blit(self.gun_type, (self.window[0]-125, self.window[1]-120))

class grenade_data():
    grenade_amount=5
    stun_grenade_amount=5
    def __init__(self):
        pass


class Cash():
    cash_amount = 0

    #Method used when zombie dies
    def increase_cash(self,amount):
        self.cash_amount+=amount

    #Method controls players cash
    # if player has the cash to purchase Item method will
    # return True allowing the purchase to be made
    def cash_add_remove(self, cash):
        if self.cash_amount == 0 or (self.cash_amount + cash) == 0:
            print("Player does not have enough funds")
            return False
        else:
            self.cash_amount += cash
            return True

    def update(self,screen):
        screen.blit(pygame.font.Font(None, 40).render("$"+str(self.cash_amount), True, (255, 255, 255)), (400, 7))

class Shop_Gui(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.window_size=(1080, 720)
        self.image = pygame.image.load("Assets/Zombie Animations/zombie_idle/skeleton-idle_0.png")
        self.image = pygame.transform.scale(self.image, (int(120.5), int(111)))
        self.rect = self.image.get_rect()





# Zombie killed counter
# class Zombies_Killed:
#     zombies_killed = 0
#     def __init__(self, window_size):
#         self.window_size=window_size
#
#     def killed_zombie(self):
#         self.zombies_killed +=1
#
#     def draw(self, screen):
#         health_value = str(self.zombies_killed)
#         health_text = pygame.font.Font(None, 25)
#         screen.blit(health_text.render("Zombies Killed: " + health_value, True, (255, 255, 255)), (160, self.window_size[1]-60))


"""
class Clock:
    def __init__(self, window_size):
        self.window_size=window_size

    def drawClock(self):
"""