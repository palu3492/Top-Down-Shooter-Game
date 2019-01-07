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
        pygame.draw.rect(screen, (200, 200, 200), (10, 10, 200, 200))
        pygame.draw.line(screen, (0, 0, 0), (110, 10), (110,210))
        pygame.draw.line(screen, (0, 0, 0), (10, 110), (210, 110))
        pygame.draw.rect(screen, (0, 0, 200), (10+int(X/25), 10+int(Y/25), 7, 7))

    def update_zom(self, screen, zombie):
        X,Y = zombie.get_posistion()
        pygame.draw.rect(screen, (0, 255, 0), (10+int(X/25), 10+int(Y/25), 7, 7))

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
        self.images= [pygame.image.load("blHUD.png"), (40, window[1] - 76)],[pygame.image.load("brHUD.png"),
                                (window[0] - 263, window[1] - 162)],[pygame.image.load("tmHUD.png"), ((window[0] / 2.0) - 225, 0)]


    def update(self, screen, window):
        for image in self.images:
            screen.blit(image[0],image[1])


class grenade_data():
    grenade_amount=5
    stun_grenade_amount=5
    def __init__(self):
        pass


class Cash():
    cash_amount = 0

    def increase_cash(self,amount):
        self.cash_amount+=amount

    def decrease_cash(self,amount):
        self.cash_amount -= amount

    def update(self,screen):
        screen.blit(pygame.font.Font(None, 40).render("$"+str(self.cash_amount), True, (255, 255, 255)), (400, 7))


"""
class Clock:
    def __init__(self, window_size):
        self.window_size=window_size

    def drawClock(self):
"""