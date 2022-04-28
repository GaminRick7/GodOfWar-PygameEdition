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


steps = 2




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
'                           XXXXXXXXXXX ',
' XX    XXX            XX    ',
' XXP                             XXXXXX',
' XXXX         XX         XX ',
' XXXX       XX        E     XXXXXXXX ',
' XX    X  XXXX    XX  XX       XXXXXXXXXXXXXXXXXXXXXXXXXXXX ',
'       X  XXXX    XX  XXX             ',
'    XXXX  XXXXXX  XX  XXXXXXXXX      X',
'XXXXXXXX  XXXXXX  XX  XXXXXXXXXXXXX XXXXXXXXXXX ']

level = Level(level_map, screen)
scroll_speed =0
################ MAIN ####################
level.setup_level(level_map)
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
                level.player.control(-steps, 0)
                scroll_speed -= 2
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                level.player.control(steps, 0)
                scroll_speed +=2
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == ord('w'):
                level.player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                level.player.control(steps, 0)
                scroll_speed = 0
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                level.player.control(-steps, 0)
                scroll_speed = 0
    bg.scroll(scroll_speed)
    clock.tick(fps)
    bg.draw(screen)
    level.run()
    pygame.display.flip()