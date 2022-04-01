
import math
import random

import pygame

from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders!")

game_icon = pygame.image.load("icon.png")
pygame.display.set_icon(game_icon)

background = pygame.image.load("background.png")


# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 50)

text_x = 10
text_y = 0


# Game Over text

gover_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    gover_text = gover_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gover_text, (200, 250))


# Player (Image from: https://www.flaticon.com/free-icons/spaceship)
player_img = pygame.image.load("spaceship.png")
player_x = 370
player_y = 480
player_x_change = 0

# Enemy (Image from: https://www.flaticon.com/free-icons/alien)
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemies_num = 10

for i in range(enemies_num):

    enemy_img.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 75))
    enemy_x_change.append(0.6)
    enemy_y_change.append(60)

# Bullet (Image from: https://www.flaticon.com/free-icons/bullet)
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 1.5
bullet_state = "Ready"


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_colliding(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) +
                         (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop

running = True

while running:

    screen.fill((255, 255, 255))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.6
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":

                    bullet_sound = mixer.Sound("laser8bit.wav")
                    bullet_sound.play()

                    bullet_x = player_x

                    fire_bullet(bullet_x, bullet_y)

    player_x += player_x_change

    # Player Movement
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy Movement
    for i in range(enemies_num):

        # Game Over

        if enemy_y[i] >= 440:
            for a in range(enemies_num):
                enemy_y[a] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.6
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.6
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_colliding(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "Ready"
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 75)
            score_value += 1

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "Ready"
    if bullet_state is "Fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
