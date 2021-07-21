#from posix import WCOREDUMP
import random, pygame, sys
from pygame import draw
from pygame import time
from pygame.event import get, post
from pygame.locals import*
from pygame.time import delay


WINDOWWIDTH = 800
WINDOWHEIGHT = 640
CELLSIZE = 40

assert WINDOWWIDTH % CELLSIZE == 0, "window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

CELLWIDTH = int(WINDOWWIDTH/ CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT/ CELLSIZE)

image = pygame.image.load('./Arts/brazilianapple.png')
new_image = pygame.transform.scale(image, (CELLSIZE, CELLSIZE))
new_image.set_colorkey((255, 0,  0))

orange_apple = pygame.image.load('./Arts/orange.png')
orange_image = pygame.transform.scale(orange_apple, (CELLSIZE, CELLSIZE))

white_appel = pygame.image.load('./Arts/appleLOGO.png')
white_image = pygame.transform.scale(white_appel, (CELLSIZE, CELLSIZE))
new_image.set_colorkey((0,0,0))

green_apple = pygame.image.load('./Arts/green_apple.png')
green_image = pygame.transform.scale(green_apple, (CELLSIZE, CELLSIZE))
green_image.set_colorkey((0,255,0))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155,0)
DARKGRAY = (40, 40, 40)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BGCOLOR = BLACK

UP = "up"
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # = pygame.font.FONT('freesansbold.ttf', 18)
    pygame. display.set_caption('Wormy')
    
    showStartScreen()
    while True:
        runGame()
        #drawScore()
        showGameOverScreen()


def runGame():

    #direction = RIGHT  # BOTAR EM 
    
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    direction = RIGHT
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    apple = getRandomLocation()
    apple_green = getRandomLocation()
    apple_orange = getRandomLocation()
    poison_apple = getRandomLocation()

    FPS = 15

    while True:
        #direction = RIGHT
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE :
                    terminate()

        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == CELLHEIGHT :
            
            return
        for wormSegment in wormCoords[3:]:
            if wormSegment['x'] == wormCoords[HEAD]['x'] and wormSegment['y'] == wormCoords[HEAD]['y']:
                return
        
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()


        elif wormCoords[HEAD]['x'] == apple_green['x'] and wormCoords[HEAD]['y'] == apple_green['y']:
            apple_green = getRandomLocation()
            FPS += 5
        elif wormCoords[HEAD]['x'] == apple_orange['x'] and wormCoords[HEAD]['y'] == apple_orange['y']:
            apple_orange = getRandomLocation()
            if FPS > 15:
                FPS -= 5

        elif wormCoords[HEAD]['x'] == poison_apple['x'] and wormCoords[HEAD]['y'] == poison_apple['y']:
            poison_apple= getRandomLocation()
            del wormCoords[-1] 
            del wormCoords[-1] 
            if len(wormCoords) < 3:
                return

        else:
            del wormCoords[-1]

        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}

        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)



        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawAplle(apple)
        draw_Apple_Green(apple_green)
        draw_apple_orange(apple_orange)
        draw_poison_apple(poison_apple)
        drawScore(len(wormCoords) - 3)
        win_mode(wormCoords)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomLocation():

    return {'x': random.randint(0, CELLWIDTH -1), 'y': random.randint(0, CELLHEIGHT -1)}


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def drawWorm(wormCoords):
    for segment in wormCoords:
        x = segment['x'] * CELLSIZE
        y = segment['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, BLUE, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x+4, y+4, CELLSIZE -8, CELLSIZE -8)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormInnerSegmentRect)

def drawAplle(apple):
    x = apple['x'] * CELLSIZE 
    y = apple['y'] * CELLSIZE 
    appleSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleSegmentRect)
    DISPLAYSURF.blit(new_image, (x, y))

def draw_Apple_Green(apple_green):
    x_green = apple_green['x'] * CELLSIZE
    y_green = apple_green['y'] * CELLSIZE
    appleSegmentRectGreen = pygame.Rect(x_green, y_green, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GREEN, appleSegmentRectGreen)
    DISPLAYSURF.blit(green_image, (x_green, y_green))
    

