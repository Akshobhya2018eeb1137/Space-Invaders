import pygame
from PIL import Image
import random
import math
import time
from pygame import mixer
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)
mixer.music.load('background.wav')
mixer.music.play(-1)

'''
img = Image.open('newPlayer.png')
img = img.resize((64, 64))
img.save('resPlayer.png')
'''
playerImg = pygame.image.load('resPlayer.png')
runningGame = 1
enemyImg = pygame.image.load('alien.png')
bulletImg = pygame.image.load('bullet.png')

font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10
GameOVERfont = pygame.font.Font('freesansbold.ttf', 256)
x_player = 340
y_player = 480

dx = 2
x_bullet = x_player
y_bullet = y_player
dy_bullet = 5
dX_enemy = []
dY_enemy = []
dX_enemy_VAL = 5
dY_enemy_VAL = 0.1
noOfEnemies = 10
x_enemy = []
y_enemy = []

for i in range(noOfEnemies):
    x_enemy.append(random.randint(0, 690))
    y_enemy.append(random.randint(30, 60))
    dX_enemy.append(dX_enemy_VAL)
    dY_enemy.append(dY_enemy_VAL)

def printScore(num):
    marks = font.render("Score: " + str(num), True, (255, 255, 255))
    screen.blit(marks, (scoreX, scoreY))
def printGameOVER():
    marks = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(marks, (300, 250))
def player(x, y):
    screen.blit(playerImg, (x, y))
def enemy(x, y):
    screen.blit(enemyImg, (x, y))
def bullet(x, y):
    screen.blit(bulletImg, (x, y))
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distbw = math.sqrt((enemyX - bulletX)** 2 + (enemyY - bulletY)** 2)
    if distbw < 30:
        return 1
    return 0
fired = 0   
readyToFire = 1
first = 0
score = 0
background = pygame.image.load('background.png')
while runningGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runningGame = 0
            break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x_player -= dx
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x_player += dx
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        y_player -= dx
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y_player += dx
    
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
        
    for i in range(noOfEnemies):
        if y_enemy[i] > 350:
            for j in range(noOfEnemies):
                y_enemy[j] = 4000
            runningGame = 0
            screen.blit(background, (0, 0))
            printGameOVER()
            break
        
        y_enemy[i] += dY_enemy[i]
        x_enemy[i] += dX_enemy[i]
        x_enemy[i] = max(-10, x_enemy[i])
        y_enemy[i] = max(0, y_enemy[i])
        x_enemy[i] = min(690, x_enemy[i])
        y_enemy[i] = min(480, y_enemy[i])
        if x_enemy[i] >= 680:
            dX_enemy[i] = -dX_enemy[i]
        elif x_enemy[i] <= 0:
            dX_enemy[i] = -dX_enemy[i]
        player(x_player, y_player)
        if keys[pygame.K_SPACE] and not fired:
            bullet(x_player + 16, y_player + 10)
            x_bullet = x_player + 16
            y_bullet = y_player + 10
            fired = 1
            mixer.Sound('laser.wav').play()
            readyToFire = 0
            first = 1
        if fired and not readyToFire:
            y_bullet -= dy_bullet
        x_player = max(-10, x_player)
        x_player = min(690, x_player)
        y_player = min(480, y_player)
        y_player = max(0, y_player)
        if fired and first:
            x_bullet = x_player + 16
            y_bullet = y_player + 10
            first = 0
        if fired:
            bullet(x_bullet, y_bullet)
        if y_bullet <= -100:
            readyToFire = 1
            fired = 0
            first = 0
        
        if fired and isCollision(x_enemy[i], y_enemy[i], x_bullet, y_bullet):
            fired = 0
            readyToFire = 1
            score += 1
            first = 0
            mixer.Sound('explosion.wav').play()
            x_enemy[i] = random.randint(0, 690)
            y_enemy[i] = random.randint(30, 50)
        else:
            enemy(x_enemy[i], y_enemy[i])
    printScore(score)
    if not runningGame:
        time.sleep(5)
    pygame.display.update()
