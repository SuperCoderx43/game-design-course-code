import pygame
import numpy as np

class Asteroid:

    def __init__(self, speed, WINDOWWIDTH, WINDOWHEIGHT, startPos = -100):
        
        self.speed = speed
        self.image = pygame.image.load("ArtAssets7/asteroid.png")
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (np.random.randint(0, WINDOWWIDTH - self.rect.width), startPos) 
        self.rotateSpeed = np.random.randint(0, 10)
        self.rotation = 1

    def move(self):
        self.rect.top += self.speed
        self.rotation += self.rotateSpeed

    def draw(self):
        image = pygame.transform.rotate(self.image, self.rotation)
        return image, self.rect