# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 11:26:21 2019

@author: J. Tyler McGoffin
"""

import pygame, sys
import numpy as np
from pygame.locals import *

from ship import Ship
from laser import Laser
from asteroid import Asteroid
from background import Background
from powerup import PowerUp

#Set up window and frame rate variables
FPS = 30
WINDOWWIDTH = 500
WINDOWHEIGHT = 700

#Set up some Color variables
BLACK = (0, 0, 0)
NAVYBLUE = (0, 0, 128)
DARKPURPLE = (100, 0, 100)
WHITE = (255, 255, 255)
DARKGRAY = (100, 100, 100)

#Start the game
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT #True globals
    
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Space Shooter")
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    showStartScreen()
    # Game Loop
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    #setup game
    score = 0 # Num of asteroids destroyed
    lives = 3 
    levelUp = False
    timer_laser = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_laser, 1000)
    laser_counter = 1

    timer_shield = pygame.USEREVENT + 2
    pygame.time.set_timer(timer_shield, 1000)
    shield_counter = 1

    #Create Game Objects: ship, asteroids, lasers, background
    # Ship Controls
    playerShip = Ship(WINDOWWIDTH, WINDOWHEIGHT)
    leftHeld = False
    rightHeld = False
    upHeld = False
    downHeld = False
    firing = False

    # Lasers
    lasers = initializeObjects(20)
    laserIndex = 0
    laserSpeed = 10
    fireRate = 4 # lazers/sec

    # Asteroids
    asteroids = initializeObjects(25)
    spawnRate = 5 # asteroids/sec
    minAsteroidSpeed = 1
    maxAsteroidSpeed = 6
    asteroidIndex = 0
    
    # PowerUps
    powerups = initializeObjects(5)
    powerupSpeed = 3
    powerupIndex = 0
    powerupDropRate = 1
    laserPower = False
    shield = False
    shield_image = pygame.transform.scale(pygame.image.load("ArtAssets7/cover.png"), (100,40))
    # shield_image.convert_alpha()
    shield_rect = shield_image.get_rect()

    # Backgrounds
    backgroundObject = Background('background', WINDOWHEIGHT)
    paralaxObject = Background('paralax', WINDOWHEIGHT)

    #game loop
    while True:
        # event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == timer_laser:
                laser_counter -= 1
                if laser_counter == 0:
                    pygame.time.set_timer(timer_laser, 0)
                    laserPower = False
            elif event.type == timer_shield:
                shield_counter -= 1
                if shield_counter == 0:
                    pygame.time.set_timer(timer_shield, 0)
                    shield = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_w or event.key == K_UP:
                    upHeld = True
                elif event.key == K_d or event.key == K_RIGHT:
                    rightHeld = True
                elif event.key == K_s or event.key == K_DOWN:
                    downHeld = True
                elif event.key == K_a or event.key == K_LEFT:
                    leftHeld = True
                elif event.key == K_SPACE:
                    firing = True
            elif event.type == KEYUP:
                if event.key == K_w or event.key == K_UP:
                    upHeld = False
                elif event.key == K_d or event.key == K_RIGHT:
                    rightHeld = False
                elif event.key == K_s or event.key == K_DOWN:
                    downHeld = False
                elif event.key == K_a or event.key == K_LEFT:
                    leftHeld = False
                elif event.key == K_SPACE:
                    firing = False

        # Increase Game Difficulty
        if score % 10 == 0 and levelUp:
            minAsteroidSpeed += 2
            maxAsteroidSpeed += 2
            spawnRate += 1
            levelUp = False
        elif score % 10 != 0:
            levelUp = True

        # spawn asteroids and lasers
        if firing and laserPower:
            lasers[laserIndex] = Laser(playerShip.rect, laserSpeed)
            lasers[laserIndex].rect.center = (lasers[laserIndex].rect.centerx - 30, lasers[laserIndex].rect.centery)
            laserIndex += 1
            if laserIndex >= len(lasers):
                laserIndex = 0
            lasers[laserIndex] = Laser(playerShip.rect, laserSpeed)
            lasers[laserIndex].rect.center = (lasers[laserIndex].rect.centerx + 30, lasers[laserIndex].rect.centery)
            laserIndex += 1
            if laserIndex >= len(lasers):
                laserIndex = 0
        elif firing:
            lasers[laserIndex] = Laser(playerShip.rect, laserSpeed)
            firing = False
            laserIndex += 1
            if laserIndex >= len(lasers):
                laserIndex = 0
        
        # spawn powerups
        if np.random.randint(0, (FPS)/powerupDropRate) == 0:
            powerups[powerupIndex] = PowerUp(powerupSpeed, WINDOWWIDTH)
            powerupIndex += 1
            if powerupIndex >= len(powerups):
                powerupIndex = 0

        # automate asteroid spawning
        if np.random.randint(0, FPS/spawnRate) == 0:
            asteroids[asteroidIndex] = Asteroid(np.random.randint(minAsteroidSpeed, maxAsteroidSpeed), WINDOWWIDTH, WINDOWHEIGHT)
            asteroidIndex += 1
            if asteroidIndex >= len(asteroids):
                asteroidIndex = 0

        # update state (object locations)
        playerShip.move(left=leftHeld, right=rightHeld, down=downHeld, up=upHeld)
        backgroundObject.move()
        paralaxObject.move()
        for powerup in powerups:
            if powerup != None: powerup.move()
        for laser in lasers:
            if laser != None: laser.move()
        for asteroid in asteroids:
            if asteroid != None: asteroid.move()
        if shield:
            shield_rect.center = (playerShip.rect.centerx, playerShip.rect.centery - 80)
        
        # detect collisions
        for currentPowerIndex, powerup in enumerate(powerups):
            if powerup != None:
                if playerShip.rect.colliderect(powerup.rect):
                    result = addBuff(powerup)
                    if result == 0:
                        laserPower = True
                        timer_laser = pygame.USEREVENT + 1
                        pygame.time.set_timer(timer_laser, 1000)
                        laser_counter = 5
                    elif result == 1:
                        lives += 1
                    elif result == 2:
                        shield = True
                        timer_shield = pygame.USEREVENT + 2
                        pygame.time.set_timer(timer_shield, 1000)
                        shield_counter = 5
                    powerups[currentPowerIndex] = None


        for currentAsteroidIndex, asteroid in enumerate(asteroids):
            if asteroid != None:
                for currentLaserIndex, laser in enumerate(lasers):
                    if laser != None:
                        if laser.rect.colliderect(asteroid.rect):
                            asteroids[currentAsteroidIndex] = None
                            lasers[currentLaserIndex] = None
                            score += 1
                if shield:
                    if shield_rect.colliderect(asteroid.rect):
                        asteroids[currentAsteroidIndex] = None
                if playerShip.rect.colliderect(asteroid.rect):
                    lives -= 1
                    if lives > 0:
                        playerHit()
                        playerShip.setStartPos()
                        asteroids = initializeObjects(25)
                        lasers = initializeObjects(20)
                        powerups = initializeObjects(5)
                        shield = False
                        laserPower = False
                    else:
                        return
                    break

        # draw on screen
        DISPLAYSURF.fill(BLACK)
        draw(backgroundObject.image, backgroundObject.rect)
        draw(paralaxObject.image, paralaxObject.rect)
        draw(image=playerShip.image, rect=playerShip.rect) # args = img, rect
        if shield:
            draw(shield_image, shield_rect)
        drawLasers(lasers)
        drawLasers(powerups)
        drawAsteroids(asteroids)

        drawHUD(lives, score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawHUD(lives, score):
    healthBarSurf = BASICFONT.render("Ships remaining: " + str(lives), True, WHITE)
    healthBarRect = healthBarSurf.get_rect()
    healthBarRect.topleft = (10, 10)
    draw(healthBarSurf, healthBarRect)

    scoreSurf = BASICFONT.render("Asteroids destroyed: " + str(score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH - 10, 10)
    draw(scoreSurf, scoreRect)

def addBuff(powerup):
    if powerup.type == 'triforce':
        return 0
    elif powerup.type == 'heart':
        return 1
    elif powerup.type == 'shield':
        return 2

def playerHit():
    hitSurf = BASICFONT.render("You've been destroyed!", True, WHITE)
    hitRect = hitSurf.get_rect()
    hitRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    draw(hitSurf, hitRect)
    pygame.display.update()
    pygame.time.wait(2000)

def initializeObjects(num):
    objects = []
    for x in range(num):
        objects.append(None)
    return objects

def draw(image, rect):
    DISPLAYSURF.blit(image, rect)

def drawLasers(lasers):
    for laser in lasers:
        if laser != None:
            draw(laser.image, laser.rect)

def drawAsteroids(asteroids):
    for asteroid in asteroids:
        if asteroid != None:
            image, rect = asteroid.draw()
            draw(image, rect)

def terminate():
    pygame.quit()
    sys.exit()

def showStartScreen():
    return

def showGameOverScreen():
    return
    
if __name__ == '__main__':
    main()

