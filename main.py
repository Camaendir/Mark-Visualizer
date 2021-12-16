import pygame, sys
from pygame.locals import *
from time import sleep

BLACK = (0, 0, 0)
GREY = (120, 120, 120)
RED = (255, 0, 0)

leftAndRight = [(1.0, 4.0)]
fullCP = [0]
maxCP = 180
noteSumms = [0]
fullSum = 0
countingMarks = 0
averages = [-1]
last_average = []


def addMark(data):
    global last_average
    global maxCP, fullSum, countingMarks, averages
    cp = int(data[0])
    mark = data[1]
    itteration = len(fullCP)
    if mark.lower() == "b":
        newsumm = noteSumms[itteration - 1]
        maxCP = maxCP - cp
        fullCP.append(fullCP[itteration - 1])
        newCP = fullCP[itteration - 1]
    else:
        mark = float(mark)
        fullSum += mark
        countingMarks += 1
        newsumm = noteSumms[itteration - 1] + mark * cp
        newCP = fullCP[itteration - 1] + cp
        fullCP.append(newCP)
        if len(data) == 2:
            last_average.append((cp, mark))
    
    noteSumms.append(newsumm)
    if fullCP[-1] != 0:
        averages.append(newsumm / fullCP[-1])
    else:
        averages.append(averages[-1])
    upperLimit = (newsumm + maxCP - newCP) / 180
    lowerLimit = (newsumm + (maxCP - newCP) * 4) / 180
    leftAndRight.append((upperLimit, lowerLimit))


def drawCirclesAndLines(screen):
    myfont = pygame.font.SysFont(None, 15)
    t_height = 600
    t_width = 450
    verticalSize = 500
    horizontalSize = 400
    horizontalPadding = 25
    verticalPadding = 50
    itterations = len(leftAndRight)
    stepSize = verticalSize / (itterations - 1)
    lastPoints = [(0, 0), (0, 0), (0,0)]

    mark_step = horizontalSize / 3
    for i in range(4):
        pygame.draw.line(screen, GREY, (horizontalPadding + i * mark_step, verticalPadding),
                         (horizontalPadding + i * mark_step, verticalPadding + verticalSize))

    for i in range(itterations):
        height = int(verticalSize + verticalPadding - (i * stepSize))
        left = int((leftAndRight[i][0] - 1) * horizontalSize / 3 + horizontalPadding)
        right = int((leftAndRight[i][1] - 1) * horizontalSize / 3 + horizontalPadding)
        avg = int((averages[i] - 1) * horizontalSize / 3 + horizontalPadding)
        pygame.draw.circle(screen, BLACK, (left, height), 5)
        pygame.draw.circle(screen, BLACK, (right, height), 5)
        if averages[i] != -1:
            label = myfont.render(f"{averages[i]:.3}", 1, GREY)
            screen.blit(label, (avg + 10, height-10))
            pygame.draw.circle(screen, RED, (avg, height), 5)
        if i != 0:
            pygame.draw.line(screen, BLACK, lastPoints[0], (left, height), 1)
            pygame.draw.line(screen, BLACK, lastPoints[1], (right, height), 1)
        if averages[i-1] != -1:
            pygame.draw.line(screen, RED, lastPoints[2], (avg, height), 1)
        lastPoints = [(left, height), (right, height), (avg, height)]

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((450, 600))
    pygame.display.set_caption("Notenbestimmung")
    screen.fill((255, 255, 255))
    
    filename = "marks.mks"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename, "r") as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            addMark(line.split(" "))

    drawCirclesAndLines(screen)

    print(f"Possible final grades: {leftAndRight[-1][0]:1.3} - {leftAndRight[-1][1]:1.3}")
    print(f"Average grade: {averages[-1]}")
    print(last_average) 

    cp_sum = 0
    for i in range(len(last_average)):
        cp_sum += last_average[i][0]

    average = float(0)
    for i in range(len(last_average)):
        average += last_average[i][1] * last_average[i][0] / cp_sum

    print(average)
    
    while True:
        sleep(1)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
