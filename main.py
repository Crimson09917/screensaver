from random import randint
import pygame
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((100,100), pygame.FULLSCREEN)
pygame.mouse.set_visible(0)

def chooseImage():
    images = ["red.png", "blu.png", "yellow.png", "green.png"]
    x = randint(0,3)
    return pygame.image.load("images/"+images[x])

def updateVector(wall, v):
    variance = 1
    x = v["x"]
    y = v["y"]

    if wall == "left":
        return {"x":-1*x, "y":y+randint(-1*variance, variance)}

    elif wall == "top":
        return {"x":x+randint(-1*variance, variance), "y":-1*y}

    elif wall == "bottom":
        return {"x":x+randint(-1*variance, variance), "y":-1*y}

    elif wall == "right":
        return {"x":-1*x, "y":y+randint(-1*variance, variance)}

def checkCorner(LS, RS, TS, BS):
    global screenHeight
    global screenWidth
    bound = 5

    if LS <= bound and TS <= bound:
        return True
    elif RS >= screenWidth-bound and TS <= bound:
        return True
    elif LS <= bound and BS >= screenHeight-bound:
        return True
    elif RS >= screenWidth-bound and BS >= screenHeight-bound:
        return True
    return False

screenWidth, screenHeight = pygame.display.get_surface().get_size()
bg = chooseImage()
bgWidth, bgHeight = bg.get_size()

xPos = 0
yPos = 0

leftSide = 50
rightSide = bgWidth+50
topSide = 50
bottomSide = bgHeight+50
borders = [leftSide, topSide, rightSide, bottomSide]
v = {"x":5, "y":5}
mainLoop = True
gTriggered = False

walls = [0, screenWidth, 0, screenHeight]

rick = pygame.image.load("images/rick.png")
rickWidth, rickHeight = rick.get_size()

while mainLoop:
    pygame.time.delay(10)
    window.fill((0,0,0))
    changeImage = False

    while True:
        newLeftSide = leftSide+v["x"]
        newRightSide = rightSide+v["x"]
        newTopSide = topSide+v["y"]
        newBottomSide = bottomSide+v["y"]

        if checkCorner(newLeftSide, newRightSide, newTopSide, newBottomSide) == True:
            gTriggered = True

        if newLeftSide < walls[0]:
            v = updateVector("left", v)
            changeImage = True
            continue
        if newRightSide > walls[1]:
            v = updateVector("right", v)
            changeImage = True
            continue
        if newTopSide < walls[2]:
            v = updateVector("top", v)
            changeImage = True
            continue
        if newBottomSide > walls[3]:
            v = updateVector("bottom", v)
            changeImage = True
            continue
    
        leftSide = newLeftSide
        rightSide = newRightSide
        topSide = newTopSide
        bottomSide = newBottomSide
        break
    
    if not gTriggered:
        if changeImage == False:
            window.blit(bg, (leftSide, topSide))
        else:
            bg = chooseImage()
            window.blit(bg, (leftSide, topSide))
    else:
        window.blit(rick, (leftSide, topSide))
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainLoop = False
            if event.key == pygame.K_g:
                gTriggered = True
            if event.key == pygame.K_UP:
                if v["x"] < 0:
                    v["x"] -= 1

                if v["y"] < 0:
                    v["y"] -= 1
                    
            if event.key == pygame.K_DOWN:
                if v < 0:
                    v["x"] += 1
                    v["y"] += 1
                else:
                    v["x"] -= 1
                    v["y"] -= 1
            
            if event.key == pygame.K_q:
                walls = [-5000, screenWidth+5000, -5000, screenHeight+5000]

    pygame.display.update()

pygame.quit()
