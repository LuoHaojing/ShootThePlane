__author__ = 'Sabrina.Luo'
import pygame
import sys
import time
import random

screen_width = 400
screen_height = 600


class Plane:
    def __init__(self):
        self.image = pygame.image.load('myplane.png').convert_alpha()
        self.x = (screen_width - self.image.get_width()) / 2
        self.y = (screen_height - self.image.get_height())

    def move(self):
        speed = 10
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and self.x > 0:
            self.x -= speed
        elif key[pygame.K_RIGHT] and self.x + self.image.get_width() < screen_width:
            self.x += speed
        elif key[pygame.K_UP] and self.y > 0:
            self.y -= speed
        elif key[pygame.K_DOWN] and self.y + self.image.get_height() < screen_height:
            self.y += speed


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('bullet.png').convert_alpha()

    def move(self):
        speed = 20
        self.y -= speed


class Enemy:
    def __init__(self):
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.x = random.randint(0, screen_width - self.image.get_width())
        self.y = 0

    def move(self):
        speed_list = [4, 8, 12]
        self.y += random.choice(speed_list)


pygame.init()
screen = pygame.display.set_mode((400, 600), 0, 0)
title = pygame.display.set_caption('ShootThePlane')
font = pygame.font.SysFont('Arial', 30, bold=True)
background = pygame.image.load('bg.jpg').convert()

plane = Plane()
bullets = []
enemies = []

interval0 = 200
b_interval = 0
e_interval = 0

game_over = 0
score = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    if b_interval == 0:
        b_x = plane.x + plane.image.get_width() / 2
        b_y = plane.y + 50
        bullets.append(Bullet(b_x, b_y))

    if e_interval == 0:
        enemies.append(Enemy())

    for bubu in reversed(bullets):
        bubu.move()
        screen.blit(bubu.image, (bubu.x, bubu.y))
        if bubu.y < 0:
            bullets.remove(bubu)

    b_interval += 20  # interval of bullets, the bigger the faster
    e_interval += 20
    if b_interval == interval0:
        b_interval = 0
    if e_interval == interval0:
        e_interval = 0

    for wuwu in reversed(enemies):
        wuwu.move()
        screen.blit(wuwu.image, (wuwu.x, wuwu.y))
        if wuwu.y + wuwu.image.get_height() > screen_height:
            enemies.remove(wuwu)

    for bubu in reversed(bullets):
        if game_over == 1:
            break
        for wuwu in reversed(enemies):
            if wuwu.y + wuwu.image.get_height() > plane.y + 30:
                if wuwu.x < plane.x < wuwu.x + wuwu.image.get_width() - \
                        20 or wuwu.x + 20 < plane.x + plane.image.get_width() \
                        < wuwu.x + wuwu.image.get_width():
                    game_over = 1
                    break

            if wuwu.x < bubu.x < wuwu.x + wuwu.image.get_width() and wuwu.y < \
                    bubu.y < wuwu.y + wuwu.image.get_height():
                score += 1000
                bullets.remove(bubu)
                enemies.remove(wuwu)
                break

    screen.blit(plane.image, (plane.x, plane.y))
    plane.move()

    text_score = font.render('Score:%s' % score, 1, (0, 0, 0))
    screen.blit(text_score, (0, 0))

    if game_over == 1:
        text_over = font.render('Game Over', 1, (255, 0, 0), (0, 0, 0))
        screen.blit(text_over, (150, 300))

    pygame.display.update()
    time.sleep(0.05)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
