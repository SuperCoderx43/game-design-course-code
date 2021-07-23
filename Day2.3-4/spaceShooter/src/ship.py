import pygame

class Ship:

    def __init__(self, windowWidth, windowHeight):
        self.image = pygame.transform.scale(pygame.image.load('ArtAssets7/ship.png'), (80, 80))
        self.rect = self.image.get_rect()
        
        self.leftLimit = 10
        self.rightLimit = windowWidth - 10
        self.upLimit = 10
        self.downLimit = windowHeight - 10
        self.moveSpeed = 8 # pixels per frame

        self.setStartPos()
    
    def move(self, left, right, up, down):
        if left and self.rect.left >= self.leftLimit:
            self.rect.left -= self.moveSpeed
        if right and self.rect.right <= self.rightLimit:
            self.rect.right += self.moveSpeed
        if up and self.rect.top >= self.upLimit:
            self.rect.top -= self.moveSpeed
        if down and self.rect.bottom <= self.downLimit:
            self.rect.bottom += self.moveSpeed

    def setStartPos(self):
        # spawn ship in start position
        xCoord = (self.rightLimit + self.leftLimit) / 2
        yCoord = self.downLimit - (self.rect.height / 2)

        self.rect.center = (xCoord, yCoord)