import pygame
import sys
import os
import time
from player import Player
from enemy import Enemy
from tile import Tile
from spritesheet import Spritesheet
from level import Level
import parallax
from math import inf

############## VARIABLES ###############
#

worldx = 960
worldy = 480
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((worldx, worldy))
fps = 40  # frame rate
ani = 4   # animation cycles
main = True

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

############### INITIAL SETUP #############

clock = pygame.time.Clock()
pygame.init()
world = pygame.display.set_mode([worldx, worldy])
backdrop = pygame.image.load(os.path.join('images', 'mountain.png'))
backdrop = pygame.transform.scale(backdrop, (960, 480))
backdropbox = world.get_rect()

player = Player()  # spawn player
player.rect.x = 0  # go to x
player.rect.y = 0  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 2


enemy = Enemy(300, 0, 4, "enemy1")
enemy_list = pygame.sprite.Group()
enemy_list.add(enemy)

########## BACKGROUND ###############
bg = parallax.ParallaxSurface((960, 480), pygame.RLEACCEL)
# clouds should not move at all
bg.add(os.path.join('images', 'background','01.png'), inf)

# 02.png pans 3x faster than 07.png
bg.add(os.path.join('images', 'background','02.png'), 3)
bg.add(os.path.join('images', 'background','03.png'), 2.5)
bg.add(os.path.join('images', 'background','04.png'), 2)
bg.add(os.path.join('images', 'background','05.png'), 1.5)
bg.add(os.path.join('images', 'background','06.png'), 1)
bg.add(os.path.join('images', 'background','07.png'), 1)

level_map = [
'                            ',
'                            ',
' XX    XXX            XX    ',
' XX P                       ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

level = Level(level_map, screen)
scroll_speed =0
################ MAIN ####################

while main:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
                scroll_speed -= 2
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
                scroll_speed +=2
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
                scroll_speed = 0
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
                scroll_speed = 0
    bg.scroll(scroll_speed)
    clock.tick(fps)
    bg.draw(screen)
    level.setup_level(level_map)
    level.run()
    player.update()
    enemy_list.draw(world)
    enemy.update()
    player_list.draw(world)
    pygame.display.flip()