def draw_apple_orange(apple_orange):
    x_orange = apple_orange['x'] * CELLSIZE
    y_orange = apple_orange['y'] * CELLSIZE
    appleSegmentRectOrange = pygame.Rect(x_orange, y_orange, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, (255, 127, 0), appleSegmentRectOrange)
    DISPLAYSURF.blit(orange_image, (x_orange, y_orange))


def draw_poison_apple(poison_apple):                   # preciso ver isso ainda 
    x_posion = poison_apple['x'] * CELLSIZE
    y_posion = poison_apple['y'] * CELLSIZE
    poisonAppleSegmentRect = pygame.Rect(x_posion, y_posion, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, (255,255,255), poisonAppleSegmentRect)
    DISPLAYSURF.blit(white_image, (x_posion, y_posion))

def drawScore(score):

    scoreScreen = pygame.font.Font('freesansbold.ttf', 20)
    game_score = scoreScreen.render('Score: '+str(score), True, WHITE)
    score_rect = game_score.get_rect()
    score_rect.midtop = (WINDOWWIDTH/8, 10)
    


    DISPLAYSURF.blit(game_score, score_rect)
    
    pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()

def showGameOverScreen():

    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH/2, 10)
    overRect.midtop = (WINDOWWIDTH/2, gameRect.height + 10 +25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    pygame.display.update()
    pygame.time.wait(500)
    checkForkeyPress()

    while True:
        if checkForkeyPress():
            pygame.event.get()
            return

def checkForkeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            else:
                return True

    return False

def win_mode(wormCoords):
    if len(wormCoords) == 33:
        win_screen = pygame.font.Font('freesansbold.ttf', 120)
        win_ask = win_screen.render('YOU WIN !!', True, BLUE)
        win_rect = win_ask.get_rect()
        win_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

        DISPLAYSURF.blit(win_ask, win_rect)
        pygame.display.update()
        pygame.time.wait(2000)
        terminate()
        
    
def showStartScreen():
    start_screen = pygame.font.Font('freesansbold.ttf', 50)
    start_screen_sumary = pygame.font.Font('freesansbold.ttf', 20)
    start_ask = start_screen.render('Ready to start the game?', True, WHITE)
    start_ask_red_apple = start_screen_sumary.render('Red apple: Just to increase your wormy', True, RED)#.Apple green: It will increase both your wormy and velocity\nApple orange: It will increase your wormy but will decrease your velocity for normal one',True, RED)
    start_ask_green_apple = start_screen_sumary.render('Green apple: It will increase both your wormy and velocity', True, GREEN)
    start_ask_white_apple = start_screen_sumary.render('White apple: It will poison your wormy and decrease it', True, WHITE)
    start_ask_orange_apple = start_screen_sumary.render('Orange: It will increase your wormy and decrease velocity', True, ORANGE)

    start_rect = start_ask.get_rect()
    start_ask_red_apple_rect = start_ask_red_apple.get_rect()
    start_ask_red_apple_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 60)
    start_ask_green_apple_rect = start_ask_green_apple.get_rect()
    start_ask_green_apple_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 80)
    start_ask_white_apple_rect = start_ask_white_apple.get_rect()
    start_ask_white_apple_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 100)
    start_ask_orange_apple_rect = start_ask_orange_apple.get_rect()
    start_ask_orange_apple_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 120)
    start_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    DISPLAYSURF.blit(start_ask, start_rect)
    DISPLAYSURF.blit(start_ask_red_apple, start_ask_red_apple_rect)
    DISPLAYSURF.blit(start_ask_green_apple, start_ask_green_apple_rect)
    DISPLAYSURF.blit(start_ask_white_apple, start_ask_white_apple_rect)
    DISPLAYSURF.blit(start_ask_orange_apple, start_ask_orange_apple_rect)

    pygame.display.update()
    pygame.time.wait(5000)    

    """ time_screen = start_screen.render('Time : '+str(),True, WHITE)
        time_screen_rect = time_screen.get_rect()
        time_screen_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/4)
        DISPLAYSURF.blit(time_screen, time_screen_rect)"""


if __name__ == '__main__':
    main()