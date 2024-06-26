import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Load background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('player.png')
x = 370
y = 480
x_change = 0

# Enemy
enemyimg = []
x1 = []
y1 = []
ex_change = []
ey_change = []
num_of_enemeies = 6
for i in range(num_of_enemeies):
    enemyimg.append(pygame.image.load('enemy.png'))
    x1.append(random.randint(0, 736))
    y1.append(random.randint(50, 150))
    ex_change.append(2)
    ey_change.append(40)

# Bullet
bulletimg = pygame.image.load('bullet.png')
xb = 0
yb = 480
bx_change = 0
by_change = 10
bState = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x1, y1, i):
    screen.blit(enemyimg[i], (x1, y1))

def bullet_fire(xb, yb):
    global bState   
    bState = "fire"
    screen.blit(bulletimg, (xb + 16, yb + 10))

def iscollision(x1, y1, xb, yb):
    distance = math.sqrt(math.pow(x1 - xb, 2) + math.pow(y1 - yb, 2))
    if distance < 27:
        return True
    else: 
        return False

def player_enemy_collision(player_x, player_y, enemy_x, enemy_y):
    distance = math.sqrt(math.pow(player_x - enemy_x, 2) + math.pow(player_y - enemy_y, 2))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
game_over = False
while running:
    # RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke for left and right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            if event.key == pygame.K_RIGHT:
                x_change = 5
            if event.key == pygame.K_SPACE:
                if bState == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    xb = x
                    bullet_fire(xb, yb)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0

    if not game_over:
        x += x_change
        # Boundary check for player
        if x <= 0:
            x = 0
        elif x >= 736:
            x = 736

        # Boundary check for enemy   
        for i in range(num_of_enemeies):
            if y1[i] > 550:
                for j in range(num_of_enemeies):
                    y1[j] = 2000
                game_over = True
                break

            x1[i] += ex_change[i]
            if x1[i] <= 0:
                ex_change[i] = 2
                y1[i] += ey_change[i]
            elif x1[i] >= 736:
                ex_change[i] = -2
                y1[i] += ey_change[i]

            # Collision with bullet
            collision = iscollision(x1[i], y1[i], xb, yb)
            if collision:
                collision_sound = mixer.Sound('explosion.wav')
                collision_sound.play()
                yb = 480
                bState = "ready"
                score_value += 1
                x1[i] = random.randint(0, 736)
                y1[i] = random.randint(30, 150)

            # Collision with player
            if player_enemy_collision(x, y, x1[i], y1[i]):
                for j in range(num_of_enemeies):
                    y1[j] = 2000
                game_over = True
                break

            enemy(x1[i], y1[i], i)

        # Bullet movement
        if bState == "fire":
            bullet_fire(xb, yb)
            yb -= by_change
            if yb <= 0:
                yb = 480
                bState = "ready"

        player(x, y)
        show(textX, textY)
    else:
        game_over_text()

    pygame.display.update()  # Updating the display
 