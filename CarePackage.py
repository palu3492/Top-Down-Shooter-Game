import pygame
import random

class PackageSystem(pygame.sprite.Sprite):

    def spawn_package(self):
        self.rect.y = random.randint(1, 108) *10
        self.rect.x = random.randint(1, 192) *10

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Human.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.image.get_rect().size)
        self.rect = self.image.get_rect()
        self.spawn_package()

    def move_posistion(self, X, Y):
        self.rect.y = self.rect.y + Y
        self.rect.x = self.rect.x + X