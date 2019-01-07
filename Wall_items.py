import pygame

class GunOnWall(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("gun_on_wall.png")
        self.rect = self.image.get_rect()
        self.rect.x =0
        self.rect.y = 0
        self.gunX=100
        self.gunY=10


    def update(self,cameraX,cameraY):
        self.rect.x = self.gunX+cameraX
        self.rect.y = self.gunY+cameraY

    #do you already own item? then chang press to buy

    def press_to_buy(self, screen,cameraX,cameraY):
        screen.blit(pygame.font.Font(None, 20).render("Press [X] to buy", True, (255, 255, 255)), (self.gunX+cameraX, self.gunY+30+cameraY))
        return "shotgun"