import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.display.set_caption("ALIEN INVASION ON EARTH")
background = pygame.image.load("wall.jpg")
scaled_img = pygame.transform.scale(background, (800, 600))

mixer.music.load("aliensong.wav")
mixer.music.play(-1)

player_img = pygame.image.load("spaceship.png")
player_a = 368
player_b = 480
player_a_change = 0


enemy_img = []
enemy_a = []
enemy_b = []
enemy_a_change = []
enemy_b_change = []
enemy_number = 10


for i in range(enemy_number):
    enemy_img.append(pygame.image.load("alien.png"))
    enemy_a.append(random.randint(0,735))
    enemy_b.append(random.randint(50,150))
    enemy_a_change.append(.5)
    enemy_b_change.append(40)


bullet_img = pygame.image.load("bullet.png")
bullet_a = 0
bullet_b = 480
# bullet_a_change = 0
bullet_b_change = 5
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 35)
text_a = 10
text_b = 10

over_font =  pygame.font.Font("freesansbold.ttf", 80)

def display_scores(a, b):
    score = font.render(f"SCORE: {str(score_value)}", True, (255 , 255 ,255))
    screen.blit(score, (a, b))

def game_over_text():
    over_text= over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(a, b):
    screen.blit(player_img, (a, b))


def enemy(a, b, i):
    screen.blit(enemy_img[i], (a, b))


def fire_bullet(a, b):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (a, b + 10))

def is_collision(enemy_a, enemy_b, bullet_a, bullet_b):
    distance = math.sqrt((math.pow(enemy_a - bullet_a, 2)) + (math.pow(enemy_b - bullet_b, 2)))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:
    # clock.tick(1000)
    screen.fill((0, 0, 0))
    screen.blit(scaled_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                player_a_change = -1
            if event.key == pygame.K_RIGHT:
                player_a_change = 1


            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("bullet.mp3")
                    bullet_sound.play()
                    bullet_a = player_a
                    fire_bullet(bullet_a, bullet_b)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_a_change = 0

    player_a += player_a_change
    if player_a <= 0:
        player_a = 0
    elif player_a >=736:
        player_a = 736


    for i in range(enemy_number):
        if enemy_b[i] > 440:
            for j in range(enemy_number):
                enemy_b[j] = 3000
            mixer.music.stop()
            game_over_sound = mixer.Sound("over.wav")
            game_over_sound.play()
            game_over_text()
            break


        if enemy_a[i] <= 0:
            enemy_a_change[i] = .5
            enemy_b[i] += enemy_b_change[i]
        elif enemy_a[i] >= 736:
            enemy_a_change[i] = -.5
            enemy_b[i] += enemy_b_change[i]

        collision = is_collision(enemy_a[i], enemy_b[i], bullet_a, bullet_b)
        if collision:
            explosion_sound = mixer.Sound("mineexpolosion.wav")
            explosion_sound.play()
            bullet_b = 480
            bullet_state = "ready"
            score_value += 1
            enemy_a[i] = random.randint(0, 735)
            enemy_b[i] = random.randint(50, 150)
        enemy(enemy_a[i], enemy_b[i], i)
        enemy_a[i] += enemy_a_change[i]

    if bullet_b <= 0:
        bullet_b = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet_b -= bullet_b_change
        fire_bullet(bullet_a, bullet_b)


    player(player_a, player_b)
    display_scores(text_a, text_b)

    pygame.display.flip()








