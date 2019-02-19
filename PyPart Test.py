import PyParticles
import pygame
import random as rand
import numpy as np
from datetime import datetime
from sys import getsizeof



pygame.init()
clock = pygame.time.Clock()
width = 800
height = 600


def rgb(minimum, maximum, value): #rgb function which returns rgb value depending on speed
    if value > maximum: #makes sure value given cannot exceed max
        value = maximum
    #minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b



gameDisplay = pygame.display.set_mode((width, height)) #creates display
pygame.display.set_caption("title") #sets title


env = PyParticles.Environment(width, height, (np.pi, 0))



env.addParticles(100, size = 5, speed=1)

fps = 60
frame = 0
time = 0


looptimes = np.array([])

showgrid = False
fillgrid = False

running = True
pause = False
i=1
while running:
    i += 1

    startTime = datetime.now()
    gameDisplay.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_g:
                showgrid = not showgrid
            if event.key == pygame.K_f:
                fillgrid = not fillgrid
    

    if fillgrid == True:
        for p in env.particles:
            for cell in p.cells:
                index = np.argwhere(env.squarepointers == cell)
                #print(index)
                toplefty = index[0][0]*env.squareheight
                topleftx = index[0][1]*env.squarewidth
                pygame.draw.rect(gameDisplay, (205, 205, 205), (topleftx, toplefty, env.squarewidth, env.squareheight))
    
    
    for p in env.particles:
        p.colour = rgb(0, 30, p.speed)
        pygame.draw.circle(gameDisplay, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)
    
    
    if showgrid == True:
        for i in range(0, env.cols + 1):
            pointA = [i*env.squarewidth, 0]
            pointB = [i*env.squarewidth, env.height]
            pointC = [0, i*env.squareheight]
            pointD = [env.width, i*env.squareheight]
            pygame.draw.line(gameDisplay, (255, 255, 255), pointA, pointB)
            pygame.draw.line(gameDisplay, (255, 255, 255), pointC, pointD)    
            
            
    if pause == False:
        env.update()
    
    clock.tick(fps)
    
    frame+=1
    time = frame/fps
    
    pygame.display.update()
    
    looptimes = np.append(looptimes, ((datetime.now() - startTime).microseconds))
    


print("Finished!")       
print("Time: " + str(int(np.mean(looptimes))))
pygame.quit()



