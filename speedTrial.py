import pygame
from PIL import Image
import time
import random
from pygame.locals import *
from threading import *

# COLORS stored in RGB format
black = (0, 0, 0)
white = (255, 255, 255)
red = (160, 0, 0)
green = (30, 140, 30)
blue = (0, 0, 160)
grey = (200, 200, 200)

pygame.init() # initializes program

# display
display_width = 800
display_height = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Speed Trial')

global timeElapsed
timeElapsed = 0
global zActive
zActive = 2
global activeTarget
activeTarget = 4
global tempActiveTarget
tempActiveTarget = 5
global start

clock = pygame.time.Clock()

pygame.time.set_timer(USEREVENT + 1, 800)

gameFont = pygame.font.SysFont('CharlemagneStd-Bold.otf', 20)

# all PLAYER IMAGES stored as variables
playerStage1 = pygame.image.load('C:/Programming/PythonProjects/PyGame/speedTrial/playerStage1.png')
with Image.open('C:/Programming/PythonProjects/PyGame/speedTrial/playerStage1.png') as img:
    width, height = img.size

directionMarker = pygame.image.load('C:/Programming/PythonProjects/PyGame/speedTrial/directionDetector.png')
with Image.open('C:/Programming/PythonProjects/PyGame/speedTrial/directionDetector.png') as Ximg:
    width, height = Ximg.size

zTool = pygame.image.load('C:/Programming/PythonProjects/PyGame/speedTrial/zTool.png')
zToolActive = pygame.image.load('C:/Programming/PythonProjects/PyGame/speedTrial/zToolActive.png')
xTool = pygame.image.load('C:/Programming/PythonProjects/PyGame/speedTrial/xTool.png')
xToolActive = pygame.image.load('C:/Programming/PythonProjects/PyGame/speedTrial/xToolActive.png')

# definitions of functions

def player(playerStage, xplayer, yplayer):
    gameDisplay.blit(playerStage, (xplayer, yplayer))

def dMarker(xmarker, ymarker):
    gameDisplay.blit(directionMarker, (xmarker, ymarker))

def whichTool():
    global zActive
    if random.randint(0, 1) == 0:
        zActive = 1
    else:
        zActive = 0

def whichTarget():
    global activeTarget
    tempRandomTarget = random.randint(0, 3)
    if tempRandomTarget == 0:
        activeTarget = 0
    elif tempRandomTarget == 1:
        activeTarget = 1
    elif tempRandomTarget == 2:
        activeTarget = 2
    elif tempRandomTarget == 3:
        activeTarget = 3

def display_message(text, size, x, y):
    gameFont = pygame.font.Font('C:/Windows/Fonts/CharlemagneStd-Bold.otf', size)
    message = gameFont.render(text, 1, black)
    gameDisplay.blit(message, (x, y))

def game_over():
    global start
    global difchange
    display_message('You lose, start over', 50, 80, 250)

    display_message('Would you like to', 25, 270, 300)
    display_message('go up a difficulty?', 25, 264, 330)

    display_message('YES  //  NO', 40, 275, 490)
    display_message('enter \'y\' or \'n\'', 25, 280, 527)
    userInput = 0
    difchange = 0

    pygame.display.update()

    while userInput == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_y:
                    userInput = 1
                    difchange = 1
                elif event.key == pygame.K_n:
                    userInput = 1
                    difchange = 0

    # time.sleep(2)
    
    print(userInput, difchange)
    game_loop()
    start = 1


class Indicators:

    def target(self, xtarget, ytarget, color, wtarget=100, htarget=200):
        pygame.draw.rect(gameDisplay, color, [xtarget, ytarget, wtarget, htarget])

    def tool(self, wTool, xtool, ytool):
        gameDisplay.blit(wTool, (xtool, ytool))

option1 = Indicators()
option2 = Indicators()
option3 = Indicators()
option4 = Indicators()

