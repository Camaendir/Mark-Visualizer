import pygame, sys
from pygame.locals import *

BLACK = (0, 0, 0)
GREY = (120, 120, 120)

leftAndRight = [(1.0, 4.0)]
fullCP = [0]
maxCP = 180
noteSumms = [0]


def addMark(data):
    cp = int(data[0])
    mark = float(data[1])
    itteration = len(fullCP)
    newCP = fullCP[itteration - 1] + cp
    fullCP.append(newCP)
    newsumm = noteSumms[itteration - 1] + mark * cp
    noteSumms.append(newsumm)
    upperLimit = newsumm / 180 + (maxCP - newCP) / 180
    lowerLimit = newsumm / 180 + (maxCP - newCP) * 4 / 180
    leftAndRight.append((upperLimit, lowerLimit))


def drawCirclesAndLines():
    t_height = 600
    t_width = 450
    verticalSize = 500
    horizontalSize = 400
    horizontalPadding = 25
    verticalPadding = 50
    itterations = len(leftAndRight)
    stepSize = verticalSize / (itterations - 1)
    lastPoints = [(0, 0), (0, 0)]

    mark_step = horizontalSize / 3
    for i in range(4):
        pygame.draw.line(screen, GREY, (horizontalPadding + i * mark_step, verticalPadding),
                         (horizontalPadding + i * mark_step, verticalPadding + verticalSize))

    for i in range(itterations):
        height = int(verticalSize + verticalPadding - (i * stepSize))
        left = int((leftAndRight[i][0] - 1) * horizontalSize / 3 + horizontalPadding)
        right = int((leftAndRight[i][1] - 1) * horizontalSize / 3 + horizontalPadding)
        pygame.draw.circle(screen, BLACK, (left, height), 5)
        pygame.draw.circle(screen, BLACK, (right, height), 5)
        if i is not 0:
            pygame.draw.line(screen, BLACK, lastPoints[0], (left, height), 1)
            pygame.draw.line(screen, BLACK, lastPoints[1], (right, height), 1)
        lastPoints = [(left, height), (right, height)]


pygame.init()
screen = pygame.display.set_mode((450, 600))
pygame.display.set_caption("Notenbestimmung")
screen.fill((255, 255, 255))

file = open("marks.mks", "r")
for line in file.readlines():
    addMark(line.split(" "))
file.close()

drawCirclesAndLines()

print(leftAndRight[len(leftAndRight) - 1])

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
