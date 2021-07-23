import pygame
import numpy as np

class PowerUp:
    def __init__(self, Speed, WINDOWWIDTH):
        random = np.random.randint(0,3)
        if random == 0:
            self.image = pygame.image.load("ArtAssets7/triforce.png")
            # self.image.convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 80))
            self.rect = self.image.get_rect()
            self.type = 'triforce'
        elif random == 1:
            self.image = pygame.image.load("ArtAssets7/heart.png")
            # self.image.convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 80))
            self.rect = self.image.get_rect()
            self.type = 'heart'
        elif random == 2:
            self.image = pygame.image.load("ArtAssets7/shield.png")
            # self.image.convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 80))
            self.rect = self.image.get_rect()
            self.type = 'shield'
        self.speed = Speed
        self.rect.midtop = (np.random.randint(10, WINDOWWIDTH - 10), 10)
    
    def move(self):
        self.rect.top += self.speed
    
    def buff(self):
        return