def game_loop():
    global timeElapsed
    global numWrong
    global start
    global prevNumberCount
    numRight = 0
    numWrong = 0
    targetHit = 0

    xplayer = ((display_width / 2) - (img.size[0] / 2))
    yplayer = display_height - img.size[0]

    xmarker = xplayer - Ximg.size[0]
    ymarker = yplayer
    roundWon = False
    exitGame = False

    prevNumberCount = [numRight, numWrong]

    whichTarget()
    whichTool()
    tempActiveTarget = activeTarget

    def blank_game():
        gameDisplay.fill(grey)
        player(playerStage1, xplayer, yplayer)
        dMarker(xmarker, ymarker)

        option1.target((display_width - display_width), (display_height - 200), blue)
        option2.target((display_width - display_width), (display_height - 500), blue)
        option3.target((display_width - 100), (display_height - 500), blue)
        option4.target((display_width - 100), (display_height - 200), blue)

        option1.tool(zTool, 480, 50)
        option3.tool(xTool, 600, 50)

    if start == 1:
        for word in ['Ready', 'Set', 'Go']:
            display_message(word, 40, 400, 400)
            pygame.display.update()
            time.sleep(0.8)
            blank_game()

    while exitGame==False:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_w:
                    yplayer = 300
                    ymarker = 300
                elif event.key == pygame.K_s:
                    yplayer = 600
                    ymarker = 600
                elif event.key == pygame.K_a:
                    xmarker = xplayer - Ximg.size[0]
                elif event.key == pygame.K_d:
                    xmarker = xplayer + img.size[0]
                elif event.key == pygame.K_z:
                    if zActive == 1:
                        if activeTarget == 0:
                            if ymarker == 600 and xmarker == (xplayer - Ximg.size[0]):
                                numRight += 1
                                if numRight == prevNumberCount[0] + 1:
                                    continue

                                targetHit = 1
                            else:
                                 numWrong += 1
                                 targetHit = 0
                        elif activeTarget == 1:
                            if ymarker == 300 and xmarker == (xplayer - Ximg.size[0]):
                                numRight += 1
                                if numRight == prevNumberCount[0] + 1:
                                    continue
                                targetHit = 1
                            else:
                                 numWrong += 1
                                 targetHit = 0

                        elif activeTarget == 2:
                            if ymarker == 300 and xmarker == (xplayer + img.size[0]):
                                numRight += 1
                                if numRight == prevNumberCount[0] + 1:
                                    continue
                                targetHit = 1
                            else:
                                 numWrong += 1
                                 targetHit = 0
                        elif activeTarget == 3:
                            if ymarker == 600 and xmarker == (xplayer + img.size[0]):
                                numRight += 1
                                if numRight == prevNumberCount[0] + 1:
                                    continue
                                targetHit = 1
                            else:
                                 numWrong += 1
                                 targetHit = 0
                    else:
                        numWrong += 1
                        targetHit = 0
                elif event.key == pygame.K_x:
                    if zActive == 0:
                        if activeTarget == 0:
                            if ymarker == 600 and xmarker == (xplayer - Ximg.size[0]):
                                numRight += 1
                                if numRight == prevNumberCount[0] + 1:
                                    continue
                                targetHit = 1
                            else:
                                numWrong += 1
                                targetHit = 0
                        elif activeTarget == 1:
                            if ymarker == 300 and xmarker == (xplayer - Ximg.size[0]):
                                numRight += 1
                                if numRight == prevNumberCount[0] + 1:
                                    continue
                                targetHit = 1
                            else:
                                numWrong += 1
                                targetHit = 0
                        elif activeTarget == 2:
                            if ymarker == 300 and xmarker == (xplayer + img.size[0]):
                                numRight += 1
                                if numRight == prevNumberCount[0] + 1:
                                    continue
                                targetHit = 1
                            else:
                                numWrong += 1
                                targetHit = 0
                        elif activeTarget == 3:
                            if ymarker == 600 and xmarker == (xplayer + img.size[0]):
                                numRight += 1
                                if numRight == prevNumberCount[0] + 1:
                                    continue
                                targetHit = 1
                            else:
                                numWrong += 1
                                targetHit = 0
                    else:
                        numWrong += 1
                        targetHit = 0
                # else:
                #     numWrong += 1
                #     targetHit = 0

            elif event.type == USEREVENT + 1:
                whichTool()
                whichTarget()

                if activeTarget == tempActiveTarget:
                    whichTarget()

                if numRight == prevNumberCount[0] and start == 0:
                    # if targetHit == 0:
                    numWrong += 1

        blank_game()

        if timeElapsed > 5:

            if  zActive == 1:
                option2.tool(zToolActive, 480, 50)
                option3.tool(xTool, 600, 50)
            elif zActive == 0:
                option4.tool(xToolActive, 600, 50)
                option1.tool(zTool, 480, 50)

        if activeTarget == 0:
            option1.target((display_width - display_width), (display_height - 200), red)
        elif activeTarget == 1:
            option2.target((display_width - display_width), (display_height - 500), red)
        elif activeTarget == 2:
            option3.target((display_width - 100), (display_height - 500), red)
        elif activeTarget == 3:
            option4.target((display_width - 100), (display_height - 200), red)


        # every 0.05 second reset modifier
        timeElapsed += 1
        if timeElapsed > 60: # 46 for 800 mili
            timeElapsed = 0

        if numWrong >= 25:
            game_over()


        # print(timeElapsed)
        display_message('hit: {}'.format(numRight), 40, 10, 70)

        display_message('missed: {}'.format(numWrong), 40, 10, 140)
        tempActiveTarget = activeTarget

        start = 0

        pygame.display.update()
        clock.tick(60)

start = 1
game_loop()
pygame.quit()
quit()
